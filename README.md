
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
   - Deschide fisierul .parquet folosind Pandas si motorul PyArrow
   - Citeste datele in memorie sub forma de DataFrame
   - Transforma continutul in format .csv
   - Salveaza fisierul .csv fara coloana de index
   - Afiseaza un mesaj de confirmare la final
   - Returneaza DataFrame-ul rezultat pentru utilizare ulterioara 
   - Codul este eficient deoarece foloseste biblioteca Pandas pentru a citi fisierul Parquet si a-l converti rapid in format CSV. Functia este simpla si reutilizabila, iar utilizarea modulului pyarrow asigura performanta buna la citire. Conversia elimina indexul, ceea ce face fisierul rezultat mai curat si pregatit pentru analiza sau procesare ulterioara

2. download_logos.py
   - Primeste o lista de domenii web
   - Descarca logo-urile in paralel folosind ThreadPoolExecutor
   - Apeleaza o functie externa pentru a grupa logo-urile in functie de similaritate vizuala
   - Salveaza rezultatele in fisierul logo_clusters.csv
   - Afiseaza grupurile in consola si vizual pe ecran
   - Codul este eficient deoarece foloseste paralelizarea cu ThreadPoolExecutor, ceea ce permite descarcarea mai multor logo-uri in acelasi timp, reducand semnificativ timpul total de executie. Se evita descarcarile duplicate prin verificarea existentei fisierului inainte. In plus, sunt tratate erorile de retea pentru a preveni blocarea programului. Logo-urile sunt grupate si salvate intr-un fisier CSV pentru analiza ulterioara, iar rezultatele sunt afisate si vizual, ceea ce imbunatateste experienta utilizatorului
  
3. compare_logos.py
   - Incarca modelele pre-antrenate CLIP si ResNet pentru extragerea caracteristicilor vizuale
   - Deschide fiecare imagine si extrage vectori de caracteristici folosind ambele modele
   - Comaseaza vectorii CLIP si ResNet intr-un singur vector unificat pentru fiecare imagine
   - Calculeaza similaritatea cosinus intre toate perechile de imagini
   - Grupeaza imaginile in functie de acest scor de similaritate, pe baza unui prag configurabil
   - Aplica normalizare cu StandardScaler pentru alinierea distributiilor
   - Salveaza grupurile rezultate intr-un fisier .pkl cu timestamp
   - Daca exista un fisier anterior de clustere, compara evolutia intre vechi si nou: imagini mutate, adaugate sau eliminate
   - Ofera o functie de afisare vizuala a grupurilor, unde fiecare cluster este prezentat cu imaginile sale alaturate

4. __main__.py
   - ESTE FISIERUL CARE TREBUIE RULAT
   - Pasi:
     - Gestioneaza procesul complet de obtinere si analiza a logo-urilor pentru o lista de domenii
     - Converteste un fisier .parquet in .csv folosind Pandas (prin convert_parquet.convert_parquet_to_csv)
     - Extrage coloana domain din fisierul CSV si o transforma intr-o lista
     - Utilizeaza functia download_logo() din modulul download_logos pentru a descarca logo-urile dintr-un serviciu online (clearbit.com)
     - Foloseste ThreadPoolExecutor pentru descarcarea paralela a logo-urilor
     - Creeaza o mapare domain -> fisier_logo si elimina intrarile esuate
     - Apeleaza group_logos_with_tracking() din modulul compare_logos pentru a grupa logo-urile pe baza similaritatii vizuale (CLIP + ResNet)
     - Scrie rezultatele grupate intr-un fisier CSV (logo_clusters.csv) cu format: cluster, domenii, logo-uri
     - Afiseaza grupurile in consola
     - Apeleaza show_clusters() din compare_logos pentru a afisa fiecare grup de logo-uri vizual, folosind Matplotlib
Cum rulezi proiectul

1. Navigheaza in PyCharm la fisierul:
   .../pythonProject11/pip/__main__.py

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
