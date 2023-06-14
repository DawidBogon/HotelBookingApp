from .website import WebsiteUser, WebsiteAccessPoint, WebsiteHotel
from .website.views import views
from .website.auth import auth
from .website.hotel import hotel
import os
import threading
from .website.access_point import access_point

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

    t1 = threading.Thread(target=flask1, daemon=True)

    t2 = threading.Thread(target=flask2, daemon=True)

    t3 = threading.Thread(target=flask3, daemon=True)

    t1.start()
    t2.start()
    t3.start()

    while True:
        pass

