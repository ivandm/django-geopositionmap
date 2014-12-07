# -*- coding: ISO-8859-1 -*-
"""
Form Widget classes specific to the geoSite admin site.
"""

# A class that corresponds to an HTML form widget, 
# e.g. <input type="text"> or <textarea>. 
# This handles rendering of the widget as HTML.
import json

from django.template.loader import render_to_string
from .conf import settings

from django.utils import six

from django import forms
from django.forms import widgets, MultiWidget, Media
from django.utils.html import conditional_escape, format_html, format_html_join
from django.forms.util import flatatt, to_current_timezone
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.templatetags.static import static

from . import LatLng

# classe widget utilizzata dal campo forms.geoFields LatLngField
class LatLngTextInputWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = (
            forms.TextInput(),
            forms.TextInput(),
        )
        super(LatLngTextInputWidget, self).__init__(widgets, attrs)
        
    def decompress(self, value):
        if isinstance(value, six.text_type):
            return value.rsplit(',')
        if value:
            return [value.lat, value.lng]
        return [None,None]
        
    def format_output(self, rendered_widgets):
        return render_to_string('geopositionmap/widgets/geopositionmap.html', {
            'latitude': {
                'html': rendered_widgets[0],
                'label': _("latitude"),
            },
            'longitude': {
                'html': rendered_widgets[1],
                'label': _("longitude"),
            },
            'config': {
                'map_widget_height': settings.GEOPOSITION_MAP_WIDGET_HEIGHT,
                'map_options': json.dumps(settings.GEOPOSITION_MAP_OPTIONS),
                'marker_options': json.dumps(settings.GEOPOSITION_MARKER_OPTIONS),
            }
        })
        
    class Media:
        #extend = False
        css = {
            'all': (
                    'geopositionmap/geopositionmap.css',
                    )
        }
        js = (
            '//maps.google.com/maps/api/js?sensor=false', 
            'geopositionmap/geopositionmap.js',
            )