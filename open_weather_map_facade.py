from datetime import timedelta

import requests

API_URL = 'http://api.openweathermap.org/data/2.5/forecast/daily'
API_KEY = '4c7fd0781b820a77cdf429f35ad92599'


class OpenWeatherMapFacade:
    def get_weather(self, city, arrival_date, departue_date):
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
        current_date = arrival_date
        for i in range(0, (departue_date - arrival_date).days + 1):
            weather_info = weather_infos[i]
            icons_name = [x['icon'] for x in weather_info['weather']]
            result.append({
                'temp': weather_info['temp'],
                'pressure': weather_info['pressure'],
                'humidity': weather_info['humidity'],
                'description': [x['description'] for x in
                                weather_info['weather']],
                'icons': self._get_icon(icons_name),
                'date': current_date.strftime('%d %B'),
            })
            if current_date == departue_date:
                break
            current_date += one_day
        return result

    def _get_icon(self, icons_name):
        return ['http://openweathermap.org/img/w/{name}.png'.format(
            name=icon_name,
        ) for icon_name in icons_name]


if __name__ == '__main__':
    owmf = OpenWeatherMapFacade()
    import datetime

    print([a['date'] for a in
           owmf.get_weather('Warsaw', datetime.datetime.today(),
                            datetime.datetime.today() +
                            timedelta(days=2))])
