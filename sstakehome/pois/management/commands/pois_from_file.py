import csv
import json
import os
import xmltodict

from django.core.management.base import BaseCommand, CommandError
from pois.models import Coordinates, PoI

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('filenames', nargs='+', type=str)

    def handle(self, *args, **options):
        for fn in options['filenames']:
            try:
                ext = os.path.splitext(fn)[1]
                if ext == '.json':
                    self.import_PoIs_from_json(fn)
                elif ext == '.csv':
                    self.import_PoIs_from_csv(fn)
                elif ext == '.xml':
                    self.import_PoIs_from_xml(fn)
                else:
                    self.stdout.write(
                        self.style.WARNING(f'Unrecognised format, skipping: {fn}')
                    )
            except:
                raise CommandError(f'Error handling file: {fn}')

            self.stdout.write(
                self.style.SUCCESS('Successfully imported all points')
            )

    def import_PoIs_from_json(self, fn):
        data = json.loads(open(fn).read())
        for d in data:
            create_poi_from_jdict(d)

    def import_PoIs_from_csv(self, fn):
        with open(fn, newline='') as csvfile:
            poireader = csv.DictReader(csvfile)
            for row in poireader:
                create_poi_from_csv(row)

    def import_PoIs_from_xml(self, fn):
        d = xmltodict.parse(open(fn).read())
        for e in d['RECORDS']['DATA_RECORD']:
            create_poi_from_xml(e)
            
csv_keys = (
    'poi_id',
    'poi_name',
    'poi_category',
    'poi_latitude',
    'poi_longitude',
    'poi_ratings'
)

xml_keys = (
    'pid',
    'pname',
    'platitude',
    'plongitude',
    'pcategory',
    'pratings',
)

def import_category(c):
    return c[:4]

def import_ratings_json(rs):
    return [str(i) for i in rs]

def import_ratings_csv(rs):
    return [int(eval(x)) for x in rs[1:-1].split(',')]

def import_ratings_xml(rs):
    return [int(x) for x in rs.split(',')]

def create_poi_from_xml(e):
    coords = Coordinates(latitude=e['platitude'],
                         longitude=e['plongitude'])
    coords.save()
    category = import_category(e['pcategory'])
    ratings = import_ratings_xml(e['pratings'])
    poi = PoI(external_id=e['pid'],
              name=e['pname'],
              category=category,
              coordinates=coords,
              ratings=ratings,
              )
    poi.save()
    return poi.pk

def create_poi_from_csv(row):
    coords = Coordinates(latitude=row['poi_latitude'],
                         longitude=row['poi_longitude'])
    coords.save()
    category = import_category(row['poi_category'])
    ratings = import_ratings_csv(row['poi_ratings'])
    poi = PoI(external_id=row['poi_id'],
              name=row['poi_name'],
              category=category,
              coordinates=coords,
              ratings=ratings,
              )
    poi.save()
    return poi.pk

def create_poi_from_jdict(d):
    coords = Coordinates(**d['coordinates'])
    coords.save()
    category = import_category(d['category'])
    ratings = import_ratings_json(d['ratings'])
    poi = PoI(external_id=d['id'],
              name=d['name'],
              category=category,
              description=d['description'],
              coordinates=coords,
              ratings=ratings,
              )
    poi.save()
    return poi.pk
