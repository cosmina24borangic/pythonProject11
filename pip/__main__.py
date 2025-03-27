import convert_parquet
import download_logos
import compare_logos
import pandas as pd
import concurrent.futures
import os

if __name__ == "__main__":
    # Convertim fisierul Parquet in CSV
    input_file = "logos.snappy.parquet"
    output_file = "logos2.csv"
    df = convert_parquet.convert_parquet_to_csv(input_file, output_file)

    # Descarcam toate logo-urile
    print("Incepem descarcarea logo-urilor...")
    domains = df["domain"].dropna().tolist()

    # Descarcare paralelizata
    with concurrent.futures.ThreadPoolExecutor() as executor:
        logo_paths = {
            domain: path for domain, path in zip(domains, executor.map(download_logos.download_logo, domains))
            if path is not None
        }

    print(f"Am descarcat {len(logo_paths)} logo-uri. Incepem gruparea...")

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