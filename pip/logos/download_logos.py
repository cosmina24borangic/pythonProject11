import requests
import os
import pandas as pd

def download_logo(domain):
    """Funcție care descarcă logo-ul unui site pe baza domeniului"""
    logo_url = f"https://logo.clearbit.com/{domain}"
    try:
        response = requests.get(logo_url, stream=True)
        if response.status_code == 200:
            os.makedirs("logos", exist_ok=True)
            file_path = f"logos/{domain}.png"
            with open(file_path, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            return file_path
    except Exception as e:
        print(f"Eroare la descărcare pentru {domain}: {e}")
    return None

if __name__ == "__main__":
    df = pd.read_csv("logos2.csv")
    domains = df["domain"].dropna().tolist()  # Descărcăm toate logo-urile
    logo_paths = {domain: download_logo(domain) for domain in domains}

    # Filtrăm doar logo-urile descărcate cu succes
    valid_logos = {domain: path for domain, path in logo_paths.items() if path}

    print("Logo-urile descărcate cu succes:")
    print(valid_logos)