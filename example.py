from pprint import pprint
from quickweather import Airport

a = Airport("GRU")
pprint(a.dict)
pprint(a.get_weather())
