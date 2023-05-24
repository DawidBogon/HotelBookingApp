#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_login import LoginManager

load_dotenv()
from ..database import *


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


class Website(metaclass=SingletonMeta):
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = os.environ["APP_SECRET"]
        self.app.config[
            'SQLALCHEMY_DATABASE_URI'] = f'postgresql://{os.environ["DB_USER"]}:{os.environ["DB_PASSWORD"]}@{os.environ["DB_HOST"]}:{os.environ["DB_PORT"]}/{os.environ["DB_NAME"]}'

        self.db = SQLAlchemy(self.app)

        # register all models here
        self.TestTable = createTestTable(self.db)
        self.User = createUser(self.db)
        self.login_manager = LoginManager()
        self.login_manager.login_view = 'auth.login'
        self.login_manager.init_app(self.app)

        with self.app.app_context():
            self.db.create_all()
            print('Database schema has been synchronized')
