from pprint import pprint
from quickweather import Airport

a = Airport.random()
pprint(a.dict)
pprint(a.get_weather())
