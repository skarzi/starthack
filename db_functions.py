import re

import pandas as pd
import requests

from config import url

car = ['BlaBlaCar', 'Uber', 'Lyft', 'taxi', 'train']
hotel = ['Airbnb', 'hotel']

from geotext import GeoText


def get_balance():
    """

    :return: counts amount of money across all users accounts
    """
    r = requests.get(url + '/cashAccounts')
    cash = 0
    if r.status_code == 200:
        print(r.json())
        for account in r.json():
            cash += account['balance']
    return cash


def parse_transactions(transactions):
    df = pd.DataFrame(transactions)
    df['abroad'] = df.counterPartyName.map(
        lambda x: len(GeoText(x).cities)).astype('bool')
    expenses_abroad = df.query('abroad == True').amount.sum()
    df['cars'] = df.counterPartyName.map(
        lambda x: len(re.findall(r'|'.join(car), x))).astype('bool')
    expenses_travel = df.query('cars == True').amount.sum()
    df['hotels'] = df.counterPartyName.map(
        lambda x: len(re.findall(r'|'.join(hotel), x))).astype('bool')
    expenses_accomodation = df.query('hotels == True').amount.sum()
    return {
        'abroad': -expenses_abroad,
        'travel': -expenses_travel,
        'accomodation': -expenses_accomodation
    }


if __name__ == '__main__':
    print(get_balance())
