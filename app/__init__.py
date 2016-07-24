from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_pushjack import FlaskAPNS, FlaskGCM
from config import config


db = SQLAlchemy()
ma = Marshmallow()
apns = FlaskAPNS()
gcm = FlaskGCM()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    ma.init_app(app)
    apns.init_app(app)
    gcm.init_app(app)

    from .api_v1 import api as api_v1_blueprint
    app.register_blueprint(api_v1_blueprint, url_prefix='/api/v1')

    return app
