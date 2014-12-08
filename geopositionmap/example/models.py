from django.db import models
from geopositionmap.geoFields import LatLngField


class POI(models.Model):
    name = models.CharField(max_length=100)
    position = LatLngField(blank=True)

    class Meta:
        verbose_name_plural = 'Points of interest'
