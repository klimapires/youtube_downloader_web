from flask import Flask

app = Flask(__name__, template_folder="views/templates")

from app.controllers.main_controller import main_controller

app.register_blueprint(main_controller)