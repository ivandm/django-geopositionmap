from . import geoManager

# classe Manager specializzata per il campo geoFields.LatLngField
# questa classe deve essere inserita nel model db che contiene un campo geoFields.LatLngField
# Esempio:
# class Mark(geoModelMixIn, models.Model):
#    objects = geoManager()
#
#    This add next method that you can override:
#    def active_OnMap(self):
#       return True 
#

class geoModelMixIn(object):
        
    def active_OnMap(self):
        return True
