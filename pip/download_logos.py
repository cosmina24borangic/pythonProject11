import os
import requests
import concurrent.futures

import compare_logos


def download_logo(domain):
    logo_url = f"https://logo.clearbit.com/{domain}"
    file_path = f"logos/{domain}.png"

    if os.path.exists(file_path):
        return file_path

    try:
        response = requests.get(logo_url, stream=True, timeout=3)
        if response.status_code == 200:
            os.makedirs("logos", exist_ok=True)
            with open(file_path, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Logo descarcat: {domain}")
            return file_path
        else:
            print(f"Logo indisponibil pentru {domain} (Status: {response.status_code})")
    except requests.exceptions.RequestException:
        print(f"Eroare la descarcare: {domain}")
    return None


def process_logos(domains):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(download_logo, domains))
    print(f"Descarcare completa! {sum(1 for r in results if r)} logo-uri salvate.")

    logo_paths = {
        domain: path for domain, path in zip(domains, results) if path is not None
    }

    print(f"Am descarcat {len(logo_paths)} logo-uri. Incepem gruparea...")

    clusters = compare_logos.group_logos_with_tracking(logo_paths)

    with open("logo_clusters.csv", "w", encoding="utf-8") as f:
        f.write("Cluster,Domenii,Logo-uri\n")
        for cluster_id, logos in clusters.items():
            domains_in_group = [domain for domain, path in logo_paths.items() if path in logos]
            f.write(f"Grup {cluster_id}, {', '.join(domains_in_group)}, {', '.join(logos)}\n")

    print("Grupurile de logo-uri au fost salvate in 'logo_clusters.csv'!")

    if clusters:
        print("\nGrupuri de logo-uri similare:")
        for cluster_id, logos in clusters.items():
            domains_in_group = [domain for domain, path in logo_paths.items() if path in logos]
            print(f"Grup {cluster_id}: Domenii {domains_in_group} -> Logo-uri: {logos}")

        compare_logos.show_clusters(clusters)
    else:
        print("Nu s-au generat grupuri de logo-uri!")
