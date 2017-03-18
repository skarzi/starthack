from collections import defaultdict

import googlemaps
import requests

from config import google_token

food = ['bakery', 'bar', 'cafe', 'meal_delivery', 'meal_takeaway',
        'restaurant']
nightlife = ['bar', 'casino', 'night_club']
wellbeing = ['beauty_salon', 'clothing_store', 'hair_care', 'park', 'spa',
             'gym']
funtime = ['amusement_park', 'aquarium', 'bowling_alley', 'casino']
art = ['art_gallery', 'museum', 'church', 'hindu_temple', 'synagogue']
city = ['city_hall', 'courthouse', 'fire_station', 'embassy', 'pharmacy',
        'hospital', 'police']

all_cats = {
    'food': food,
    'nightlife': nightlife,
    'wellbeing': wellbeing,
    'funtime': funtime,
    'art': art,
    'city': city
}


def geocode(city):
    api = googlemaps.Client(google_token)
    return api.geocode(city)[0]['geometry']['location']


def google_places(lat, lng, radius, types, key):
    AUTH_KEY = key
    LOCATION = str(lat) + "," + str(lng)
    RADIUS = radius
    TYPES = types
    MyUrl = ('https://maps.googleapis.com/maps/api/place/radarsearch/json'
             '?location=%s'
             '&radius=%s'
             '&types=%s'
             '&sensor=false&key=%s') % (LOCATION, RADIUS, TYPES, AUTH_KEY)
    response = requests.get(MyUrl)
    jsonRaw = response.json()
    return jsonRaw


def get_coords(x):
    return [y['geometry']['location'] for y in x]


def stats4city(city):
    """

    :param city:  name of the city :return: tuple(number of attractions in
    city(like statistics), all coordinates for types of attractions)
    """
    num_res_clas = defaultdict(int)
    coords_all = defaultdict(list)
    latlon = geocode(city)
    for cat, vals in all_cats.items():
        for c in vals:
            coords = get_coords(
                google_places(
                    latlon['lat'],
                    latlon['lng'],
                    radius=5000,
                    types=c,
                    key=google_token)['results'])
            num = len(coords)
            num_res_clas[cat] += num
            coords_all[cat].extend(coords)
    return dict(num_res_clas), dict(coords_all)
    # można wywalić coords_all jeżeli nie chcemy robić heatmapy


if __name__ == '__main__':
    print(stats4city('Zurich'))
