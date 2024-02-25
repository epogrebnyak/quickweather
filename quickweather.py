from dataclasses import dataclass
from pathlib import Path

import httpx
import pandas

local_csv_path = Path(__file__).parent / "airports.csv"


@dataclass
class Location:
    """Geographic location.

    Latitude (широта) is a measurement of a location north or south of the equator.
    Longitude (долгота) is a measurement of location east or west of the prime meridian.
    """

    latitude: float
    longitude: float

    def _query(self):
        return query_civil_weather(self.latitude, self.longitude)

    def get_weather(self):
        r = self._query()
        if r.text:
            return r.json()["dataseries"]
        else:
            print("Empty response, the URL was:")
            print(r.url)
            print(self.weather_url)

    @property
    def weather_url(self) -> str:
        return str(civil_weather_url(self.latitude, self.longitude))

    def round(self, n_digits: int) -> "Location":
        def r(x):
            return round(x, n_digits)
        return Location(r(self.latitude), r(self.longitude))


def airport_df(force=False):
    try:
        if force:
            raise FileNotFoundError
        df = pandas.read_csv(local_csv_path)
    except FileNotFoundError:
        airports_url = "https://raw.githubusercontent.com/mborsetti/airportsdata/main/airportsdata/airports.csv"
        df = pandas.read_csv(airports_url)
        df.to_csv(local_csv_path)
    return mask(df)


def mask(df):
    return df[["iata", "name", "city", "country", "lat", "lon", "tz"]].dropna()


def civil_weather_url(latitude, longitude):
    payload = {
        "lat": latitude,
        "lon": longitude,
        "product": "civillight",
        "output": "json",
    }
    return httpx.URL("https://www.7timer.info/bin/api.pl", params=payload)


def query_civil_weather(latitude, longitude):
    """Use 7timer.info to get weather forecast."""
    url = civil_weather_url(latitude, longitude)
    return httpx.get(str(url))


def weather_at_airport(iata_code: str):
    """Get weather forecast by IATA airport code."""
    return Airport(iata_code).get_weather()


@dataclass
class Airport:
    """Airport as defined by four-letter IATA code."""

    iata_code: str

    @classmethod
    def dataframe(cls):
        return airport_df()

    @classmethod
    def random(cls):
        from random import choice
        iata_code = choice(airport_df().iata.values) 
        return cls(iata_code)



    @property
    def dict(self):
        df = airport_df()
        return df[df.iata == self.iata_code].iloc[0].to_dict()

    @property
    def location(self):
        d = self.dict
        return Location(latitude=d["lat"], longitude=d["lon"]).round(3)

    def get_weather(self):
        return self.location.get_weather()
