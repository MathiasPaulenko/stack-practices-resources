import redis
import json
from queue import Queue
from flask import Flask, Response

app = Flask(__name__)
r = redis.Redis(host="localhost", port=6379)
clients = []


@app.route("/events")
def events():
    q = Queue()
    clients.append(q)

    def generate():
        try:
            while True:
                msg = q.get()
                yield f"data: {json.dumps(msg)}\n\n"
        finally:
            clients.remove(q)

    return Response(generate(), mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@app.route("/publish/<channel>/<message>")
def publish(channel, message):
    r.publish(channel, json.dumps({"msg": message}))
    return {"published": True}


def subscribe_channel(channel):
    pubsub = r.pubsub()
    pubsub.subscribe(channel)
    for message in pubsub.listen():
        if message["type"] == "message":
            data = json.loads(message["data"])
            for q in list(clients):
                q.put(data)


if __name__ == "__main__":
    import threading
    thread = threading.Thread(target=subscribe_channel, args=("sse-broadcast",), daemon=True)
    thread.start()
    app.run(host="0.0.0.0", port=5000, threaded=True)
