"""
OAuth 2.0 login with Google — Flask + Authlib.

Setup:
    pip install flask authlib requests
    export FLASK_SECRET_KEY=<random-secret>
    export GOOGLE_CLIENT_ID=<your-client-id>
    export GOOGLE_CLIENT_SECRET=<your-client-secret>

Register http://localhost:5000/callback as an authorized redirect URI
in Google Cloud Console, then run: python flask_app.py
"""

import os
from flask import Flask, redirect, session, url_for
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET_KEY"]
oauth = OAuth(app)

google = oauth.register(
    name="google",
    client_id=os.environ["GOOGLE_CLIENT_ID"],
    client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
    access_token_url="https://oauth2.googleapis.com/token",
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    api_base_url="https://www.googleapis.com/oauth2/v1/",
    client_kwargs={"scope": "openid email profile"},
)


@app.route("/")
def index():
    user = session.get("user")
    return f"Hello, {user['email']}!" if user else '<a href="/login">Sign in with Google</a>'


@app.route("/login")
def login():
    redirect_uri = url_for("callback", _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route("/callback")
def callback():
    token = google.authorize_access_token()
    user = google.get("userinfo").json()
    session["user"] = user
    return redirect("/")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
