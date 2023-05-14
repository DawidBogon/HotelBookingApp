.PHONY: docs start create_db
.DEFAULT: help

help:
	@echo "Commands available: help, start, create_db"


start:
	@cd .. && python -m HotelBookingApp


create_db:
	@python ./database/tables.py
