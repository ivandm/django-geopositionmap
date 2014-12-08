###################
# 
# This file is part of geField package.
# Copyright 2014 Ivan Del Mastro <info [a-t] adventure2italy.com>
# Version	1.0.0
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.
# 
# * @license    GNU/GPL - MIT, see above
###################

from django.db import models
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
        
class geoManager(models.Manager):
    def get_queryset(self):
        return geoQuerySet(self.model, using=self._db)
        
    def active_on_map(self):
        return self.get_queryset().active_on_map()

    def bound( self, ne=None, sw=None ):
        return self.get_queryset().bound(ne=ne, sw=sw)
