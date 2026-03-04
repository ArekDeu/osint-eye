# 🔍 OSINT Platform

Narzędzie OSINT do wyszukiwania informacji publicznych o osobach.

## Co potrafi?

- 👤 **Imię i nazwisko** → profile social media, możliwe usernames, linki Google
- ✉️ **Email** → sprawdzenie 120+ serwisów (Holehe), wycieki danych (HIBP)
- 📱 **Telefon** → kraj, operator, linki do sprawdzenia
- 🖼️ **Zdjęcie** → linki do wyszukiwarek twarzy (Yandex, Google, PimEyes)

## Uruchomienie lokalne (na swoim komputerze)

### 1. Pobierz projekt

```bash
git clone https://github.com/TWOJ_NICK/osint-platform.git
cd osint-platform
```

### 2. Zainstaluj biblioteki

```bash
cd backend
pip install -r requirements.txt
```

### 3. Uruchom serwer

```bash
python main.py
```

### 4. Otwórz w przeglądarce

```
http://localhost:8000
```

## Deploy na Railway

1. Wejdź na [railway.app](https://railway.app)
2. Kliknij **New Project** → **Deploy from GitHub repo**
3. Wybierz to repozytorium
4. Railway automatycznie wykryje Procfile i uruchomi aplikację
5. Kliknij **Generate Domain** żeby dostać publiczny URL

## Struktura projektu

```
osint-platform/
├── backend/
│   ├── main.py              # Główna aplikacja FastAPI
│   ├── requirements.txt     # Biblioteki Python
│   └── modules/
│       ├── name_search.py   # Moduł imię/nazwisko
│       ├── email_search.py  # Moduł email
│       ├── phone_search.py  # Moduł telefon
│       └── image_search.py  # Moduł zdjęcie
├── frontend/
│   └── index.html           # Interfejs użytkownika
├── Procfile                 # Konfiguracja Railway
└── railway.toml             # Ustawienia Railway
```

## ⚠️ Disclaimer

Narzędzie przeznaczone wyłącznie do celów edukacyjnych i OSINT na własnych danych lub za zgodą osoby. Nie używaj do nielegalnego śledzenia innych osób.
