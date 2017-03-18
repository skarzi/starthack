import time
from datetime import datetime, timedelta

import pandas as pd
import requests

API_KEY = 'ma595491219569679758263226220714'


class DataProvider:
    def __init__(self, locale, currency, country, origin,
                 outbound_date, inbound_date):
        self._quotes_url = 'http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/{}/{}/{}/{}/{}/{}/{}\
        ?apiKey={}'
        self._codes_table = pd.DataFrame()
        self._locale = locale
        self._currency = currency
        self._country = country
        self._origin = origin
        self._outbound_date = outbound_date
        self._inbound_date = inbound_date

    def _create_url(self, destination='anywhere'):
        return self._quotes_url.format(
            self._country,
            self._currency,
            self._locale,
            self._origin,
            destination,
            self._outbound_date,
            self._inbound_date,
            API_KEY,
        )

    @staticmethod
    def get_suggestions(city):
        url = 'http://partners.api.skyscanner.net/apiservices/autosuggest/v1.0/CH/CHF/en-GB/?query={}&apiKey={}'.format(
            city, API_KEY)
        suggestions = requests.get(url).json()
        suggestions = list(
            map(lambda x: {'name': x['PlaceName'], 'code': x['PlaceId']},
                suggestions['Places']))
        return suggestions

    def _get_connections(self, destination='anywhere'):
        data = requests.get(self._create_url(destination))
        return data.json()

    def _select_col_places(self, data):
        return pd.DataFrame(data['Places'])

    def _select_col_quotes(self, data):
        return pd.DataFrame(data['Quotes'])

    def _get_names(self, df):
        return df['OutboundLeg'].map(
            lambda x: {
                'origin': self._get_airport_name(x['OriginId']),
                'destination': self._get_airport_name(x['DestinationId'])
            }
        )

    def _get_airport_name(self, id_):
        airport_info = self._codes_table[self._codes_table['PlaceId'] == id_]
        return {
            'city_name': airport_info['CityName'].values[-1],
            'country_name': airport_info['CountryName'].values[-1],
            'code': airport_info['SkyscannerCode'].values[-1]
        }

    def get_propositions(self, destination='anywhere'):
        data = self._get_connections(destination)
        quotes = self._select_col_quotes(data)
        self._codes_table = self._select_col_places(data)
        airports_names = self._get_names(quotes)
        quotes['Airport'] = airports_names
        return quotes

    def _get_session(self, origin, destination, outdate, indate, adults):
        url = "http://partners.api.skyscanner.net/apiservices/pricing/v1.0"

        payload = "apiKey={}&country={}&currency={}&locale={}&originplace={}-sky&destinationplace={}-sky\
        &outbounddate={}&inbounddate={}&adults={}"
        payload = payload.format(
            API_KEY,
            self._country,
            self._currency,
            self._locale,
            origin,
            destination,
            outdate,
            indate,
            adults,
        )
        headers = {
            'content-type': "application/x-www-form-urlencoded",
            'accept': "application/json",
            'cache-control': "no-cache",
        }

        response = requests.request("POST", url, data=payload, headers=headers)

        return response.headers['Location']

    def get_prices(self, origin, destination, outdate, indate, adults):
        session_url = self._get_session(
            origin,
            destination,
            outdate,
            indate,
            adults,
        )
        query = '?sortorder={}&apiKey={}'.format('asc', API_KEY)
        response = requests.get(session_url + query)
        while response.status_code == '204':
            time.sleep(5)
            response = requests.get(session_url + query)
        return response.json()


if __name__ == '__main__':
    dp = DataProvider('en-GB', 'EUR', 'CH',
                      DataProvider.get_suggestions('Warszawa')[1]['code'],
                      (datetime.today() + timedelta(days=2)).date(),
                      (datetime.today() + timedelta(days=7)).date())
    print(dp.get_propositions(
        destination=DataProvider.get_suggestions('Zurych')[-1]['code']))
