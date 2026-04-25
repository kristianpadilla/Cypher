from flask import Flask, render_template
from flask_socketio import SocketIO
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cypher_secret'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

ui_state = {
    "status": "standby",
    "user_text": "",
    "cypher_text": "",
}

def set_ui_state(status=None, user_text=None, cypher_text=None):
    """Call this from main.py to push updates to the UI instantly."""
    if status is not None:
        ui_state["status"] = status
    if user_text is not None:
        ui_state["user_text"] = user_text
    if cypher_text is not None:
        ui_state["cypher_text"] = cypher_text
    socketio.emit('state_update', ui_state)

@app.route("/")
def index():
    return render_template("cypher.html")

def run_ui():
    socketio.run(app, port=5000, debug=False, use_reloader=False, allow_unsafe_werkzeug=True)

def start_ui():
    t = threading.Thread(target=run_ui, daemon=True)
    t.start()
    print("Cypher UI running at http://localhost:5000")

if __name__ == "__main__":
    print("Cypher UI running at http://localhost:5000")
    socketio.run(app, port=5000, debug=False, allow_unsafe_werkzeug=True)
