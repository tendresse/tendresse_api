from flask import Flask
from flask_socketio import SocketIO
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import os, logging, sys, uuid

db = SQLAlchemy()
ma = Marshmallow()
socketio = SocketIO()

def create_app(debug=False):
    """Create an application."""
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY',str(uuid.uuid4()))
    app.config['IONIC_API_TOKEN'] = os.environ.get('IONIC_API_TOKEN','')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URI'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    ma.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    socketio.init_app(app)
    return app

