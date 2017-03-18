import requests

from geopy.distance import (
    distance,
    Point,
)
from geopy.geocoders import Nominatim

from uber_rides.client import UberRidesClient
from uber_rides.session import Session

SERVER_TOKEN = 'SQcKdYbSKuWQvGMKHDdtA0UnHvt6rSQXB51Fajtj'
CURRENCY_API_URL = 'http://api.fixer.io/latest?symbols=USD,EUR'

geolocator = Nominatim()


class UberFacade:
    def __init__(self):
        self._session = Session(server_token=SERVER_TOKEN)
        self._client = UberRidesClient(self._session)

    def get_rides(self, city):
        latitude, longtitude = self._lat_lot_of_city(city)
        response = self._client.get_products(latitude, longtitude)
        response = response.json.get('products')
        all_offers = list()
        for offer in response:
            all_offers.append({
                'name': offer['display_name'],
                'price_details': offer['price_details'],
                'logo': offer['image'],
                'capacity': offer['capacity'],
            })
        return all_offers

    def get_rides_from_to(self, from_, to_, seats=1):
        from_latitude, from_longtitude = self._lat_lot_of_city(from_)
        to_latitude, to_longtitude = self._lat_lot_of_city(to_)
        prices = self._client.get_price_estimates(
            start_latitude=from_latitude,
            start_longitude=from_longtitude,
            end_latitude=to_latitude,
            end_longitude=to_longtitude,
            seat_count=seats
        )
        best = None
        for price in prices.json['prices']:
            if (price['high_estimate'] is None or
                    price['low_estimate'] is None or
                    price['currency_code'] is None):
                continue
            if best is None:
                best = price
            if (best['low_estimate'] < price['low_estimate']):
                best = price
        result = {key: val for key, val in best.items() if key in (
            'currency_code', 'low_estimate', 'high_estimate'
        )}
        # dystans w linii prostej !
        result['distance'] = distance(
            Point(from_latitude, from_longtitude),
            Point(to_latitude, to_longtitude),
        ).kilometers
        if result['currency_code'] != 'EUR':
            result['low_estimate'], result['high_estimate'] = self._convert_currencies(
                [result['low_estimate'], result['high_estimate']],
                result['currency_code'],
                'EUR',
            )
            result['currency_code'] = 'EUR'
        return result

    def _lat_lot_of_city(self, city):
        loc = geolocator.geocode(city)
        return loc.latitude, loc.longitude

    def _convert_currencies(self, amounts, from_currency, to_currency):
        convert_coeff = requests.get(
            CURRENCY_API_URL,
            params={'symbols': '{0},{1}'.format(from_currency, to_currency)},
        ).json()['rates'][from_currency]
        return [int(amount / convert_coeff) for amount in amounts]


if __name__ == '__main__':
    print(UberFacade().get_rides_from_to('Zurich', 'St Gallen'))
