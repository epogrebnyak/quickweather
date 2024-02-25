from pprint import pprint
from quickweather import Airport

a = Airport.random(country="RU")
pprint(a.dict)
pprint(a.get_weather()[:3])
