# Grove code challenge
To find a nearest store, address or zip is geocoded using Google geocoding service via [geocoder](https://github.com/DenisCarriere/geocoder) python library. Internet connection is required for the application to run. If you expect a nearest store with your input and the application returns "Unable to geocode your location", this could be cause of internet connection issue, try to run it again. 

If inputed location is geocoded successfully, then store locations from CSV files is transformed to a list of dicts with calculated distance from the inputed address or ZIP code, then returns a closest store in text or json format

I used [Haversine formula](https://en.wikipedia.org/wiki/Haversine_formula) to calculate the distance between inputed address (or ZIP code) and store location

# Instructions
Create [virtualdev](https://packaging.python.org/guides/installing-using-pip-and-virtualenv/), then run `pip install -r requirements.txt`
```
Usage:
  python find_store.py --address=<address>
  python find_store.py --address=<address>  [--units=(mi|km)] [--output=(text|json)]
  python find_store.py --zip=<zip>
  python find_store.py --zip=<zip> [--units=(mi|km)] [--output=(text|json)]

Options:
  --zip=<zip>           Find nearest store to this zip code. If there are multiple best-matches, return the first.
  --address=<address>   Find nearest store to this address. If there are multiple best-matches, return the first.
  --units=(mi|km)       Display units in miles or kilometers [default: mi].
  --output=(text|json)  Output in human-readable text, or in JSON (e.g. machine-readable) [default: text].

Example
  python find_store.py --address="1770 Union St, San Francisco, CA 94123"
  python find_store.py --zip=94115 --units=km
```

To test, please run run `pytest`