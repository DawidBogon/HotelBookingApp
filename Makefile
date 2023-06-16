.PHONY: docs start create_db
.DEFAULT: help

help:
	@echo "Commands available: help, start"


start:
	@cd .. && python -m HotelBookingApp
