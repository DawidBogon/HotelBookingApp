# HotelBookingApp

## 1. Running

Before first run, copy `.env.example` to `.env` and fine-tune the settings to match your environment:

- fill in your PostgreSQL credentials (starting with `DB_`)
- generate a unique secret key (e.g. from https://www.uuidgenerator.net/) and save it as `APP_SECRET`

Then, run `make start`. Note: all commands starting with `make` must be run from the root catalogue of this project (the one in which `Makefile` resides in).