import os
import numpy as np
import cv2
import torch
import clip
import matplotlib.pyplot as plt
import pickle
import warnings
from PIL import Image
from datetime import datetime
import torchvision.transforms as transforms
from torchvision.models import resnet50, ResNet50_Weights
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

# Optional: ascundem warningurile
warnings.filterwarnings("ignore")

# Setare pentru numar maxim de thread-uri
os.environ["LOKY_MAX_CPU_COUNT"] = "4"

# Initializare modele
device = "cuda" if torch.cuda.is_available() else "cpu"
clip_model, preprocess = clip.load("ViT-B/32", device=device)

resnet = resnet50(weights=ResNet50_Weights.DEFAULT).to(device)
resnet.eval()
resnet_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])


# Extrage caracteristici dintr-o imagine folosind CLIP si ResNet
def extract_features(img_path):
    if not os.path.exists(img_path):
        print(f" Fisier inexistent: {img_path}")
        return None

    # Convertim imaginea inclusiv pentru RGBA (pt. warning transparență)
    image = Image.open(img_path).convert("RGBA").convert("RGB")

    # CLIP features
    clip_img = preprocess(image).unsqueeze(0).to(device)
    with torch.no_grad():
        clip_features = clip_model.encode_image(clip_img).cpu().numpy().flatten()

    # ResNet features
    resnet_img = resnet_transform(image).unsqueeze(0).to(device)
    with torch.no_grad():
        resnet_features = resnet(resnet_img).cpu().numpy().flatten()

    return np.concatenate((clip_features, resnet_features))


# Salvare caracteristici extrase
def save_features(features, filename="features.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(features, f)


# Incarcare caracteristici existente
def load_features(filename="features.pkl"):
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            return pickle.load(f)
    return {}


# Grupare pe baza similaritatii
def group_by_similarity(features_dict, threshold=0.85):
    logo_names = list(features_dict.keys())
    feature_vectors = np.array([features_dict[name] for name in logo_names])

    scaler = StandardScaler()
    feature_vectors = scaler.fit_transform(feature_vectors)

    sim_matrix = cosine_similarity(feature_vectors)

    clusters = []
    visited = set()

    for i in range(len(logo_names)):
        if i in visited:
            continue
        group = [logo_names[i]]
        visited.add(i)
        for j in range(i + 1, len(logo_names)):
            if j not in visited and sim_matrix[i][j] > threshold:
                group.append(logo_names[j])
                visited.add(j)
        clusters.append(group)

    return {i: group for i, group in enumerate(clusters)}


# Salvare clustere cu timestamp
def save_clusters(clusters):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"clusters_{timestamp}.pkl"
    with open(filename, "wb") as f:
        pickle.dump(clusters, f)
    print(f" Clusterele au fost salvate in {filename}")
    return filename


# Compara clusterele vechi si noi


def compare_clusters(old_clusters, new_clusters):
    old_flat = {img: cid for cid, imgs in old_clusters.items() for img in imgs}
    new_flat = {img: cid for cid, imgs in new_clusters.items() for img in imgs}

    print("\nComparare evoluție clustere:")
    for img, new_cluster in new_flat.items():
        old_cluster = old_flat.get(img)
        if old_cluster is None:
            print(f"{img} a fost adăugat în grupul {new_cluster}")
        elif old_cluster != new_cluster:
            print(f"{img} s-a mutat din grupul {old_cluster} în {new_cluster}")

    removed = set(old_flat.keys()) - set(new_flat.keys())
    for img in removed:
        print(f"{img} a fost eliminat din clustere")


# Obtine cel mai recent fisier de clustere
def get_latest_cluster_file():
    files = [f for f in os.listdir() if f.startswith("clusters_") and f.endswith(".pkl")]
    if not files:
        return None
    return sorted(files)[-1]


# Grupeaza logo-urile si urmareste modificarile
def group_logos_with_tracking(logo_paths, similarity_threshold=0.85):
    features_dict = {path: extract_features(path) for path in logo_paths.values() if os.path.exists(path)}
    save_features(features_dict)

    if not features_dict:
        print("Niciun logo valid pentru comparare!")
        return {}

    new_clusters = group_by_similarity(features_dict, threshold=similarity_threshold)

    previous_cluster_file = get_latest_cluster_file()
    if previous_cluster_file:
        with open(previous_cluster_file, "rb") as f:
            old_clusters = pickle.load(f)
        compare_clusters(old_clusters, new_clusters)
        compare_clusters(old_clusters, new_clusters)

    save_clusters(new_clusters)
    return new_clusters


# Afisare clustere
def show_clusters(clusters):
    for cluster_id, logos in clusters.items():
        num_logos = len(logos)
        fig, axes = plt.subplots(1, num_logos, figsize=(num_logos * 3, 3))
        fig.suptitle(f"Grup {cluster_id}", fontsize=16)

        if num_logos == 1:
            axes = [axes]
        for ax, logo_path in zip(axes, logos):
            img = cv2.imread(logo_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            ax.imshow(img)
            ax.axis("off")
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.show()
