from django.db import models
from django.contrib.gis.db import models as djangoGeoModels
from . import LatLng

# classe Manager specializzata per il campo geoFields.LatLngField
# questa classe deve essere inserita nel model db che contiene un campo geoFields.LatLngField
# Esempio:
# class Mark(models.Model):
#    objects = geoManager()
#
# uso: Mark.objects.bound(ne,sw).filter(altri filtri qui)
# 
# Il manager 'objects' viene ereditato dalle sotto classi.
# Esempio:
# class HikingTrail(Author, Track, Mark, CommonTrailField):
#    autore = .....
# uso: HikingTrail.objects.bound(ne,sw).filter(autore='utente')
#

class geoQuerySet(models.QuerySet):
    def active_on_map(self):
        result = self.all()
        filter_id = []
        for item in result:
            if hasattr(item, 'active_OnMap'):
                if item.active_OnMap() == True:
                    filter_id.append(item.id)
            else:
                filter_id.append(item.id)
        #r = result.filter(pk__in=filter_id)
        r = self.filter(pk__in=filter_id)
        return r
        
    def bound( self, ne='0,0', sw='0,0' ):
        result = self.active_on_map()
        if ne == None and sw == None:
            return result
        # filtra tutti i punti all'interno del bound NE,SW
        # 'ne' e 'sw' sono coordinate in formato stringa: es. '12.34,48.63'
        # ritorna un oggetto QuerySet
        NE = LatLng(ne)
        SW = LatLng(sw)
        
        # quanto sara' veloce???
        #result = self.all()
        #result = self.filter()
        
        filter_id = []
        for item in result:
            if hasattr(item, 'is_bounded'): # cerca il metodo 'di_bounded' nel modello in models
                if item.is_bounded().isBounded(NE,SW) != False:
                    filter_id.append(item.id)
        #r = result.filter(pk__in=filter_id)
        r = self.filter(pk__in=filter_id)
        return r
        
class geoManager(djangoGeoModels.Manager):
    #def get_queryset(self):
    #    return geoQuerySet(self.model, using=self._db)
        
    def active_on_map(self):
        # instead of return self.get_queryset().active_on_map() 
        return geoQuerySet(self.model, using=self._db).active_on_map() 

    def bound( self, ne=None, sw=None ):
         # instead of return self.get_queryset()..bound(ne=ne, sw=sw)
        return geoQuerySet(self.model, using=self._db).bound(ne=ne, sw=sw)
