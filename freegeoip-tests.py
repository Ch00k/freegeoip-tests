import requests
import unittest
import json
from collections import OrderedDict


def get_info(ip_or_hostname='', response_format=''):
    url = 'http://minuteware.net:8908/%s/%s' % (response_format, ip_or_hostname)
    response = requests.get(url)
    return response.status_code, response.text


class TestFreeGeoIPRESTService(unittest.TestCase):
    def test_json_response(self):
        response_body = get_info('8.8.8.8', 'json')[1]
        json_actual = json.loads(response_body)
        sorted_json_actual = OrderedDict(sorted(json_actual.items()))
        json_expected = {
            'city': '', 'region_code': '', 'region_name': '', 'areacode': '', 'ip': '8.8.8.8', 'zipcode': '',
            'longitude': -97, 'metro_code': '', 'latitude': 38, 'country_code': 'US', 'country_name': 'United States'
        }
        sorted_json_expected = OrderedDict(sorted(json_expected.items()))
        self.assertEqual(sorted_json_expected, sorted_json_actual)

    def test_xml_response(self):
        response_body = get_info('8.8.8.8', 'xml')[1]
        xml_expected = '''<?xml version="1.0" encoding="UTF-8"?>
<Response>
 <Ip>8.8.8.8</Ip>
 <CountryCode>US</CountryCode>
 <CountryName>United States</CountryName>
 <RegionCode></RegionCode>
 <RegionName></RegionName>
 <City></City>
 <ZipCode></ZipCode>
 <Latitude>38</Latitude>
 <Longitude>-97</Longitude>
 <MetroCode></MetroCode>
 <AreaCode></AreaCode>
</Response>
'''
        self.assertEqual(xml_expected, response_body)

    def test_csv_response(self):
        response_body = get_info('8.8.8.8', 'csv')[1]
        csv_expected = '"8.8.8.8","US","United States","","","","","38.0000","-97.0000","",""'
        self.assertEqual(csv_expected, response_body)

    def test_invalid_response_format(self):
        response_code = get_info('8.8.8.8', 'invalid')[0]
        self.assertEqual(response_code, 404)

    def test_empty_response_format(self):
        response_code = get_info('8.8.8.8')[0]
        self.assertEqual(response_code, 404)

    def test_invalid_ip(self):
        response_code = get_info('345.678.123.890', 'json')[0]
        self.assertEqual(response_code, 404)

    def test_empty_ip(self):
        response_body = get_info('', 'json')[1]
        my_ip = requests.get('http://jsonip.com/').text
        my_ip = json.loads(my_ip)['ip']
        geo_ip = json.loads(response_body)['ip']
        self.assertEqual(my_ip, geo_ip)

    def test_ip_and_response_format_empty(self):
        response = get_info()
        self.assertEqual(response[0], 200)
        self.assertIn('<!doctype html>', response[1])

    def test_existing_hostname(self):
        response_body = get_info('feod.lviv.ua', 'json')[1]
        response_dict = json.loads(response_body)
        self.assertEqual(response_dict['ip'], '89.184.73.151')

    def test_inexisting_hostname(self):
        response_code = get_info('minutevare.net', 'json')[0]
        self.assertEqual(response_code, 404)


if __name__ == '__main__':
    unittest.main()
