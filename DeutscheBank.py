import json

import requests
from flask import Flask, redirect, request
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

client_id = '58e85c4c-6837-4897-8891-9cf918bc911c'
client_secret = 'ALQgPOTyYtRdZRKnuWsa8v0hr2WNz_ZvBw_9KfqwdG7kBHlY766w9NRFtPoQvtPE2Vajgy3tUKvY1nbExUer6ag'
state = 'http://7bfeba68.ngrok.io'
redirect_uri = 'http://7bfeba68.ngrok.io/token'

user_token = None


@app.route('/')
def login():
    url = 'https://simulator-api.db.com/gw/oidc/authorize?response_type=code&redirect_uri={}&client_id={}&state={}'
    # response = requests.get(url.format(client_id, redirect_uri))
    return redirect(url.format(redirect_uri, client_id, state))


@app.route('/token')
def token():
    if 'code' in request.args and 'state' in request.args:
        code_ = request.args.get('code')
        state_ = request.args.get('state')
        print(code_, state_)
        r = requests.post(
            'https://simulator-api.db.com/gw/oidc/token?grant_type=authorization_code&code={}&redirect_uri={}'.format(
                code_, redirect_uri
            ),
            auth=HTTPBasicAuth(client_id, client_secret))
        token = r.json()['access_token']
        global user_token
        user_token = token
        return user_token


@app.route('/<data>', methods=['GET'])
def balance(data):
    if user_token:
        r = requests.get(
            'https://simulator-api.db.com/gw/dbapi/v1/{}'.format(data),
            headers={"Authorization": "Bearer {}".format(user_token)})
        if r.status_code == 200:
            return json.dumps(r.json())
        else:
            return json.dumps(r.status_code)


if __name__ == '__main__':
    app.run()
