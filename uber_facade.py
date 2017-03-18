import requests

from uber_rides.client import UberRidesClient
from uber_rides.session import Session

SERVER_TOKEN = 'SQcKdYbSKuWQvGMKHDdtA0UnHvt6rSQXB51Fajtj'


class UberFacade:
    def __init__(self):
        self._session = Session(server_token=SERVER_TOKEN)
        self._client = UberRidesClient(self._session)

    def get_rides(self, city):
        latitude, longtitude = self._lat_lot_of_city(city)
        response = self._client.get_products(latitude, longtitude)
        return response.json.get('products')

    def _lat_lot_of_city(self, city):
        response = requests.get(
            'https://maps.googleapis.com/maps/api/geocode/json',
            params={'address': city},
        )
        resp_json_payload = response.json()
        return list(
            resp_json_payload['results'][0]['geometry']['location'].values(),
        )


if __name__ == '__main__':
    print(UberFacade().get_rides('Berlin'))
