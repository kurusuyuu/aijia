from flask import Flask

from App.house_views import house_blue
from utils.settings import templates_dir,static_dir
from App.user_views import user_blue
from utils.functions import init_ext
from App.order_views import order_blue


def create_app(config):
    app = Flask(__name__,
                template_folder=templates_dir,
                static_folder=static_dir)
    app.register_blueprint(blueprint=user_blue, url_prefix='/user')
    app.register_blueprint(blueprint=house_blue, url_prefix='/house')
    app.register_blueprint(blueprint=order_blue, url_prefix='/order')


    app.config.from_object(config)
    init_ext(app)

    return app