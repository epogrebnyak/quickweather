from quickweather import Airport, Location


def test_sheremetyevo():
    assert Airport("SVO").location == Location(latitude=55.973, longitude=37.415)


def test_weather():
    r = Airport("SVO").location._query()
    print(r.url)
    print(r.text)
    assert len(r.json()["dataseries"]) == 7
