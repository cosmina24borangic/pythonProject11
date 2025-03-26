import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

# Extrage histograma HSV
def extract_color_histogram(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return None
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([hsv], [0, 1], None, [50, 60], [0, 180, 0, 256])
    cv2.normalize(hist, hist)
    return hist.flatten()

# Extrage descriptorii ORB
def extract_orb_descriptors(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        return None
    orb = cv2.ORB_create()
    keypoints, descriptors = orb.detectAndCompute(image, None)
    return descriptors

# Compara descriptorii ORB folosind brute-force matcher
def compare_orb(desc1, desc2):
    if desc1 is None or desc2 is None:
        return 0
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(desc1, desc2)
    if not matches:
        return 0
    scores = [m.distance for m in matches]
    return 1 - (sum(scores) / (len(scores) * 256))  # normalize between 0 and 1

# Compara histogramele
def compare_histograms(hist1, hist2):
    return cv2.compareHist(hist1.astype("float32"), hist2.astype("float32"), cv2.HISTCMP_CORREL)

# Grupeaza pe bază de histograma + ORB
def group_logos_with_tracking(logo_paths, hist_threshold=0.8, orb_threshold=0.15):
    features = {
        path: {
            "hist": extract_color_histogram(path),
            "orb": extract_orb_descriptors(path)
        } for path in logo_paths.values() if os.path.exists(path)
    }

    clusters = []
    visited = set()
    keys = list(features.keys())

    for i, key1 in enumerate(keys):
        if key1 in visited:
            continue
        cluster = [key1]
        visited.add(key1)
        for j in range(i + 1, len(keys)):
            key2 = keys[j]
            if key2 in visited:
                continue

            hist_sim = compare_histograms(features[key1]["hist"], features[key2]["hist"])
            orb_sim = compare_orb(features[key1]["orb"], features[key2]["orb"])


            if hist_sim > hist_threshold or orb_sim > orb_threshold:
                cluster.append(key2)
                visited.add(key2)

        clusters.append(cluster)

    return {i: group for i, group in enumerate(clusters)}

# Vizualizare
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
