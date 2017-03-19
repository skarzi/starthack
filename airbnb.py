import json

import requests


class BadAPIResponse(Exception):
    pass


class AirBNBService:
    """
    Provide simple interface to AirBNB `unofficial` API.
    `Official` api doesn't support date parameters for it's search endpoint
    making it quite useless for our case.
    This is quite dirty solution - feel warned.
    """
    ENDPOINT_URL = "https://www.airbnb.com/api/v2/explore_tabs"
    API_KEY = "d306zoyjsyarp7ifhu67rjxn52tv0t20"

    def get_default_params(self, **kwargs):
        """ provide some default URL params (used by airbnb website) """
        defaults = {
            "version": "1.1.0",
            "fetch_filters": "true",
            "supports_for_you_v3": "false",
            "items_per_grid": 9999,
            "currency": "EUR",
            "key": AirBNBService.API_KEY,
        }
        defaults.update(kwargs)
        return defaults

    def search(self, location, checkin, checkout, **kwargs):
        """ search for available places for given parameters """
        date_format = "%Y-%m-%d"
        params = self.get_default_params(**kwargs)
        params.update({
            "location": location,
            "checkin": checkin.strftime(date_format),
            "checkout": checkout.strftime(date_format)
        })
        response = requests.get(AirBNBService.ENDPOINT_URL, params=params)
        return self.clean_data(json.loads(response.text))

    def clean_data(self, data):
        """ clean data returned from endpoint since it's too ugly and complex """
        try:
            ads_list = data["explore_tabs"][0]["sections"][0]["listings"]
        except (KeyError, IndexError):
            raise BadAPIResponse(
                "Response received from AirBNB API lacks expected data.")
        else:
            return ads_list


if __name__ == "__main__":
    # obtain and display some simple data
    from datetime import date

    api = AirBNBService()
    data = api.search("Zurich", date(2017, 3, 20), date(2017, 3, 24))
    print(
        """
        Sample place:
        {listing[name]}, {listing[city]}
        {listing[public_address]}
        Cost: {pricing_quote[rate]} ({pricing_quote[rate_type]})
        """.format(**data[0])
    )
    from pprint import pprint
    pprint(data[0])
