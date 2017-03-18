from urllib.parse import urlencode, urljoin

import requests
from flask import abort, Flask, session, redirect, request
from flask import render_template
from flask import send_from_directory
from requests.auth import HTTPBasicAuth

# App config
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# api location
DB_AUTH_URL = "https://simulator-api.db.com/gw/oidc/"
DB_API_URL = "https://simulator-api.db.com/gw/dbapi/v1/"

# App credentials
CLIENT_ID = '58e85c4c-6837-4897-8891-9cf918bc911c'
CLIENT_SECRET = 'ALQgPOTyYtRdZRKnuWsa8v0hr2WNz_ZvBw_9KfqwdG7kBHlY766w9NRFtPoQvtPE2Vajgy3tUKvY1nbExUer6ag'

# Local settings (change this or add import from other file!)
SERVER_HOST = 'http://8426b9ab.ngrok.io'
REDIRECT_URI = urljoin(SERVER_HOST, "authenticated")
app.secret_key = "A0Zr98j/3yX R~XHH!jmN]LWX/,?RT"  # totally random, straight outta flask docs


def create_api_url(endpoint, params=None, auth_endpoint=False):
    """ return encoded url. Use DB API Auth endpoints if auth = True"""
    url = urljoin(DB_AUTH_URL if auth_endpoint else DB_API_URL, endpoint)
    if params:
        encoded_params = urlencode(params)
        url = "{}?{}".format(url, encoded_params)
    return url


@app.route('/')
def home():
    """
    if user is not authenticated redirect to login page, in other case
    render standard template with main form
     """
    return render_template("index.html", authenticated=("user_token" in session))


@app.route("/authenticate")
def choose_auth_method():
    """ allow user choosing between OAuth providers """
    return render_template("auth.html")


@app.route('/authenticate/db')
def authenticate_with_db():
    """ begin DB OAuth flow """
    url = create_api_url("authorize", {
        "response_type": "code", "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID, "state": SERVER_HOST}, auth_endpoint=True)
    return redirect(url)


@app.route('/authenticated')
def get_token():
    """ get token from api and store it in user's session """
    if not "code" in request.args:
        abort(400)

    code_ = request.args.get('code')
    response = requests.post(
        create_api_url("token", {
            "grant_type": "authorization_code", "code": code_,
            "redirect_uri": REDIRECT_URI
        }, auth_endpoint=True), auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET))
    session["user_token"] = response.json()['access_token']
    return redirect("/")


@app.route('/dbapi/<data>', methods=['GET'])
def proxy_dbapi_request(data):
    """ proxy request to DB API signing it with user's token """
    if not "user_token" in session:
        abort(403)

    response = requests.get(create_api_url(data), headers={
        "Authorization": "Bearer {}".format(session["user_token"])})
    print(session["user_token"])
    if response.status_code == 200:
        return response.text
    return response.text


@app.route('/static/<file>')
def serve_static(file):
    return send_from_directory("static", file)


if __name__ == '__main__':
    app.run()
