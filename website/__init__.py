#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..database import *
from flask_session import Session

load_dotenv()


class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class WebsiteUser(metaclass=SingletonMeta):
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = os.environ["APP_SECRET"]
        self.app.config[
            'SQLALCHEMY_DATABASE_URI'] = f'postgresql://{os.environ["DB_USER"]}:{os.environ["DB_PASSWORD"]}@{os.environ["DB_HOST"]}:{os.environ["DB_PORT"]}/{os.environ["DB_NAME_USER"]}'
        self.app.config["SESSION_PERMANENT"] = False
        self.app.config["SESSION_TYPE"] = "filesystem"
        Session(self.app)
        self.db = SQLAlchemy(self.app)

        # register all models here
        self.TestTable = createUserTables(self.db)
        # self.login_manager = LoginManager()
        # self.login_manager.login_view = 'auth.login'
        # self.login_manager.init_app(self.app)

        with self.app.app_context():
            self.db.create_all()
            print('Database schema has been synchronized')


class WebsiteAccessPoint(metaclass=SingletonMeta):
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = os.environ["APP_SECRET"]
        self.app.config[
            'SQLALCHEMY_DATABASE_URI'] = f'postgresql://{os.environ["DB_USER"]}:{os.environ["DB_PASSWORD"]}@{os.environ["DB_HOST"]}:{os.environ["DB_PORT"]}/{os.environ["DB_NAME_ACCESS_POINT"]}'
        self.db = SQLAlchemy(self.app)

        # register all models here
        self.User, self.Role, self.Room, self.HotelData = createAccessPointTables(self.db)
        self.login_manager = LoginManager()
        self.login_manager.login_view = 'http://localhost:5000/login'
        self.login_manager.init_app(self.app)

        with self.app.app_context():
            self.db.create_all()
            print('Database schema has been synchronized')


class WebsiteHotel(metaclass=SingletonMeta):
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = os.environ["APP_SECRET"]
        self.app.config[
            'SQLALCHEMY_DATABASE_URI'] = f'postgresql://{os.environ["DB_USER"]}:{os.environ["DB_PASSWORD"]}@{os.environ["DB_HOST"]}:{os.environ["DB_PORT"]}/{os.environ["DB_NAME_HOTEL"]}'
        self.db = SQLAlchemy(self.app)
        engine = create_engine(f'postgresql://{os.environ["DB_USER"]}:{os.environ["DB_PASSWORD"]}@{os.environ["DB_HOST"]}:{os.environ["DB_PORT"]}/{os.environ["DB_NAME_HOTEL"]}')
        self.Session = sessionmaker(bind=engine)
        # register all models here
        self.Room, self.Reservation = createHotelTables(self.db)
        self.login_manager = LoginManager()
        self.login_manager.login_view = 'auth.login'
        self.login_manager.init_app(self.app)

        with self.app.app_context():
            self.db.drop_all()
            self.db.create_all()
            self.set_initial_values()
            print('Database schema has been synchronized')

    def set_initial_values(self):
        if os.environ["DB_NAME_HOTEL"] == 'hotel':
            rooms = [(0, 20, 2, "czajnik,TV", 120),
                     (1, 20, 2, "czajnik,TV", 120),
                     (2, 20, 2, "czajnik,TV", 120),
                     (3, 23, 2, "czajnik,TV", 125),
                     (4, 23, 2, "czajnik,TV", 125),
                     (5, 23, 2, "czajnik,TV", 125),
                     (6, 23, 2, "czajnik,TV", 125),
                     (7, 35, 3, "czajnik,TV", 180),
                     (8, 35, 3, "czajnik,TV", 180),
                     (9, 35, 3, "czajnik,TV", 180),
                     (10, 40, 4, "czajnik,TV", 220),
                     (11, 40, 4, "czajnik,TV", 220),
                     (12, 40, 4, "czajnik,TV", 220),
                     (13, 40, 4, "czajnik,TV", 220),
                     (14, 120, 6, "czajnik,TV", 700),
                     (15, 60, 4, "czajnik,TV", 300),
                     (16, 25, 2, "czajnik,TV", 140),
                     (17, 25, 2, "czajnik,TV", 140)]
            try:
                for id, size, number_of_beds, additionals, price in rooms:
                    new_room = self.Room(id=id, size=size, number_of_beds=number_of_beds, additionals=additionals,
                                         price=price)
                    self.db.session.add(new_room)
                self.db.session.commit()
            except:
                pass
