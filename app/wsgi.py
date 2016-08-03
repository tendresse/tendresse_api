#! /usr/bin/env python
import os
from flask_socketio import SocketIO
from app import create_app

app = create_app(os.getenv('APP_CONFIG', 'default'))
socketio = SocketIO(app)
if __name__ == '__main__':
    socketio.run(app)