import os
import threading
import time

import schedule
import requests
from sqlalchemy import table

from .website import WebsiteUser, WebsiteAccessPoint, WebsiteHotel
from .website.access_point import access_point
from .website.auth import auth
from .website.hotel import hotel
from .website.views import views

if __name__ == '__main__':
    website = WebsiteUser()
    website_access_point = WebsiteAccessPoint()
    website_hotel = WebsiteHotel()

    website.app.register_blueprint(views, url_prefix='/')
    website.app.register_blueprint(auth, url_prefix='/')
    website_access_point.app.register_blueprint(access_point, url_prefix='/')
    website_hotel.app.register_blueprint(hotel, url_prefix='/')

    def flask1():
        website.app.run(host="0.0.0.0", debug=(os.environ["APP_DEBUG"]).lower() == "true",
                        port=int(os.environ["APP_PORT"]), use_reloader=False)

    def flask2():
        website_access_point.app.run(host="0.0.0.0", debug=(os.environ["APP_DEBUG"]).lower() == "true",
                                     port=int(os.environ["APP_PORT"])+1, use_reloader=False)

    def flask3():
        website_hotel.app.run(host="0.0.0.0", debug=(os.environ["APP_DEBUG"]).lower() == "true",
                              port=int(os.environ["APP_PORT"])+2, use_reloader=False)

    def access_point_update_service():
        hotels = website_access_point.HotelData.query.all()
        for hotel in hotels:
            hotel_dict = hotel.return_table()
            endpoint = hotel_dict['api_endpoint']
            res = requests.get(endpoint + '/get_all_rooms')
            if res.status_code == 200:
                res_json = res.json()
                website_access_point.Room.query.delete().where(website_access_point.Room.api_endpoint == endpoint)
                for room in res_json['result']:
                    room_id = room['id']
                    del room['id']
                    hotel_dict['api_endpoint'] += '/' + room_id
                    website_access_point.Room.query.insert().values(hotel_dict | room)


    schedule.every(10).minutes.do(access_point_update_service)

    t1 = threading.Thread(target=flask1, daemon=True)

    t2 = threading.Thread(target=flask2, daemon=True)

    t3 = threading.Thread(target=flask3, daemon=True)

    t1.start()
    t2.start()
    t3.start()

    while True:
        schedule.run_pending()
        time.clock(1)

