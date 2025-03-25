"""
import convert_parquet
import download_logos
import compare_logos
import pandas as pd

if __name__ == "__main__":
    # 1️⃣ Convertim fișierul Parquet în CSV
    input_file = "logos.snappy.parquet"
    output_file = "logos2.csv"
    df = convert_parquet.convert_parquet_to_csv(input_file, output_file)

    # 2️⃣ Descărcăm **DOAR PRIMELE 50** de logo-uri
    print("🔽 Începem descărcarea logo-urilor...")
    domains = df["domain"].dropna().head(50).tolist()  # Limităm la 50
    logo_paths = {domain: download_logos.download_logo(domain) for domain in domains}

    # 3️⃣ Comparăm și grupăm **DOAR CELE DESCĂRCATE CU SUCCES**
    valid_logos = [logo for logo in logo_paths.values() if logo is not None]
    print(f"✅ Am descărcat cu succes {len(valid_logos)} logo-uri. Începem compararea...")

    # **🔹 Apelăm funcția de grupare corectă**
    # Filtrăm doar logo-urile descărcate cu succes
    valid_logo_paths = {domain: path for domain, path in logo_paths.items() if path is not None}

    # Apelăm gruparea doar cu logo-urile valide
    clusters = compare_logos.group_logos(valid_logo_paths)

    # 5️⃣ Afișăm grupările în consolă
    if clusters:  # Dacă există grupuri returnate
        print("\n🔹 **Grupuri de logo-uri similare:**")
        for cluster_id, logos in clusters.items():
            if cluster_id != -1:  # -1 înseamnă logo unic (outlier)
                print(f"✅ Grup {cluster_id}: {logos}")

        # Afișează logo-urile care nu au pereche
        unique_logos = clusters.get(-1, [])
        if unique_logos:
            print("\n🚀 **Logo-uri unice (fără pereche):**")
            print(unique_logos)
    else:
        print("❌ Nu s-au generat grupuri de logo-uri!") """
"""
import convert_parquet
import download_logos
import compare_logos
import pandas as pd

if __name__ == "__main__":
    # 1️⃣ Convertim fișierul Parquet în CSV
    input_file = "logos.snappy.parquet"
    output_file = "logos2.csv"
    df = convert_parquet.convert_parquet_to_csv(input_file, output_file)

    # 2️⃣ Descărcăm **DOAR PRIMELE 50** de logo-uri
    print("🔽 Începem descărcarea logo-urilor...")
    domains = df["domain"].dropna().head(50).tolist()  # Limităm la 50
    logo_paths = {domain: download_logos.download_logo(domain) for domain in domains}

    # 3️⃣ Comparăm și grupăm **DOAR CELE DESCĂRCATE CU SUCCES**
    valid_logo_paths = {domain: path for domain, path in logo_paths.items() if path is not None}

    print(f"✅ Am descărcat cu succes {len(valid_logo_paths)} logo-uri. Începem compararea folosind AI...")

    # **🔹 Apelăm noua funcție bazată pe ResNet50**
    clusters = compare_logos.group_logos_with_clustering(valid_logo_paths)

    # 5️⃣ Afișăm grupările în consolă și vizual
    if clusters:  # Dacă există grupuri returnate
        print("\n🔹 **Grupuri de logo-uri similare (AI-based):**")
        for cluster_id, logos in clusters.items():
            if cluster_id != -1:  # -1 înseamnă logo unic (outlier)
                domains_in_group = [domain for domain, path in valid_logo_paths.items() if path in logos]
                print(f"✅ Grup {cluster_id}: Domenii {domains_in_group} -> Logo-uri: {logos}")

        # Afișează logo-urile care nu au pereche
        unique_logos = clusters.get(-1, [])
        if unique_logos:
            print("\n🚀 **Logo-uri unice (fără pereche):**")
            for idx, logo in enumerate(unique_logos):
                domain = [domain for domain, path in valid_logo_paths.items() if path == logo]
                print(f"❗ Grup Unic {idx + 1}: Domeniu {domain} -> Logo: {logo}")

        # 🔹 Afișăm grupurile de logo-uri vizual
        compare_logos.show_clusters(clusters)
    else:
        print("❌ Nu s-au generat grupuri de logo-uri!")"""
"""import convert_parquet
import download_logos
import compare_logos
import pandas as pd

if __name__ == "__main__":
    # 1️⃣ Convertim fișierul Parquet în CSV
    input_file = "logos.snappy.parquet"
    output_file = "logos2.csv"
    df = convert_parquet.convert_parquet_to_csv(input_file, output_file)

    # 2️⃣ Descărcăm **DOAR PRIMELE 50** de logo-uri
    print("🔽 Începem descărcarea logo-urilor...")
    domains = df["domain"].dropna().head(50).tolist()  # Limităm la 50
    logo_paths = {domain: download_logos.download_logo(domain) for domain in domains}

    # 3️⃣ Comparăm și grupăm **DOAR CELE DESCĂRCATE CU SUCCES**
    valid_logo_paths = {domain: path for domain, path in logo_paths.items() if path is not None}

    print(f"✅ Am descărcat cu succes {len(valid_logo_paths)} logo-uri. Începem compararea folosind AI...")

    # **🔹 Apelăm noua funcție de grupare cu CLIP și ResNet50**
    clusters = compare_logos.group_logos_with_clustering(valid_logo_paths)

    # 5️⃣ Salvăm grupările într-un fișier CSV
    with open("logo_clusters.csv", "w", encoding="utf-8") as f:
        f.write("Cluster,Domenii,Logo-uri\n")
        for cluster_id, logos in clusters.items():
            if cluster_id != -1:
                domains_in_group = [domain for domain, path in valid_logo_paths.items() if path in logos]
                f.write(f"Grup {cluster_id}, {', '.join(domains_in_group)}, {', '.join(logos)}\n")

        unique_logos = clusters.get(-1, [])
        if unique_logos:
            for idx, logo in enumerate(unique_logos):
                domain = [domain for domain, path in valid_logo_paths.items() if path == logo]
                f.write(f"Grup Unic {idx + 1}, {', '.join(domain)}, {logo}\n")

    print("✅ Grupurile de logo-uri au fost salvate în 'logo_clusters.csv'!")

    # 6️⃣ Afișăm grupările în consolă și vizual
    if clusters:
        print("\n🔹 **Grupuri de logo-uri similare (AI-based):**")
        for cluster_id, logos in clusters.items():
            if cluster_id != -1:
                domains_in_group = [domain for domain, path in valid_logo_paths.items() if path in logos]
                print(f"✅ Grup {cluster_id}: Domenii {domains_in_group} -> Logo-uri: {logos}")

        # Afișează logo-urile care nu au pereche
        unique_logos = clusters.get(-1, [])
        if unique_logos:
            print("\n🚀 **Logo-uri unice (fără pereche):**")
            for idx, logo in enumerate(unique_logos):
                domain = [domain for domain, path in valid_logo_paths.items() if path == logo]
                print(f"❗ Grup Unic {idx + 1}: Domeniu {domain} -> Logo: {logo}")

        # 🔹 Afișăm grupurile de logo-uri vizual
        compare_logos.show_clusters(clusters)
    else:
        print("❌ Nu s-au generat grupuri de logo-uri!")
"""
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