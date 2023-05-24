from .website import Website
from .website.views import views
from .website.auth import auth
import os

if __name__ == '__main__':
    website = Website()

    website.app.register_blueprint(views, url_prefix='/')
    website.app.register_blueprint(auth, url_prefix='/')

    website.app.run(host="0.0.0.0", debug=(os.environ["APP_DEBUG"]).lower() == "true", port=int(os.environ["APP_PORT"]))
