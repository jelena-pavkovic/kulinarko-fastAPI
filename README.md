# Kulinarko API

Backend za Kulinarko - aplikaciju za porodičnu knjigu recepata i planiranje kupovine, razvijenu kao lični/porodični projekat.

## O projektu

Kulinarko omogućava čuvanje recepata, praćenje sastojaka (imam / treba da kupim / neoznačeno) i automatsko generisanje liste za kupovinu na osnovu izabranih recepata.

## Tehnologije

- **Python** + **FastAPI**
- **PostgreSQL** (baza `kulinarko`)
- **psycopg2** za konekciju sa bazom
- **python-dotenv** za konfiguraciju putem `.env` fajla

## Struktura baze

7 tabela:

- `categories`
- `recipes`
- `ingredients`
- `recipe_ingredients`
- `steps`
- `shopping_lists`
- `shopping_items`

## Pokretanje projekta

1. Kloniraj repozitorijum i uđi u folder projekta:

   ```bash
   git clone <url-repozitorijuma>
   cd kulinarko_api
   ```

2. Napravi virtuelno okruženje i aktiviraj ga:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Instaliraj zavisnosti:

   ```bash
   pip install -r requirements.txt
   ```

4. Napravi `.env` fajl u root folderu sa sledećim sadržajem (popuni svojim vrednostima):

   ```
   DB_USER=tvoje_korisnicko_ime
   DB_PASSWORD=tvoja_lozinka
   DB_HOST=localhost
   DB_NAME=kulinarko
   ```

5. Pokreni server:

   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

6. API dokumentacija dostupna na:
   ```
   http://localhost:8000/docs
   ```

## Napomena

`.env` fajl se ne kači na GitHub (nalazi se u `.gitignore`) i sadrži osetljive podatke o konekciji ka bazi.

## Planirane funkcionalnosti

- Finansijsko planiranje na osnovu cena sastojaka
- Zaseban ekran za sastojke/artikle (katalog koji se deli između recepata)
- Kategorija "grickalice" - artikli koji se dodaju direktno na listu za kupovinu, bez upotrebe u receptima
- Korisnički nalozi / prijava (planirano za kraj, nakon ostalih funkcionalnosti)
  git
