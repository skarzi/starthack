import os
import requests

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import (
    Airport,
    Base,
    City,
    Continent,
    Country,
)
from skyscanner_facade import (
    API_KEY,
    API_URL,
)


def _prepare_db():
    # Initialize the database :: Connection & Metadata retrieval
    basedir = os.path.abspath(os.path.dirname(__file__))
    engine = create_engine(
        'sqlite:///' + os.path.join(basedir, 'skyscanner.db'),
        pool_recycle=3600,
    )
    Session = sessionmaker(bind=engine)
    # Create all tables that do not already exist
    Base.metadata.create_all(engine)
    return Session()


def _get_json():
    return requests.get(API_URL + 'geo/v1.0', params={'apiKey': API_KEY}).json()


def _parse_and_write_json(db_session, json_):
    for continent in json_['Continents']:
        continent_ = Continent(id=continent['Id'], name=continent['Name'])
        db_session.add(continent_)
        for country in continent['Countries']:
            country_ = Country(
                id=country['Id'],
                name=country['Name'],
                currency_id=country['CurrencyId'],
                continent_id=continent['Id'],
            )
            db_session.add(country_)
            for city in country['Cities']:
                lon, lat = [
                    float(x.strip()) for x in city['Location'].split(',')
                ]
                city_ = City(
                    id=city['Id'],
                    iata_code=city['IataCode'],
                    name=city['Name'],
                    longtitude=lon,
                    latitude=lat,
                    country_id=country['Id'],
                )
                db_session.add(city_)
                for airport in city['Airports']:
                    lon, lat = [
                        float(x.strip()) for x in airport['Location'].split(',')
                    ]
                    airport_ = Airport(
                        id=airport['Id'],
                        name=airport['Name'],
                        latitude=lat,
                        longtitude=lon,
                        city_id=city['Id'],
                    )
                    db_session.add(airport_)
    db_session.commit()


if __name__ == '__main__':
    db_session = _prepare_db()
    # _parse_and_write_json(db_session, _get_json())
    ids = [x.id for x in db_session.query(Country).all()]
    print('PL' in ids)
