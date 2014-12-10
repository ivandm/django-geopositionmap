# -*- coding: ISO-8859-1 -*-

# A class that is responsible for:
# doing VALIDATION, e.g. an EmailField that makes sure its data is a valid email address.
# choce a WIDGET geoWidget's type
# 

"""
Field forms classes.
"""

from django import forms
from django.core import validators
from django.core.validators import EMPTY_VALUES
from django.utils.encoding import smart_text, force_text
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

import sys, traceback

from . import geoWidgets
from . import LatLng

from gpxdata import Document
        
class LatLngFormField(forms.MultiValueField):
    widget = geoWidgets.LatLngTextInputWidget
    
    default_error_messages = {
        'invalid': _('Enter a valid geoposition.')
    }

    def __init__(self, *args, **kwargs):
        #self.widget = geoWidgets.LatLngTextInputWidget()
        fields = (
            forms.DecimalField(label=_('latitude'),max_value=90.0, min_value=-90.0),
            forms.DecimalField(label=_('longitude'),max_value=180.0, min_value=-180.0),
        )
        if 'initial' in kwargs:
            kwargs['initial'] = LatLng(*kwargs['initial']).pos
        super(LatLngFormField, self).__init__(fields, **kwargs)

    def widget_attrs(self, widget):
        classes = widget.attrs.get('class', '').split()
        classes.append('geoposition')
        return {'class': ' '.join(classes)}

    def compress(self, value_list):
        if value_list:
            return value_list
        return ""

