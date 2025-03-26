import os
import requests
import concurrent.futures
import compare_logos


def download_logo(domain, retries=2):
    logo_url = f"https://logo.clearbit.com/{domain}"
    file_path = f"logos/{domain}.png"

    if os.path.exists(file_path):
        print(f"Logo deja existent: {domain}")
        return file_path

    os.makedirs("logos", exist_ok=True)

    attempt = 0
    while attempt <= retries:
        try:
            response = requests.get(logo_url, stream=True, timeout=10)
            if response.status_code == 200:
                with open(file_path, "wb") as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                print(f"Logo descarcat: {domain}")
                return file_path
            else:
                print(f"Logo indisponibil pentru {domain} (Status: {response.status_code})")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Eroare la descarcare: {domain}, retry {attempt}/{retries}")
            attempt += 1

    return None


def process_logos(domains):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(download_logo, domains))

    logo_paths = {
        domain: path for domain, path in zip(domains, results) if path is not None
    }

    print(f"Descarcare completa! {len(logo_paths)} logo-uri salvate.")
    print("Incepem gruparea...")

    clusters = compare_logos.group_logos_with_tracking(logo_paths)

    # Salvam gruparile intr-un fisier CSV
    with open("logo_clusters.csv", "w", encoding="utf-8") as f:
        f.write("Cluster,Domenii,Logo-uri\n")
        for cluster_id, logos in clusters.items():
            domains_in_group = [domain for domain, path in logo_paths.items() if path in logos]
            f.write(f"Grup {cluster_id}, {', '.join(domains_in_group)}, {', '.join(logos)}\n")

    print("Grupurile de logo-uri au fost salvate in 'logo_clusters.csv'!")

    # Afisam in consola si vizual
    if clusters:
        print("\nGrupuri de logo-uri similare:")
        for cluster_id, logos in clusters.items():
            domains_in_group = [domain for domain, path in logo_paths.items() if path in logos]
            print(f"Grup {cluster_id}: Domenii {domains_in_group} -> Logo-uri: {logos}")

        compare_logos.show_clusters(clusters)
    else:
        print("Nu s-au generat grupuri de logo-uri!")
