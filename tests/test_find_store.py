from find_store import find_store
from collections import defaultdict
import json

STORE_LOCATIONS = 'tests/test-store-locations.csv'

def test_good_address():
	arguments = defaultdict(str)
	arguments['--address'] = '1770 Union St, San Francisco, CA 94123'
	result = find_store(arguments, STORE_LOCATIONS)
	assert 'San Francisco West (2675 Geary Blvd, San Francisco, CA 94118-3400) is 2.38755505411 km away' == result

def test_bad_address():
	arguments = defaultdict(str)
	arguments['--address'] = 'bad address'
	result = find_store(arguments, STORE_LOCATIONS)
	assert 'Unable to find your location' == result

def test_json_output():
	arguments = defaultdict(str)
	arguments['--zip'] = '94123'
	arguments['--units'] = 'mi'
	arguments['--output'] = 'json'
	result = find_store(arguments, STORE_LOCATIONS)
	json_output = json.loads(result)

	assert json_output['units'] == 'miles'
	assert json_output['distance'] == 1.4495726501734552
	assert json_output['Store Name'] == 'San Francisco West'

def test_good_bad_zip_code():
	arguments = defaultdict(str)
	arguments['--zip'] = '0'
	arguments['--units'] = 'mi'
	result = find_store(arguments, STORE_LOCATIONS)
	assert 'Unable to find your location' == result
