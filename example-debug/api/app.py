from flask import Flask
import socket
import os

app = Flask(__name__)

@app.route("/")
def home():
    return {
        "hostname": socket.gethostname(),
        "message": "Hello from Swarm",
        "pid": os.getpid()
    }

@app.route("/health")
def health():
    return {"status": "ok"}

app.run(host="0.0.0.0", port=5000)
