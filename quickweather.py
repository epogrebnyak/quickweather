"""Get weather forecast from https://www.7timer.info/ for arbitrary location or IATA airport.

See also:
   curl wttr.in
"""

from dataclasses import dataclass
from pathlib import Path

import httpx
import pandas

local_csv_path = Path(__file__).parent / "airports.csv"


@dataclass
class Location:
    """Geographic location.

    Latitude (ru: "широта") is a measurement of a location North or South of equator.
    Longitude (ru: "долгота") is a measurement of a location East or West of the prime meridian.
    """

    latitude: float
    longitude: float

    def query(self):
        return query_civil_weather(self.latitude, self.longitude)

    def get_weather(self):
        return self.query().json()["dataseries"]

    @property
    def weather_url(self) -> str:
        return str(civil_weather_url(self.latitude, self.longitude))

    def round(self, n_digits: int) -> "Location":
        """Round location coordinates to n digits."""

        def r(x):
            return round(x, n_digits)

        return Location(r(self.latitude), r(self.longitude))


def airport_df() -> pandas.DataFrame:
    """Return dataframe with all airports. Will cache dataframe to a local file."""
    try:
        df = pandas.read_csv(local_csv_path)
    except FileNotFoundError:
        airports_url = "https://raw.githubusercontent.com/mborsetti/airportsdata/main/airportsdata/airports.csv"
        df = pandas.read_csv(airports_url)
        df.to_csv(local_csv_path)
    return df

def iata_df() -> pandas.DataFrame:
    """Return dataframe with IATA airports.
    Not all airports have IATA code.
    """ 
    return mask(airport_df())

def mask(df) -> pandas.DataFrame:
    return df[["iata", "name", "city", "country", "lat", "lon", "tz"]].dropna()


def civil_weather_url(latitude, longitude):
    """Make base URL for 7timer.info API call.
       Note there will be a further redirect from this URL.
    """
    payload = {
        "lat": latitude,
        "lon": longitude,
        "product": "civillight",
        "output": "json",
    }
    return httpx.URL("https://www.7timer.info/bin/api.pl", params=payload)


def query_civil_weather(latitude, longitude):
    """Use 7timer.info to get simple weather forecast."""
    url = civil_weather_url(latitude, longitude)
    return httpx.get(str(url), follow_redirects=True)


def weather_at_airport(iata_code: str):
    """Get weather forecast by IATA airport code."""
    return Airport(iata_code).get_weather()


@dataclass
class Airport:
    """Airport as defined by four-letter IATA code."""

    iata_code: str

    @classmethod
    def dataframe(cls):
        return iata_df()


    @classmethod
    def random(cls, country=None):
        from random import choice

        df = cls.dataframe()
        if country:
            df = df[df.country == country]
        iata_code = choice(df.iata.values)
        return cls(iata_code)

    @property
    def dict(self):
        df = airport_df()
        d = df[df.iata == self.iata_code].iloc[0].to_dict()
        del d['Unnamed: 0'] # data not necessary 
        del d['lid'] # missing data
        return d

    @property
    def location(self):
        d = self.dict
        return Location(latitude=d["lat"], longitude=d["lon"]).round(3)

    def get_weather(self):
        return self.location.get_weather()
