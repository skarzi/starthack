import requests

from config import url


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


if __name__ == '__main__':
    print(get_balance())
