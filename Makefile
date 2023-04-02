.PHONY: docs start
.DEFAULT: help

help:
	@echo "Commands available: help, start"


start:
	@cd .. && python -m HotelBookingApp
