from datetime import timedelta

import requests

API_URL = 'http://api.openweathermap.org/data/2.5/forecast/daily'
API_KEY = '4c7fd0781b820a77cdf429f35ad92599'


class OpenWeatherMapFacade:
    def get_weather(self, city, date):
        one_day = timedelta(days=1)
        weather_infos = requests.get(
            API_URL,
            params={
                'APPID': API_KEY,
                'q': city,
                'units': 'metric',
            },
        ).json()['list']
        result = list()
        current_data = date
        for weather_info in weather_infos:
            icons_name = [x['icon'] for x in weather_info['weather']]
            result.append({
                'temp': weather_info['temp'],
                'pressure': weather_info['pressure'],
                'humidity': weather_info['humidity'],
                'description': [x['description'] for x in weather_info['weather']],
                'icons': self._get_icon(icons_name),
                'date': current_data.strftime('%d.%m.%Y'),
            })
            current_data = date + one_day
        return result

    def _get_icon(self, icons_name):
        return ['http://openweathermap.org/img/w/{name}.png'.format(
            name=icon_name,
        ) for icon_name in icons_name]


if __name__ == '__main__':
    owmf = OpenWeatherMapFacade()

    import datetime
    print(owmf.get_weather('Zurich', datetime.datetime.today())[0]['date'])
