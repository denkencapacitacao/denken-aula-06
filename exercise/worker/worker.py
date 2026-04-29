import os
import json
import time
import socket
import random
import redis

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    decode_responses=True
)

hostname = socket.gethostname()
print(f"[worker] started on {hostname}", flush=True)

while True:
    item = r.brpop("tasks", timeout=5)
    if not item:
        continue

    _, raw_task = item
    task = json.loads(raw_task)
    value = int(task.get("value", 0))
    multiplier = random.randint(2, 10)
    result = value * multiplier

    time.sleep(float(os.getenv("PROCESSING_DELAY", "1")))

    output = {
        "input": value,
        "multiplier": multiplier,
        "result": result,
        "worker_hostname": hostname,
        "processed_at": time.time()
    }

    r.lpush("results", json.dumps(output))
    r.ltrim("results", 0, 49)

    print(f"[worker] processed value={value} result={result}", flush=True)
