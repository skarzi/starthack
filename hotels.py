from skyscanner.skyscanner import Hotels

from config import skyscanner_token
from pprint import pprint
from datetime import datetime, timedelta

hotels_service = Hotels('prtl6749387986743898559646983194')


def get_suggestions(name):
    return hotels_service.location_autosuggest(
        market='CH',
        currency='EUR',
        locale='en-GB',
        query=name).parsed


def get_hotels(entity, checkin, checkout, guests, rooms):
    return hotels_service.get_result(
        market='CH',
        currency='EUR',
        locale='en-GB',
        entityid=entity,
        checkindate=checkin,
        checkoutdate=checkout,
        guests=guests,
        rooms=rooms).parsed

if __name__ == '__main__':
    outbound = (datetime.today() + timedelta(days=2)).date()
    inbound = (datetime.today() + timedelta(days=7)).date()

    city = input("City: ")
    suggested = get_suggestions(city)
    cities = [p for p in suggested['results'] if (p['geo_type'] == 'City' and p['parent_place_id'] == 1)]
    ids = [c['individual_id'] for c in cities]
    print(ids)
    idx = int(input("Select: "))
    pprint(get_hotels(ids[idx], outbound, inbound, 1, 1))
