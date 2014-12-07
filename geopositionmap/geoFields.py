# -*- coding: ISO-8859-1 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.six import with_metaclass
from django.utils.encoding import smart_text

from django.utils.translation import ugettext_lazy as _

from . import LatLng
from . import geoFormFields
        
# Campo django di gestione dei punti geografici
# i punti geografici sono oggetti istanza LatLng
#class LatLngField(models.CharField):
class LatLngField(with_metaclass(models.SubfieldBase, models.Field)):

    # TEST OK
    
    description = _("A geoposition Latitude and Longitude field")

    # If you’re handling custom Python types. 
    # You must use special metaclass "models.SubfieldBase"
    # This ensures that the to_python() method, documented below, 
    # will always be called when the attribute is initialized.
    #__metaclass__ = models.SubfieldBase
    
    def __init__(self, *args, **kwargs):
        
        # decimali di default per le coordinate 
        # setta max_length come lunghezza della stringa delle coordinate dall'oggetto LatLng
        # max_length = len( LatLng() )
        p = LatLng()
        self.max_length = len(p) #43
        default = {'max_length': self.max_length}
        kwargs.update(default)
               
        super(LatLngField, self).__init__(*args, **kwargs)
    
    def get_internal_type(self):
        #return 'CharField'
        return 'GeoPosition Map field'  
        
    def db_type(self, connection):
        # calcola la lunghezza del campo char del database
        p = LatLng()
        lenght = len(p) #self.max_length * 2 + 11
        return 'char(%s)'%lenght # type this: "-041.90997180,-012.53650420"
        
    # Converting database values to Python objects
    # quindi da stringa ad oggetto LatLng
    def to_python(self, value):
        if isinstance(value, LatLng):
            return value
        if isinstance(value, list): # valore arriva dal form 
            return LatLng(value[0], value[1])
        # se non e' un oggetto LatLng istanzia un nuovo oggetto LatLng
        # il tipo di valore in 'value' sara' gestito direttamente dall'oggetto LatLng
        p = LatLng()
        p.setPos(value)
        return p
    
    # Converting Python objects to query values
    # quindi da oggetto LatLng a stringa (!!)
    def get_prep_value(self, value):
        if isinstance(value, LatLng):
            return value.to_string() # usa sempre il formato predefinito dell'oggetto LatLng
        
        # se non e' un oggetto LatLng tenta la conversione
        # e ritorna la stringa
        p = LatLng()
        p.setPos(value)
        return p.to_string()
        
    # implementare la ricerca nel db sul campo
    # per ricercare se la coordinata e' all'interno di un'area (bound)
    # ma forse debbo spostare la ricerca nel Manager con un metodo specifico
    # che controlla tutti i campi, e ritorna una lista iterabile (con yield??)
    # per avere le istanze di modello per i normali metodi di ricerca
    # esempio:
    # mymodel.object.bounded(NE, SW).filter(...)
    
    # forse serve
    #def value_to_string(self, obj):
    #    value = self._get_val_from_obj(obj)
    #    return smart_text(value)
        
    def get_prep_lookup(self, lookup_type, value):
        value = self.get_prep_value(value)
        return super(LatLngField, self).get_prep_lookup(lookup_type, value)
        
    # implementare il campo form da utilizzare per il template
    def formfield(self, **kwargs):
        # Returns the default form field to use when this field is displayed in a model. 
        # This method is called by the ModelForm helper.
        
        # Utilizza LatLngField di geoFields. Campi forms personalizzati 
        defaults = {'form_class': geoFormFields.LatLngFormField}
        kwargs.update(defaults)
        return super(LatLngField, self).formfield(**kwargs)

    