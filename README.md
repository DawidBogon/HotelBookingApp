# HotelBookingApp

## 1. Instalation
Install PostgresSQL: https://www.postgresql.org/download/

Install Python 3.x: https://www.python.org/downloads/

Install make:

- Linux: apt / other package manager
- Windows: https://gnuwin32.sourceforge.net/packages/make.htm
- Mac: Brew

Install requirements with pip:

`pip install -r requirements.txt`


## 2. Running

Before first run, copy `.env.example` to `.env` and fine-tune the settings to match your environment:

- fill in your PostgresSQL credentials (starting with `DB_`)
- generate a unique secret key (e.g. from https://www.uuidgenerator.net/) and save it as `APP_SECRET`

Before first run create empty database according to .env variables (`DB_NAME_USER`, `DB_NAME_ACCESS_POINT`, `DB_NAME_HOTEL`)

Then, run `make start`. Note: all commands starting with `make` must be run from the root catalogue of this project (the one in which `Makefile` resides in).


## 3. Multiple flask instances on 1 PC
Three classes with applications are created: websiteUser, websiteAccessPoint and websiteHotel. Applications are running on different ports