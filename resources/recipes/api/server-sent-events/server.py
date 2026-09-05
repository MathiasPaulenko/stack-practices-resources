from flask import Flask, Response
import json
import time
from queue import Queue

app = Flask(__name__)
clients = []


@app.route("/events")
def events():
    def generate():
        counter = 0
        while True:
            counter += 1
            data = {"message": f"Update {counter}", "timestamp": time.time()}
            yield f"id: {counter}\ndata: {json.dumps(data)}\n\n"
            time.sleep(2)

    return Response(
        generate(),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.route("/broadcast")
def broadcast_stream():
    q = Queue()
    clients.append(q)

    def generate():
        try:
            while True:
                msg = q.get()
                yield f"data: {json.dumps(msg)}\n\n"
        finally:
            clients.remove(q)

    return Response(generate(), mimetype="text/event-stream")


@app.route("/publish/<message>")
def publish(message):
    for q in list(clients):
        q.put({"msg": message})
    return {"published": len(clients)}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
