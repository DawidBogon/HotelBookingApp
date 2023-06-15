from .website import WebsiteUser, WebsiteAccessPoint, WebsiteHotel
from .website.views import views
from .website.auth import auth
from .website.hotel import construct_blueprint #import hotel
import os
import threading
from .website.access_point import access_point
import pandas as pd


if __name__ == '__main__':
    website = WebsiteUser()
    website_access_point = WebsiteAccessPoint()
    website_hotel1 = WebsiteHotel(db_name=os.environ["DB_NAME_HOTEL"])
    website_hotel2 = WebsiteHotel(db_name=os.environ["DB_NAME_HOTEL2"])

    website.app.register_blueprint(views, url_prefix='/')
    website.app.register_blueprint(auth, url_prefix='/')
    website_access_point.app.register_blueprint(access_point, url_prefix='/')
    website_hotel1.app.register_blueprint(construct_blueprint(website_hotel1, 'hotel1'), url_prefix='/')
    website_hotel2.app.register_blueprint(construct_blueprint(website_hotel2, 'hotel2'), url_prefix='/')

    def flask1():
        website.app.run(host="0.0.0.0", debug=(os.environ["APP_DEBUG"]).lower() == "true",
                        port=int(os.environ["APP_PORT"]), use_reloader=False)

    def flask2():
        website_access_point.app.run(host="0.0.0.0", debug=(os.environ["APP_DEBUG"]).lower() == "true",
                                     port=int(os.environ["APP_PORT"])+1, use_reloader=False)

    def flask3():
        website_hotel1.app.run(host="0.0.0.0", debug=(os.environ["APP_DEBUG"]).lower() == "true",
                              port=int(os.environ["APP_PORT"])+2, use_reloader=False)

    def flask4():
        website_hotel2.app.run(host="0.0.0.0", debug=(os.environ["APP_DEBUG"]).lower() == "true",
                               port=int(os.environ["APP_PORT"]) + 3, use_reloader=False)

    t1 = threading.Thread(target=flask1, daemon=True)

    t2 = threading.Thread(target=flask2, daemon=True)

    t3 = threading.Thread(target=flask3, daemon=True)

    t4 = threading.Thread(target=flask4, daemon=True)

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    while True:
        pass

