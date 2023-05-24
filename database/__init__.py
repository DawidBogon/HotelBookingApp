#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, func


def createTestTable(db):
    class TestTable(db.Model):
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        data = db.Column(db.String(10000))
        date = db.Column(db.DateTime(timezone=True), default=func.now())

    return TestTable

def createUser(db):
    class User(db.Model,UserMixin):
        __tablename__ = "users"
        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(255), unique=True)
        login = db.Column(db.String(255), unique=True)
        password = db.Column(db.String(255))
        first_name = db.Column(db.String(255))
        last_name = db.Column(db.String(255))

    return User