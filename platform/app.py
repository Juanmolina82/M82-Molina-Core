from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os, json
from datetime import datetime
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET", "m82-dev")
STATE_FILE = "data/m82_state.json"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f: return json.load(f)
    return {"strait": "Hormuz", "traffic_24h": 0, "engine_status": "INIT", "timestamp": ""}

def save_state(data):
    os.makedirs("data", exist_ok=True)
    with open(STATE_FILE, 'w') as f: json.dump(data, f)

@app.route('/api/v1/update_metrics', methods=['POST'])
def update_metrics():
    data = request.json
    if data.get("debug_pin") != os.getenv("M82_DEBUG_PIN"): return {"error": "Unauthorized"}, 401
    save_state(data)
    return {"status": "ok", "lynx": "synced"}

@app.route('/api/v1/engine_status', methods=['GET'])
def engine_status():
    return jsonify(load_state())

@app.route('/health', methods=['GET'])
def health(): return {"status": "green", "vault": "M82", "time": datetime.utcnow().isoformat()}

@app.route('/')
def index():
    s = load_state()
    return f"""
    <h1>M82 Lynx Dashboard</h1>
    <h2>Hormuz: {s['traffic_24h']} VLCC/d</h2>
    <h2>Status: {s['engine_status']}</h2>
    <h3>Last Update: {s['timestamp']}</h3>
    <p>PIN: {os.getenv('M82_DEBUG_PIN')}</p>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
