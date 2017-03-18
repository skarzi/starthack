import requests


API_URL = 'http://partners.api.skyscanner.net/apiservices/'
API_KEY = 'pw948929450599841224927489979782'
DEFAULTS_SKYSCANNER = {
    'currency': 'EUR',
    'locale': 'en-GB',
    'country': 'CH',
    'cabinclass': 'first',
    'locationschema': 'iata',
    'children': 0,
    'infants': 0,

}


class SkyscannerFacade:
    def __init__(self, country, currency, locale):
        self._country = country
        self._currency = currency
        self._locale = locale

    def get_flights(
        self,
        from_,
        to_,
        outbound_date,
        inbound_date,
        adults=1,
        **kwargs
    ):
        """
        flights = requests.get(
            API_URL + ("browsequotes/v1.0/{country}/{currency}/{locale}/"
                        "{originPlace}/{destinationPlace}/{outboundPartialDate}/"
                        "{inboundPartialDate}").format(
                    country=self._country,
                    locale=self._locale,
                ),
            params={'apiKey':API_KEY},
        )
        """
        from_id = self._get_city_id(from_)
        to_id = self._get_city_id(to_)
        self._create_session(
            from_id,
            to_id,
            outbound_date,
            inbound_date,
            adults,
        )

    def _create_session(
        self,
        from_,
        to_,
        outbound_date,
        inbound_date,
        adults,
        **kwargs
    ):
        creating_result = requests.post(
            API_URL + 'pricing/v1.0',
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                # 'X-Forwarded-For': '172.27.1.19',
                'Accept': 'application/json',
            },
            data={
                'cabinclass': self._get_or_default(kwargs, 'cabinclass'),
                'country': self._country,
                'currency': self._currency,
                'locale': self._locale,
                'locationschema': self._get_or_default(
                    kwargs,
                    'locationschema',
                ),
                'originplace': from_,
                'destinationplace': to_,
                'outbounddate': outbound_date,
                'inbounddate': inbound_date,
                'adults': adults,
                'children': self._get_or_default(kwargs, 'children'),
                'infants': self._get_or_default(kwargs, 'infants'),
                'apiKey': API_KEY,
            },
        )
        print(creating_result)
        print(creating_result.headers)
        print(creating_result.json())

    def _get_or_default(self, dict_, key):
        return dict_.get(key, DEFAULTS_SKYSCANNER[key])

    def _get_autosuggest(self, city, **kwargs):
        suggestions = requests.get(
            API_URL + "autosuggest/v1.0/{country}/{currency}/{locale}".format(
                country=self._country,
                currency=self._currency,
                locale=self._locale,
            ),
            params={"query": city, "apiKey": API_KEY},
        )
        return suggestions.json()

    def _get_city_id(self, city):
        print(self._get_autosuggest(city)['Places'][0]['PlaceId'])
        return self._get_autosuggest(city)['Places'][0]['PlaceId']


if __name__ == '__main__':
    sf = SkyscannerFacade(currency='EUR', locale='en-GB', country='CH')
    sf.get_flights('Warsaw', 'Zurich', '2017-03-26', '2017-03-28', {'adults': 1})
