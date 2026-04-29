from flask import Flask, jsonify
import os
import json
import socket
import redis

app = Flask(__name__)

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    decode_responses=True
)

@app.route("/health")
def health():
    return jsonify({
        "service": "viewer",
        "status": "ok",
        "hostname": socket.gethostname()
    })

@app.route("/status")
def status():
    return jsonify({
        "viewer_hostname": socket.gethostname(),
        "queue_size": r.llen("tasks"),
        "results_size": r.llen("results")
    })

@app.route("/results")
def results():
    raw_items = r.lrange("results", 0, 20)
    items = [json.loads(item) for item in raw_items]
    return jsonify({
        "viewer_hostname": socket.gethostname(),
        "items": items
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
