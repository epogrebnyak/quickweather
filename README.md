# quickweather

Get free weather forecast from www.7timer.info (no registration or token needed).

## Install

```console
git clone https://github.com/epogrebnyak/quickweather.git
cd quickweather
pip install -e .
pip install -r requirements.txt
```

## Example

### Pick an airport by IATA code

```python
from pprint import pprint
from quickweather import Airport, Location

a = Airport("UEN")
pprint(a.dict)
```

Output:

```
{'city': 'Urengoy',
 'country': 'RU',
 'elevation': 56.0,
 'iata': 'UEN',
 'icao': 'USDU',
 'lat': 65.9599990845,
 'lon': 78.43699646,
 'name': 'Urengoy Airport',
 'subd': 'Yamalo-Nenets',
 'tz': 'Asia/Yekaterinburg'}
```

### Get the 'civil' weather forecast for an airport

Limit forecast to 3 days (out of 7):

```python
weather = Airport("UEN").get_weather()[:3]
pprint(weather)
```

Output:

```
[{'date': 20240225,
  'temp2m': {'max': -14, 'min': -16},
  'weather': 'cloudy',
  'wind10m_max': 3},
 {'date': 20240226,
  'temp2m': {'max': -6, 'min': -16},
  'weather': 'cloudy',
  'wind10m_max': 4},
 {'date': 20240227,
  'temp2m': {'max': -2, 'min': -7},
  'weather': 'lightsnow',
  'wind10m_max': 3}]
```

Check <https://github.com/Yeqzids/7timer-issues/wiki/Wiki> for `wind10m_max` scales.

### Get forecast for any geographic location

Proximity of São Paulo, Brazil:

```python
weather = Location(latitude=-23, longitude=-43).get_weather()
pprint(weather[:3])
```

> [!IMPORTANT]
> Please appreciate <www.7timer.info> is a free service that does not require registration,
> which is unique for weather data. Even `curl wttr.in` may be down because there are too many
> queries and not enough computer resources to handle them.
> Please do not make too many queries for <www.7timer.info> using this or other code.

## Aknowledgements

Many thanks to:

- <https://www.7timer.info> for keeping API alive, open and free,
- <https://github.com/mborsetti/airportsdata> for the IATA airport data,
- [`curl wttr.in`](https://wttr.in/:help?lang=ru) for inspiration.
