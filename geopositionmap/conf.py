# -*- coding: utf-8 -*-
from django.conf import settings
from appconf import AppConf


class GeopositionMapConf(AppConf):
    MAP_WIDGET_HEIGHT = 480
    
    # google settings
    GOOGLE_VIEW = True
    MAP_OPTIONS = {}
    MARKER_OPTIONS = {}
    
    # osm settings
    OSM_VIEW = True

    class Meta:
        prefix = 'geopositionmap'
