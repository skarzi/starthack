import json
from copy import deepcopy

import requests
from requests_oauthlib import OAuth1

from config import yelp_consumer_key, yelp_consumer_secret, yelp_token, \
    yelp_token_secret

root_categories = None


def get_categories_tree():
    categories_yelp = requests.get(
        'https://www.yelp.com/developers/documentation/v2/all_category_list/categories.json').json()

    from collections import defaultdict
    cats = defaultdict(list)
    for c in categories_yelp:
        for p in c['parents']:
            cats[p].append({'alias': c['alias'], 'title': c['title']})

    root_cats = [c for c in categories_yelp if not c['parents']]

    all_cats = {c['alias']: {'children': [], 'title': c['title']} for c in
                categories_yelp}

    tree = {c['alias']: {'children': all_cats[c['alias']]['children'],
                         'title': c['title']} for c in root_cats}

    for c in categories_yelp:
        for p in c['parents']:
            all_cats[p]['children'].append({c['alias']: all_cats[c['alias']]})

    return tree


def del_keys(x):
    keys = {
        'categories', 'display_phone', 'image_url', 'location',
        'rating_img_url_small', 'review_count'
    }
    copy = deepcopy(x)
    for key in copy.keys():
        if key not in keys:
            del x[key]
    copy = deepcopy(x)
    for key in copy['location'].keys():
        if key != 'coordinate':
            del x['location'][key]
    return x


def coords_only(x):
    return x['location']['coordinate']


def get_places(city):
    global root_categories
    if not root_categories:
        root_categories = json.load(open('root_cats.json'))
    auth = OAuth1(yelp_consumer_key, yelp_consumer_secret, yelp_token,
                  yelp_token_secret)

    points = {}
    for c in root_categories.keys():
        r = requests.get(
            'https://api.yelp.com/v2/search?location={}&category_filter={}&radius_filter=5000&limit=40&sort=2'.format(
                city, c),
            auth=auth)
        points[c] = r.json()

    keys2del = []
    for c in points.keys():
        try:
            points[c] = [coords_only(x) for x in points[c]['businesses']]
        except KeyError:
            if 'error' in points[c].keys():
                keys2del.append(c)
            else:
                pass
    for k in keys2del:
        del points[k]

    return points


if __name__ == '__main__':
    print(get_places('Zurich'))
