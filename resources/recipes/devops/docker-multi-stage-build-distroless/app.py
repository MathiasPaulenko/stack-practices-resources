from flask import Flask

app = Flask(__name__)


@app.route("/health")
def health():
    return "ok"


@app.route("/")
def index():
    return "hello from multi-stage python\n"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
