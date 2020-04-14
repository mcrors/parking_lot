from flask import Flask
from config import configDict


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(configDict[config_name])
    configDict[config_name].init_app(app)

    from .car_bp import car_bp as car_blueprint
    app.register_blueprint(car_blueprint)

    return app
