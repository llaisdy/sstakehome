import csv
import json
import os
import xmltodict

from django.test import TestCase

from pois.models import Coordinates
from pois.management.commands.pois_from_file import (
    create_poi_from_csv,
    create_poi_from_jdict,
    create_poi_from_xml
    )

eg_poi_in =   {
    "id": "9684715928",
    "name": "50嵐",
    "category": "coffee-shop",
    "description": "aqeflxeurqjjfckl",
    "coordinates": {
      "latitude": 24.89868170026652,
      "longitude": 121.21074869999998
    },
    "ratings": [2, 2, 3, 3, 4, 5, 2, 2, 4, 1],
  }

class PoITestCase(TestCase):
    data_dir = 'pois/test_data/'
    
    def test_create_Coordinates(self):
        coords = Coordinates(**eg_poi_in['coordinates'])
        coords.save()
        self.assertTrue(coords.pk > 0)

    def test_create_PoI(self):
        created = create_poi_from_jdict(eg_poi_in)
        self.assertTrue(created)

    def test_import_PoIs_from_json(self):
        fn = os.path.join(self.data_dir, 'pois-10.json')
        data = json.loads(open(fn).read())
        for d in data:
            self.assertTrue(create_poi_from_jdict(d))

    def test_import_PoIs_from_csv(self):
        fn = os.path.join(self.data_dir, 'pois-10.csv')
        with open(fn, newline='') as csvfile:
            poireader = csv.DictReader(csvfile)
            for row in poireader:
                self.assertTrue(create_poi_from_csv(row))

    def test_import_PoIs_from_xml(self):
        fn = os.path.join(self.data_dir, 'pois-10.xml')
        d = xmltodict.parse(open(fn).read())
        for e in d['RECORDS']['DATA_RECORD']:
            self.assertTrue(create_poi_from_xml(e))
