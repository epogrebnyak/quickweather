# quickweather
Get free weather forecast from www.7timer.info (no registration or token needed).

## Install

Let's keep it a secret.

## TODO: must provide header 

Если мы запускаем `Airport.random().get_weather()`, то получаем
пустой ответ. Если по URL запроса ходили через браузер,
то похоже ответ кешируется и будет доступен какое-то время 
через программный доступ.

Вопрос - можно ли приделать хедеры к запросу, чтобы эмулировать
как будто к серверу обращается браузер.

## Example

### Pick an airport by IATA code

```python
from pprint import pprint
from quickweather import Airport, Location

a = Airport("GRU")
pprint(a.dict)
```

Output:

```
{'city': 'Sao Paulo',
 'country': 'BR',
 'iata': 'GRU',
 'lat': -23.4355564117,
 'lon': -46.4730567932,
 'name': 'Guarulhos - Governador Andre Franco Montoro International Airport',
 'tz': 'America/Sao_Paulo'}
```

### Get the 'civil' weather forecast for an airport

```python
pprint(a.get_weather())
```

<details><summary>Output:</summary>

```
[{'date': 20240225,
  'temp2m': {'max': 28, 'min': 22},
  'weather': 'lightrain',
  'wind10m_max': 3},
 {'date': 20240226,
  'temp2m': {'max': 28, 'min': 21},
  'weather': 'oshower',
  'wind10m_max': 3},
 {'date': 20240227,
  'temp2m': {'max': 30, 'min': 21},
  'weather': 'cloudy',
  'wind10m_max': 3},
 {'date': 20240228,
  'temp2m': {'max': 31, 'min': 23},
  'weather': 'lightrain',
  'wind10m_max': 3},
 {'date': 20240229,
  'temp2m': {'max': 29, 'min': 22},
  'weather': 'lightrain',
  'wind10m_max': 2},
 {'date': 20240301,
  'temp2m': {'max': 27, 'min': 21},
  'weather': 'lightrain',
  'wind10m_max': 3},
 {'date': 20240302,
  'temp2m': {'max': 26, 'min': 20},
  'weather': 'lightrain',
  'wind10m_max': 3}]
```
</details>

### Get forecast for any location

```python
weather = Location(latitude=-23, longitude=-43).get_weather() 
pprint(weather)
```

Warning: <www.7timer.info> seems to have rate limits, please do not make too many queries at once.
Please appreciate it is a free service that does not require registration,
which is unique for weather data. Even `curl wttr.in` is down because there are too many queries.

## Aknowledgements

Many thanks to:

- <www.7timer.info> for keeping API alive, open and free,
- <https://github.com/mborsetti/airportsdata> for the IATA airport data,  
- `curl wttr.in` for great idea. Hope you will get more resources to run the service.
