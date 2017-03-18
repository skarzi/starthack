import requests

API_URL = 'http://api.openweathermap.org/data/2.5/weather'
API_KEY = '4c7fd0781b820a77cdf429f35ad92599'
ICON_STORE = '/tmp/'


class OpenWeatherMapFacade:
    def get_weather(self, city, date):
        one_day = timedelta(days=1)
        weather_infos = requests.get(
            API_URL,
            params={
                'APPID': API_KEY,
                'q': city,
            },
        ).json()
        icons_name = [x['icon'] for x in weather_info['weather']]
        return {
                'temp': weather_info['main']['temp'],
                'pressure': weather_info['main']['pressure'],
                'humidity': weather_info['main']['humidity'],
                'description': [x['description'] for x in weather_info['weather']],
                'icons': self._get_icon(icons_name),
        }

    def _get_icon(self, icons_name):
        icons = list()
        for icon_name in icons_name:
            img = requests.get('http://openweathermap.org/img/w/{name}.png'.format(
                    name=icon_name,
                ),
                stream=True,
            )
            with open(ICON_STORE + icon_name + '.png', 'wb') as f:
                if img.status_code == 200:
                    for chunk in img:
                        f.write(chunk)
            icons.append(ICON_STORE + '{icon_name}.png'.format(
                icon_name=icon_name,
            ))
        return icon_name + '.png'


if __name__ == '__main__':
    owmf = OpenWeatherMapFacade()
    import datetime
    print(owmf.get_weather('Zurich', datetime.datetime.today())[0]['date'])
