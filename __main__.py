from website import WebsiteUser, WebsiteAccessPoint, WebsiteHotel
from website.views import views
from website.auth import auth
import os
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

if __name__ == '__main__':
    website = WebsiteUser()
    website_access_point = WebsiteAccessPoint()
    website_hotel = WebsiteHotel()

    website.app.register_blueprint(views, url_prefix='/')
    website.app.register_blueprint(auth, url_prefix='/')

    application = DispatcherMiddleware(website.app, {
        '/access_point': website_access_point.app,
        '/hotel': website_hotel.app
        })
    run_simple(hostname="0.0.0.0", application=application, use_debugger=(os.environ["APP_DEBUG"]).lower() == "true", port=int(os.environ["APP_PORT"]))
