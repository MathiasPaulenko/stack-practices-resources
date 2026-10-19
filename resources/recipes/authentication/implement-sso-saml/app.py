"""SAML 2.0 Service Provider demo built on Flask + python3-saml.

Endpoints:
    GET  /saml/login     -> redirect to the IdP with an AuthnRequest
    POST /saml/acs       -> consume the signed SAMLResponse, create session
    GET  /saml/sls       -> process Single Logout responses from the IdP
    GET  /saml/metadata  -> SP metadata XML to register with the IdP
    GET  /dashboard      -> protected page, requires a SAML session

Configure the IdP/SP values in saml_settings.json and export SECRET_KEY.
"""

import json
import os
from urllib.parse import urlparse

from flask import Flask, redirect, request, session
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.settings import OneLogin_Saml2_Settings

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]

# The ACS is a cross-site POST from the IdP, so the session cookie needs it.
app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.config["SESSION_COOKIE_SECURE"] = True

SETTINGS_PATH = os.path.join(os.path.dirname(__file__), "saml_settings.json")
with open(SETTINGS_PATH, encoding="utf-8") as f:
    SAML_CONFIG = json.load(f)


def init_saml_auth(req):
    return OneLogin_Saml2_Auth(req, SAML_CONFIG)


def prepare_flask_request():
    return {
        "https": "on" if request.is_secure else "off",
        "http_host": request.host,
        "script_name": request.path,
        "server_port": request.environ.get("SERVER_PORT"),
        "get_data": request.args.copy(),
        "post_data": request.form.copy(),
    }


@app.route("/")
def index():
    if "saml_user" in session:
        return redirect("/dashboard")
    return '<a href="/saml/login">Log in with SSO</a>'


@app.route("/saml/login")
def saml_login():
    auth = init_saml_auth(prepare_flask_request())
    # RelayState is echoed back to the ACS; use it for deep links.
    return_to = request.args.get("next", "/dashboard")
    return redirect(auth.login(return_to=return_to))


@app.route("/saml/acs", methods=["POST"])
def saml_acs():
    auth = init_saml_auth(prepare_flask_request())
    auth.process_response()

    errors = auth.get_errors()
    if errors:
        app.logger.error("SAML errors: %s", errors)
        return "Authentication failed", 401
    if not auth.is_authenticated():
        return "Not authenticated", 401

    # Store the session index: SLO needs it to end the IdP session.
    session["saml_user"] = {
        "email": auth.get_nameid(),
        "attributes": auth.get_attributes(),
        "session_index": auth.get_session_index(),
    }

    # RelayState carries the originally requested URL; fall back to /dashboard.
    return_to = request.form.get("RelayState", "/dashboard")
    if urlparse(return_to).netloc or not return_to.startswith("/"):
        return_to = "/dashboard"  # never redirect to an external URL
    return redirect(return_to)


@app.route("/saml/sls")
def saml_sls():
    auth = init_saml_auth(prepare_flask_request())
    url = auth.process_slo(delete_session_cb=lambda: session.clear())
    errors = auth.get_errors()
    if errors:
        app.logger.error("SLO errors: %s", errors)
        return "Logout failed", 500
    return redirect(url or "/")


@app.route("/saml/metadata")
def saml_metadata():
    settings = OneLogin_Saml2_Settings(SAML_CONFIG, sp_validation_only=True)
    metadata = settings.get_sp_metadata()
    errors = settings.validate_metadata(metadata)
    if errors:
        return f"Invalid SP metadata: {errors}", 500
    return metadata, 200, {"Content-Type": "application/samlmetadata+xml"}


@app.route("/dashboard")
def dashboard():
    if "saml_user" not in session:
        return redirect("/saml/login")
    user = session["saml_user"]
    return (
        f"<h1>Welcome {user['email']}</h1>"
        f"<pre>{user['attributes']}</pre>"
        '<a href="/saml/logout">Log out</a>'
    )


if __name__ == "__main__":
    app.run(ssl_context="adhoc")  # IdPs reject plain-HTTP ACS URLs
