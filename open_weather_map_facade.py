import requests

API_URL = 'http://api.openweathermap.org/data/2.5/forecast/daily'
API_KEY = '4c7fd0781b820a77cdf429f35ad92599'


class OpenWeatherManFacade:
    def get_weather(self, city):
        weather_infos = requests.get(
            API_URL,
            params={
                'APPID': API_KEY,
                'q': city,
                'units': 'metric',
            },
        ).json()['list']
        result = list()
        for weather_info in weather_infos:
            icons_name = [x['icon'] for x in weather_info['weather']]
            result.append({
                'temp': weather_info['temp'],
                'pressure': weather_info['pressure'],
                'humidity': weather_info['humidity'],
                'description': [x['description'] for x in weather_info['weather']],
                'icons': self._get_icon(icons_name),
            })
        return result

    def _get_icon(self, icons_name):
        return ['http://openweathermap.org/img/w/{name}.png'.format(
            name=icon_name,
        ) for icon_name in icons_name]


if __name__ == '__main__':
    owmf = OpenWeatherManFacade()
    print(owmf.get_weather('Zurich'))
