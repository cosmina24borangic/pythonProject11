
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
   - Primeste logo-urile si le compară vizual, pe baza unor caracteristici extrase din imagini
   - Extrage histograma de culoare HSV si descriitori ORB (feature points) pentru fiecare logo
   - Compara logo-urile două cate doua folosind:corelatia intre histogramele de culoare si  similaritatea intre descriptorii ORB (folosind brute-force matcher)
   - Grupează logo-urile care sunt suficient de similare vizual, pe baza unor praguri configurabile (hist_threshold, orb_threshold)
   - Nu folosește nicio tehnica de machine learning clasic: nu se antreneaza modele, nu se setează numar de clustere, nu se aplica KMeans, DBSCAN etc
   - Rezultatele sunt returnate sub forma de dictionar de clustere
   - Afiseaza vizual grupurile de logo-uri in ferestre Matplotlib
   - Metoda folosita pentru gruparea logo-urilor este mai eficienta decat tehnicile clasice de machine learning, deoarece evita complet complexitatea inutila. Nu este nevoie de antrenarea unor modele, nu trebuie stabilit dinainte un numar fix de clustere si nu sunt implicati hiperparametri dificil de ajustat. In locul unor algoritmi precum KMeans sau DBSCAN, care pot produce rezultate greu de interpretat, a fost aleasa o solutie mai simpla si mai usor de controlat: compararea directa a imaginilor folosind histograma de culoare si descriitori ORB

4. __main__.py
   - ESTE FISIERUL CARE TREBUIE RULAT
   - Pasi:
     - Gestioneaza procesul complet de obtinere si analiza a logo-urilor pentru o lista de domenii
     - Utilizeaza functia download_logo() pentru a descarca logo-urile dintr-un serviciu online
     - Foloseste ThreadPoolExecutor in process_logos() pentru descarcare paralela
     - Apeleaza group_logos_with_tracking() din modulul compare_logos pentru grupare vizuala
     - Salveaza rezultatele gruparii intr-un fisier CSV folosind operatii standard de scriere in fisier
     - Afiseaza grupurile obtinute in consola si vizual prin show_clusters() din compare_logos
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
