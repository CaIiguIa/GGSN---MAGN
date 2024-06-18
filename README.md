# Projekt MAGN — Implementacja biblioteki do budowy Multi-Associative Graph Network (MAGN) oraz uczenia (klasyfikacja + regresja)
### Autorzy:

- Szymon Jurecki
- Dominik Breksa

### Opis projektu:

Z uwagi na to, że ilość wyprodukowanego przez nas kodu jest zbyt duża, aby umieścić go w jednym pliku, postanowiliśmy stworzyć bibliotekę `magn` w języku python, która realizuje odpowiednie implementacje np. uczenia, tworzenia grafów ASA.

Ponieważ jest to dość rozległy projekt, to pozwolę sobie opisać strukturę projektu:
- Folder `docs` - zawiera wewnętrzną dokumentację, obrazki i zapisy literatury.
- Folder `resources/data` - tutaj znajduje się baza danych później pobrana z platformy Kaggle.
- Folder `src` - ma kod źródłowy paczek python, które stworzyliśmy:
  - Folder `magn` - zawiera paczkę użytą dalej do stworzenia MAGN.
- Folder `tests` - zawiera tymczasowe testy, zbudowanych przez nas method, funkcji i obiektów.
- Plik `.gitignore` - samo opisowe.
- Plik `pyproject.toml` - informacje o paczce niezbędne do instalacji.
- Plik `README.md` - ten tekst.
- PLik `requiements.txt` - zawiera niezbędne paczki zależności.
- Plik `setup.py` - instaluje naszą paczkę.

Następnie pobierzemy bazę danych z platformy Kaggle ([LINK](https://www.kaggle.com)) w formacie SQLite, na jej podstawie zbudujemy konkretny MAGN, potem przeprowadzimy uczenie i przeanalizujemy wyniki w tym notebooku.

### Cel projektu:

1. Implementacja następujących struktur danych dla małej biblioteki:
  - Aggregative Sorting Associative Graphs (ASA-Graphs)
  - Multi-Associative Graph Network (MAGN)
  - Baza danych
2. Przeprowadzenie uczenia na przykładowej bazie danych:
  - Uczenie
  - Predykcja
  - Regresja
  - Obliczenie metryk i porównanie działania.

### Wykorzystane technologie i zależności:
- Python: `3.12.0`
- Pandas: `2.2.2`
- Kaggle: `1.6.14`
- SQLite3: `3.46.0`
- Inne zawarte w `requirements.txt`