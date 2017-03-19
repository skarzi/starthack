import json
<< << << < HEAD
== == == =
from datetime import datetime
from urllib.parse import (
    urlencode,
    urljoin,
)
>> >> >> > feature / widgets

import requests
from flask import (
    abort,
    Flask,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
)
from requests.auth import HTTPBasicAuth

<< << << < HEAD
from yelp import get_categories_tree, get_places
== == == =
from TransactionHistory import TransactionHistory
from data_provider import DataProvider
from forms import FlightForm
from open_weather_map_facade import OpenWeatherMapFacade
from skyscanner_live_pricing import LivePricing
>> >> >> > feature / widgets

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
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

<< << << < HEAD
return render_template("index.html",
       == == ===
form = FlightForm()
return render_template("index.html", form=form,
       >> >> >> > feature / widgets
authenticated = ("user_token" in session))


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
    if response.status_code == 200:
        return response.text
    return response.text


@app.route('/static/<file>')
def serve_static(file):
    return send_from_directory("static", file)


@app.route('/categories_places', methods=['GET'])
def categories():
    return json.dumps(get_categories_tree())


@app.route('/attractions/<city>/<category>', methods=['GET'])
def attractions(city, category):
    print(city, category)
    return json.dumps(get_places(city))


@app.route('/results', methods=["POST"])
def results():
    form = FlightForm()
    if form.validate_on_submit():
        from_ = form.from_.data
        to_ = form.to_.data
        departure_dt = datetime.strptime(form.departure_.data,
                                         "%d %B, %Y").date()
        return_dt = datetime.strptime(form.return_.data, "%d %B, %Y").date()
        print(
            "New request: {from_} -> {to_} / {departure_dt} to {return_dt}".format(
                **locals())
        )
        transaction_history = TransactionHistory(
            json.loads(proxy_dbapi_request("transactions"))
        )

        # weather
        weather_data = OpenWeatherMapFacade().get_weather(
            to_, departure_dt, return_dt)

        # flights
        try:
            flights = LivePricing(
                DataProvider.get_suggestions(from_)[0]['code'].split('-')[0],
                DataProvider.get_suggestions(to_)[0]['code'].split('-')[0],
                departure_dt, return_dt, 1
            ).find_flights()
        except Exception:
            flights = []
        else:
            flights = transaction_history.sort_recommendations(
                flights, lambda x: x["InboundDetails"]["Carriers"][0][0])
            flights = flights[:5]

        # # accomodation
        # places = AirBNBService().search(
        #     to_, departure_dt, return_dt, items_per_grid=6)

        return render_template(
            'widgets.html', weather_data=weather_data, flights=flights,
            places=[]
        )
    abort(400)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Development Server Help')
    parser.add_argument("-d", "--debug", action="store_true", dest="debug_mode",
                        help="run in debug mode (for use with PyCharm)",
                        default=False)
    parser.add_argument("-p", "--port", dest="port",
                        help="port of server (default:%(default)s)", type=int,
                        default=5000)

    cmd_args = parser.parse_args()
    app_options = {"port": cmd_args.port}

    if cmd_args.debug_mode:
        app_options["debug"] = True
        app_options["use_debugger"] = False
        app_options["use_reloader"] = False

    app.run(**app_options)
