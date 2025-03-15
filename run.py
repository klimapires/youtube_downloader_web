from app import app, socketio
import eventlet
from app.controllers.main_controller import main_controller

app.register_blueprint(main_controller)

if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)