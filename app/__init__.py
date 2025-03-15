from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__, template_folder="views/templates")
socketio = SocketIO(app, cors_allowed_origins="*")

from app.controllers.main_controller import main_controller
app.register_blueprint(main_controller)
