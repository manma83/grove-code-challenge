from __future__ import division
import csv
from collections import defaultdict
from math import atan2, cos, pi, radians, sin, sqrt
import json

from docopt import docopt
import geocoder


def calculate_distance(location_a, location_b):
    # use Haversine formula
    # https://en.wikipedia.org/wiki/Haversine_formula
    earth_radius = 6371 # km
    latitude_a = location_a[0]
    longitude_a = location_a[1]
    latitude_b = location_b[0]
    longitude_b = location_b[1]
    d_latitude = deg2rad(latitude_b - latitude_a)
    d_longitude = deg2rad(longitude_b - longitude_a)
    a = sin(d_latitude/2) * sin(d_latitude/2) + cos(deg2rad(latitude_a)) * cos(deg2rad(latitude_b)) * sin(d_longitude/2) * sin(d_longitude/2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    d = earth_radius * c
    return d

# converts the number in degrees to the radian equivalent
def deg2rad(deg):
  return deg * (pi/180)

def map_stores(stores, geocoded_location_latlng):
    distance_map = defaultdict(lambda: [])
    for store in stores:
        store_location = (float(store['Latitude']), float(store['Longitude']))
        distance = calculate_distance(geocoded_location_latlng, store_location)
        distance_map[distance].append(store)
    return distance_map

def format_stores(file_name):
    with open(file_name, 'r') as store_locations:
        reader = csv.reader(store_locations, delimiter=',', quotechar='"')
        keys = next(reader)  # skip headers
        return [{key: value for key, value in zip(keys, r)} for r in reader]


def get_output(store, distance_km, unit, output):
    distance = distance_km
    closest_store = store[0]
    if unit == 'mi':
        distance *= 0.621371
        unit = 'miles'
    else:
        unit = 'km'

    formatted_distance = '%s %s' % (distance, unit)

    if output == 'json':
        response = closest_store
        response['units'] = unit
        response['distance'] = distance
        response = json.dumps(response)
    else:
        response = '%s (%s, %s, %s %s) is %s away' % \
                (closest_store['Store Name'],
                 closest_store['Address'],
                 closest_store['City'],
                 closest_store['State'],
                 closest_store['Zip Code'],
                 formatted_distance)

    return response


def find_store(arguments, store_file):
    location = arguments['--address'] if arguments['--address'] else arguments['--zip']

    geocoded_location = geocoder.google(location)

    if geocoded_location and geocoded_location.latlng:
        formatted_stores = format_stores(store_file)
        store_distance_map = map_stores(formatted_stores, geocoded_location.latlng)
        # sort by distance
        distances = sorted(store_distance_map.iterkeys())
        return get_output(store_distance_map[distances[0]], distances[0], arguments['--units'], arguments['--output'])
    else:
        return 'Unable to find your location'


if __name__ == '__main__':
    doc = """
        Find Store
          find_store will locate the nearest store (as the vrow flies) from
          store-locations.csv, print the matching store address, as well as
          the distance to that store.

        Usage:
          find_store --address=<address>
          find_store --address=<address>  [--units=(mi|km)] [--output=(text|json)]
          find_store --zip=<zip>
          find_store --zip=<zip> [--units=(mi|km)] [--output=(text|json)]

        Options:
          --zip=<zip>           Find nearest store to this zip code. If there are multiple best-matches, return the first.
          --address=<address>   Find nearest store to this address. If there are multiple best-matches, return the first.
          --units=(mi|km)       Display units in miles or kilometers [default: mi].
          --output=(text|json)  Output in human-readable text, or in JSON (e.g. machine-readable) [default: text].

        Example
          find_store --address="1770 Union St, San Francisco, CA 94123"
          find_store --zip=94115 --units=km
    """
    arguments = docopt(doc)

    print find_store(arguments, 'store-locations.csv')
