from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text, Boolean
from sqlalchemy import create_engine
import dotenv
import os


dotenv.load_dotenv('./.env')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
db_string = "postgresql://" + str(DB_USER) + ":" + str(DB_PASSWORD) + "@" + str(DB_HOST) + ":" + str(DB_PORT) + "/" + str(DB_NAME)
engine = create_engine(db_string)
Base = declarative_base()


# Access point tables
class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    api_endpoint = Column(String(255))
    number_of_rooms = Column(Integer)
    city = Column(String(255))
    address = Column(String(255))
    rating = Column(Float)


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    hotel = Column(Integer, ForeignKey("hotels.id"))
    size = Column(Integer)
    image = Column(Text)
    mimetype = Column(String(255))
    number_of_beds = Column(Integer)
    additionals = Column(String(255))
    price = Column(Float)


# Hotel tables
class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    role = Column(String(255))


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    login = Column(String(255))
    password = Column(String(255))


class UserRole(Base):
    __tablename__ = "user_roles"
    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey("users.id"))
    role = Column(Integer, ForeignKey("roles.id"))


class RoomH(Base):
    __tablename__ = "rooms_h"

    id = Column(Integer, primary_key=True)
    size = Column(Integer)
    number_of_beds = Column(Integer)
    additonals = Column(String(255))
    price = Column(Float)


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey("users.id"))
    room = Column(Integer, ForeignKey("rooms_h.id"))
    expire_time = Column(DateTime)
    completed = Column(Boolean)
    is_logged_in = Column(Boolean)


class RoomImage(Base):
    __tablename__ = "room_images"

    id = Column(Integer, primary_key=True)
    room = Column(Integer, ForeignKey("rooms_h.id"))
    image = Column(Text)
    mimetype = Column(String(255))


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey("users.id"))
    transaction = Column(Integer, ForeignKey("transactions.id"))
    reservation_start = Column(DateTime)
    reservation_end = Column(DateTime)
    canceled = Column(Boolean)


Base.metadata.create_all(engine)
