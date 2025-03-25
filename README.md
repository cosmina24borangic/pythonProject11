
EXPLICATIE PROIECT – CONVERSIE SI GRUPARE LOGO-URI

Structura folderului `pip`:
pip/
├── __main__.py                # Fisierul principal care trebuie rulat
├── convert_parquet.py         # Conversie din Parquet in CSV
├── download_logos.py          # Descarca logo-uri pe baza domeniilor
├── compare_logos.py           # Grupeaza logo-urile vizual (foloseste AI)
├── logos/                     # Folder unde se salveaza toate logo-urile descarcate
├── logos.snappy.parquet       # Setul de date initial (format Parquet)
├── logos2.csv                 # Fisierul CSV generat automat
├── logo_clusters.csv          # Fisier CSV cu rezultatele gruparilor

Ce face codul?

1. convert_parquet.py
   - Functia convert_parquet_to_csv deschide fisierul `.parquet` si il transforma in `.csv` folosind pandas + pyarrow
   - Codul este eficient deoarece foloseste biblioteca Pandas pentru a citi fisierul Parquet si a-l converti rapid in format CSV. Functia este simpla si reutilizabila, iar utilizarea modulului pyarrow asigura performanta buna la citire. Conversia elimina indexul, ceea ce face fisierul rezultat mai curat si pregatit pentru analiza sau procesare ulterioara

2. download_logos.py
   - Functia download_logo descarca logo-ul pentru fiecare domeniu si il salveaza in folderul `logos/`
   - Verifica daca fisierul exista deja ca sa nu-l descarce din nou
   - Codul este eficient deoarece foloseste paralelizarea cu ThreadPoolExecutor, ceea ce permite descarcarea mai multor logo-uri in acelasi timp, reducand semnificativ timpul total de executie. Se evita descarcarile duplicate prin verificarea existentei fisierului inainte. In plus, sunt tratate erorile de retea pentru a preveni blocarea programului. Logo-urile sunt grupate si salvate intr-un fisier CSV pentru analiza ulterioara, iar rezultatele sunt afisate si vizual, ceea ce imbunatateste experienta utilizatorului
  
3. compare_logos.py
   - Primeste logo-urile si le compara vizual
   - Grupeaza pe baza similaritatii (fara ML)
   - Salveaza gruparile in `logo_clusters.csv`
   - Functia group_logos_with_tracking grupeaza logo-urile pe baza similaritatii vizuale, fara sa foloseasca algoritmi de clustering din machine learning. Pentru fiecare imagine, extrage caracteristici combinand doua modele AI pre-antrenate: CLIP (pentru forma si semantica) si ResNet50 (pentru detalii vizuale). Apoi, calculeaza similaritatea intre logo-uri si le grupeaza daca scorul depaseste un anumit prag. Salveaza rezultatele si compara cu rularile anterioare pentru a urmari evolutia grupurilor. Am ales aceasta metoda pentru ca este explicabila, respecta cerinta de a nu folosi ML clasic si ofera rezultate clare

4. __main__.py
   - ESTE FISIERUL CARE TREBUIE RULAT
   - Pasi:
     - Converteste `.parquet` in `.csv`
     - Extrage domeniile
     - Descarca logo-urile
     - Grupeaza si salveaza rezultatele
Cum rulezi proiectul

1. Navigheaza in PyCharm la fisierul:
   .../pythonProject11/.venv/Lib/site-packages/pip/__main__.py

2. Ruleaza fisierul __main__.py:
   - Click dreapta > Run '__main__'
   - Sau in terminal:
     python -m pip.__main__

Ce fisiere sunt generate si unde?

| Fisier               | Locatie       | Continut                                         |
|----------------------|----------------|--------------------------------------------------|
| logos2.csv           | pip/           | Domeniile convertite din `.parquet`             |
| logos/               | pip/logos/     | Toate logo-urile salvate ca `.png`              |
| logo_clusters.csv    | pip/           | Gruparile de logo-uri similare (AI-based)       |

De ce a fost organizat asa?

- Separare clara intre conversie, descarcare si comparare
- Rulezi un singur fisier: __main__.py
- Descarcare rapida prin paralelizare
- Usor de reutilizat fisierele generate
