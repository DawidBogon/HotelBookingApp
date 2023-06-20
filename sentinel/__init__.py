import requests
from sqlalchemy import Column, Integer, String, Text, Float
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine, delete
import os
from sqlalchemy.sql import text

Base = declarative_base()


class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True)
    hotel_name = Column(String(255))
    size = Column(Integer)
    number_of_beds = Column(Integer)
    additionals = Column(String(255))
    price = Column(Float)
    rating = Column(Float)
    api_endpoint = Column(String(255))
    city = Column(String(255))
    address = Column(String(255))


class HotelData(Base):
    __tablename__ = "hotel_datas"
    id = Column(Integer, primary_key=True)
    rating = Column(Float)
    api_endpoint = Column(String(255))
    city = Column(String(255))
    address = Column(String(255))
    hotel_name = Column(String(255))

    def return_table(self):
        return dict(id=self.id, rating=self.rating, api_endpoint=self.api_endpoint, city=self.city, address=self.address, hotel_name=self.hotel_name)


def access_point_update_service():
    engine = create_engine(f'postgresql://{os.environ["DB_USER"]}:{os.environ["DB_PASSWORD"]}@{os.environ["DB_HOST"]}:{os.environ["DB_PORT"]}/{os.environ["DB_NAME_ACCESS_POINT"]}')
    Session = sessionmaker(bind=engine)
    session = Session()
    session.execute(text('LOCK TABLE rooms IN EXCLUSIVE MODE;'))
    hotels = session.query(HotelData).all()
    for hotel in hotels:
        hotel_dict = hotel.return_table()
        endpoint = hotel_dict['api_endpoint']
        res = requests.get(endpoint + '/get_all_rooms')
        if res.status_code == 200:
            res_json = res.json()
            delete_stmt = delete(Room).where(Room.hotel_name == hotel_dict['hotel_name'])
            session.execute(delete_stmt)
            for room in res_json['res']:
                room_id = room['id']
                hotel_dict['api_endpoint'] = endpoint + '/' + str(room_id)
                hotel_dict.update(room)
                del hotel_dict['id']
                room = Room(**hotel_dict)
                session.add(room)
    session.commit()
    session.close()
