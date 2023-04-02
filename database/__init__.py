#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import Column, Integer, String, func


def createTestTable(db):
    class TestTable(db.Model):
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        data = db.Column(db.String(10000))
        date = db.Column(db.DateTime(timezone=True), default=func.now())

    return TestTable
