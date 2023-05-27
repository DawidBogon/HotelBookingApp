# HotelBookingApp

## 1. Running

Before first run, copy `.env.example` to `.env` and fine-tune the settings to match your environment:

- fill in your PostgreSQL credentials (starting with `DB_`)
- generate a unique secret key (e.g. from https://www.uuidgenerator.net/) and save it as `APP_SECRET`

Then, run `make start`. Note: all commands starting with `make` must be run from the root catalogue of this project (the one in which `Makefile` resides in).


## 2. Uruchomienie 3 aplikacji flaska na 1 kompie
Tworzone są 3 klasy z aplikacjami websiteUser, websiteAccessPoint i websiteHotel. Jak definiujemy strony
definiujemy je dla danej klasy tak jak jest to obecnie robione dla klasy websiteUser. W tym aspekcie
tworzenia stron nic się nie zmienia. Jedynie base url zmienia się z "/" na "access_point/" dla access pointu
i na "hotel/" dla hotelu. Więc wszystkie strony access pointu będą dostępne pod url "http://127.0.0.1:5000/access_point/[endpoint]"
analogicznie do tego będą dostępne strony hotelowe jedynie zamiast access_point wurl będzie hotel