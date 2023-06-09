#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import func


def createUserTables(db):
    class TestTable(db.Model):
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        data = db.Column(db.String(10000))
        date = db.Column(db.DateTime(timezone=True), default=func.now())

    return TestTable


def createAccessPointTables(db):
    class User(db.Model, UserMixin):
        __tablename__ = "users"
        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(255), unique=True)
        login = db.Column(db.String(255), unique=True)
        password = db.Column(db.String(255))
        first_name = db.Column(db.String(255))
        last_name = db.Column(db.String(255))
        role = db.Column(db.Integer)

    class Role(db.Model):
        __tablename__ = "roles"
        id = db.Column(db.Integer, primary_key=True)
        role = db.Column(db.String(255))

    class Room(db.Model):
        __tablename__ = "rooms"
        id = db.Column(db.Integer, primary_key=True)
        hotel_name = db.Column(db.String(255))
        size = db.Column(db.Integer)
        number_of_beds = db.Column(db.Integer)
        additionals = db.Column(db.String(255))
        price = db.Column(db.Float)
        rating = db.Column(db.Float)
        api_endpoint = db.Column(db.String(255))
        city = db.Column(db.String(255))
        address = db.Column(db.String(255))

        def return_table(self):
            return dict(id=self.id, hotel_name=self.hotel_name, size=self.size, number_of_beds=self.number_of_beds, additionals=self.additionals,
                        price=self.price, rating=self.rating, api_endpoint=self.api_endpoint, city=self.city, address=self.address)

    class HotelData(db.Model):
        __tablename__ = "hotel_datas"
        id = db.Column(db.Integer, primary_key=True)
        rating = db.Column(db.Float)
        api_endpoint = db.Column(db.String(255))
        city = db.Column(db.String(255))
        address = db.Column(db.String(255))
        hotel_name = db.Column(db.String(255))

        def return_table(self):
            return dict(id=self.id, rating=self.rating, api_endpoint=self.api_endpoint, city=self.city, address=self.address, hotel_name=self.hotel_name)

    return User, Role, Room, HotelData


def createHotelTables(db):
    class Room(db.Model):
        __tablename__ = "rooms"
        id = db.Column(db.Integer, primary_key=True)
        size = db.Column(db.Integer)
        number_of_beds = db.Column(db.Integer)
        additionals = db.Column(db.String(255))
        price = db.Column(db.Float)

        def return_table(self):
            return dict(id=self.id, size=self.size, number_of_beds=self.number_of_beds, additionals=self.additionals,
                        price=self.price)

    class Reservation(db.Model):
        __tablename__ = "reservations"
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer)
        first_name = db.Column(db.String(255))
        last_name = db.Column(db.String(255))
        room = db.Column(db.Integer, db.ForeignKey("rooms.id"))
        reservation_start = db.Column(db.DateTime)
        reservation_end = db.Column(db.DateTime)
        reservation_time = db.Column(db.DateTime(timezone=True), default=func.now())
        canceled = db.Column(db.Boolean)

    return Room, Reservation
