import re
from datetime import datetime, timedelta
from pprint import pprint

import pandas as pd
from skyscanner.skyscanner import Hotels

from google_places import geocode

hotels_service = Hotels('prtl6749387986743898559646983194')


def map_images(x):
    splitted = x[0].split('{')
    base = splitted[0:2]
    imgs = splitted[2:]
    base = ''.join(base)[:-1]
    imgs = re.split(r':\[\d*,\d*\],', imgs[0])[:-2]
    result = []
    for img in imgs:
        result.append(base + img)
    return result


def get_hotels(city, checkin, checkout, guests=1, rooms=1):
    latlon = geocode(city)
    entity = '{},{}-latlong'.format(latlon['lat'], latlon['lng'])
    hotels = hotels_service.get_result(
        market='CH',
        currency='EUR',
        locale='en-GB',
        entityid=entity,
        checkindate=checkin,
        checkoutdate=checkout,
        guests=guests,
        rooms=rooms).parsed
    return parse_hotels(hotels)


def parse_hotels(response):
    hotels_df = pd.DataFrame.from_dict(response['hotels'])
    prices_df = pd.DataFrame.from_dict(response['hotels_prices'])
    hotels_df = hotels_df.merge(left_on='hotel_id', right_on='id',
                                right=prices_df).drop('id', axis=1)
    hotels_df['price_total'] = hotels_df.agent_prices.map(
        lambda x: x[0]['price_total'])
    hotels_df.image_urls = hotels_df.image_urls.map(map_images)
    cols = ['hotel_id', 'image_urls', 'popularity_desc', 'star_rating',
            'types', 'name', 'price_total']
    hotels_df = hotels_df[cols]
    hotels_jsn = []
    for _, row in hotels_df.iterrows():
        hotels_jsn.append(dict(row))
    return hotels_jsn


if __name__ == '__main__':
    outbound = (datetime.today() + timedelta(days=2)).date()
    inbound = (datetime.today() + timedelta(days=7)).date()

    pprint(get_hotels('Zurich', outbound, inbound, 1, 1))
