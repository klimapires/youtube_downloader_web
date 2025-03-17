from app import app, socketio
import eventlet

if __name__ == '__main__':
    eventlet.monkey_patch()  # Garante compatibilidade com eventlet
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
