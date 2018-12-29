from flask_app import app
from flask_app import socketio

if __name__ == '__main__':
    socketio.run(app, debug=True)
