from flask import Flask, request, jsonify
import os
import socket
import json
import time
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
        "service": "api",
        "status": "ok",
        "hostname": socket.gethostname()
    })

@app.route("/task", methods=["POST"])
def create_task():
    payload = request.get_json(force=True)
    task = {
        "value": payload.get("value"),
        "created_at": time.time(),
        "created_by": socket.gethostname()
    }
    r.lpush("tasks", json.dumps(task))
    return jsonify({
        "status": "queued",
        "task": task,
        "api_hostname": socket.gethostname()
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
