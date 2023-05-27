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

    class User(db.Model, UserMixin):
        __tablename__ = "users"
        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(255), unique=True)
        login = db.Column(db.String(255), unique=True)
        password = db.Column(db.String(255))
        first_name = db.Column(db.String(255))
        last_name = db.Column(db.String(255))
        role = db.Column(db.Integer)

    return TestTable, User


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

    class Hotel(db.Model):
        __tablename__ = "hotels"
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(255))
        api_endpoint = db.Column(db.String(255))
        number_of_rooms = db.Column(db.Integer)
        city = db.Column(db.String(255))
        address = db.Column(db.String(255))
        rating = db.Column(db.Float)

    class Room(db.Model):
        __tablename__ = "rooms"
        id = db.Column(db.Integer, primary_key=True)
        hotel = db.Column(db.Integer, db.ForeignKey("hotels.id"))
        size = db.Column(db.Integer)
        image = db.Column(db.Text)
        mimetype = db.Column(db.String(255))
        number_of_beds = db.Column(db.Integer)
        additionals = db.Column(db.String(255))
        price = db.Column(db.Float)

    return User, Role, Hotel, Room


def createHotelTables(db):
    class Room(db.Model):
        __tablename__ = "rooms"
        id = db.Column(db.Integer, primary_key=True)
        size = db.Column(db.Integer)
        number_of_beds = db.Column(db.Integer)
        additonals = db.Column(db.String(255))
        price = db.Column(db.Float)

    class Transaction(db.Model):
        __tablename__ = "transactions"
        id = db.Column(db.Integer, primary_key=True)
        user = db.Column(db.Integer)
        room = db.Column(db.Integer, db.ForeignKey("rooms.id"))
        expire_time = db.Column(db.DateTime)
        completed = db.Column(db.Boolean)
        is_logged_in = db.Column(db.Boolean)

    class RoomImage(db.Model):
        __tablename__ = "room_images"
        id = db.Column(db.Integer, primary_key=True)
        room = db.Column(db.Integer, db.ForeignKey("rooms.id"))
        image = db.Column(db.Text)
        mimetype = db.Column(db.String(255))

    class Reservation(db.Model):
        __tablename__ = "reservations"
        id = db.Column(db.Integer, primary_key=True)
        transaction = db.Column(db.Integer, db.ForeignKey("transactions.id"))
        reservation_start = db.Column(db.DateTime)
        reservation_end = db.Column(db.DateTime)
        reservation_time = db.Column(db.DateTime(timezone=True), default=func.now())
        canceled = db.Column(db.Boolean)

    return Room, Transaction, RoomImage, Reservation
