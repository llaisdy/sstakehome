from django.contrib.postgres.fields import ArrayField
from django.db import models

class Coordinates(models.Model): # TODO GeoDjango Point?
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f'({self.latitude}, {self.longitude})'

class PoI(models.Model):
    AIRPORT = 'airp'
    BEACH = 'beac'
    BUS_STOP = 'bust'
    CLINIC = 'clin'
    COFFEE_SHOP = 'coff'
    COLLEGE = 'coll'
    CONVENIENCE_STORE = 'conv'
    DOCTOR = 'doct'
    FAST_FOOD = 'fast'
    FERRY = 'ferr'
    FITNESS_STATION = 'fitn'
    GARDEN = 'gard'
    GYM = 'gymn'
    HOSPITAL = 'hosp'
    KINDERGARTEN = 'kind'
    MALL = 'mall'
    NATURE_RESERVE = 'natu'
    PHARMACY = 'phar'
    RAILWAY_STATION = 'rail'
    PARK = 'park'
    PUB = 'pub'
    RESTAURANT = 'rest'
    SCHOOL = 'scho'
    SPORTS_CENTRE = 'spor'
    SUPERMARKET = 'supe'
    UNIVERSITY = 'univ'
    
    POI_CATEGORY_CHOICES = (
        (AIRPORT, 'airport'),
        (BEACH, 'beach'),
        (BUS_STOP, 'bus-stop'),
        (CLINIC, 'clinic'),
        (COFFEE_SHOP, 'coffee-shop'),
        (COLLEGE, 'college'),
        (CONVENIENCE_STORE, 'convenience-store'),
        (DOCTOR, 'doctor'),
        (FAST_FOOD, 'fast-food'),
        (FERRY, 'ferry'),
        (FITNESS_STATION, 'fitness-station'),
        (GARDEN, 'garden'),
        (GYM, 'gym'),
        (HOSPITAL, 'hospital'),
        (KINDERGARTEN, 'kindergarten'),
        (MALL, 'mall'),
        (NATURE_RESERVE, 'nature-reserve'),
        (PHARMACY, 'park'),
        (RAILWAY_STATION, 'pharmacy'),
        (PARK, 'pub'),
        (PUB, 'railway-station'),
        (RESTAURANT, 'restaurant'),
        (SCHOOL, 'school'),
        (SPORTS_CENTRE, 'sports-centre'),
        (SUPERMARKET, 'supermarket'),
        (UNIVERSITY, 'university'),
    )
    
    RATINGS_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        )

    class Meta:
        verbose_name = "Point of Interest"
        verbose_name_plural = "Points of Interest"
    
    external_id = models.PositiveBigIntegerField()
    name = models.CharField(max_length=128)
    category = models.CharField(max_length=4, choices=POI_CATEGORY_CHOICES)
    description = models.TextField(max_length=1024)
    coordinates = models.ForeignKey(Coordinates,
                                    on_delete=models.SET_NULL, null=True)
    ratings = ArrayField(models.CharField(max_length=1, choices=RATINGS_CHOICES),
                         blank=True, default=list)

    @property
    def internal_id(self):
        return self.pk
