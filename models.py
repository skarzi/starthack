from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Continent(Base):
    __tablename__ = 'continent'

    id = Column(String(1), primary_key=True)
    name = Column(String)
    countries = relationship("Country", back_populates="continent")


class Country(Base):
    __tablename__ = 'country'
    id = Column(String(2), primary_key=True)
    name = Column(String)
    currency_id = Column(String(3))
    continent_id = Column(
        String(1),
        ForeignKey("continent.id"),
        nullable=False,
    )
    continent = relationship('Continent', back_populates='countries')
    cities = relationship("City", back_populates="country")


class City(Base):
    __tablename__ = 'city'
    id = Column(String(4), primary_key=True)
    name = Column(String)
    latitude = Column(Integer)
    longtitude = Column(Integer)
    iata_code = Column(String(3))
    country_id = Column(
        String(2),
        ForeignKey("country.id"),
        nullable=False,
    )
    country = relationship('Country', back_populates='cities')
    airports = relationship("Airport", back_populates="city")


class Airport(Base):
    __tablename__ = 'airport'
    id = Column(String(3), primary_key=True)
    name = Column(String)
    latitude = Column(Integer)
    longtitude = Column(Integer)
    city_id = Column(
        String(4),
        ForeignKey("city.id"),
        nullable=False,
    )
    city = relationship('City', back_populates="airports")


"""
for continent in cont:
    cont_id = continent['Id']
    cont_name = continent['Name']
    countries = list()
    for country in continent['Countries']:
        country_id = country['Id']
        country_name = country['Name']
        country_currency_id = country['CurrencyId']
        country_cities = list()
        for city in country['Cities']:
            city_id = city['Id']
            city_iata_code = city['IataCode']
            city_location = city['Location']
            city_name = city['Name']
            city_airports = list()
            for airport in city['Airports']:
                airport_id = airport['Id']
                airport_name = airport['Name']
                airport_location = airport['Location']

"""
