=====================
django-geopositionmap
=====================

A model field that can hold a geoposition (latitude/longitude), and corresponding admin/form widget.
Porting to GeoDjango Point type.
Google map and OSM map widgets.


Prerequisites
-------------

django-geopositionmap requires Django 1.4.10 or greater.
GeoDjango gis contrib geospatial framework.


Installation
------------

- Use your favorite Python packaging tool to install ``geopositionmap``
  from `PyPI`_, e.g.::

    pip install django-geopositionmap

- Add ``"geopositionmap"`` to your ``INSTALLED_APPS`` setting::

    INSTALLED_APPS = (
        # …
        "geopositionmap",
    )

- If you are still using Django <1.3, you are advised to install
  `django-staticfiles`_ for static file serving.


Usage
-----

``django-geopositionmap`` comes with a model field that makes it pretty
easy to add a geoposition field to one of your models. To make use of
it:

- In your ``myapp/models.py``::

    from django.db import models
    from geopositionmap.geoFields import LatLngField

    class POI(models.Model):
        name = models.CharField(max_length=100)
        position = LatLngField()

- This enables the following simple API::

    >>> from myapp.models import POI
    >>> poi = POI.objects.get(id=1)
    >>> poi.position
    LatLng(52.522906,13.41156)
    >>> poi.position.lat
    52.522906
    >>> poi.position.lng
    13.41156

- Some methods:

    >>> pos = LatLng(10.0, 11.0)
    >>> pos.geosPoint
    <Point object at 0x4175910L>
    >>> type(pos.geosPoint)
    <class 'django.contrib.gis.geos.point.Point'>
    >>> pos
    LatLng(10.0,11.0)
    >>> pos = LatLng('10','11')
    >>> pos
    LatLng(10.0,11.0)
    >>> pos.lat
    10.0
    >>> pos.lng
    11.0
    >>> print pos
    +010.0000000000000000,+011.0000000000000000
    >>> type(pos)
    <class 'geopositionmap.LatLng'>
    >>> pos.to_string()
    u'+010.0000000000000000,+011.0000000000000000'
    >>> type(pos.to_string())
    <type 'unicode'>
    >>> pos.pos
    (10.0, 11.0)
    >>> type (pos.pos)
    <type 'tuple'>
    >>> pos.lat = 14
    >>> pos.lng = -12
    >>> pos
    LatLng(14.0, -12.0)
    >>> pos.setPos(41,46)
    LatLng(41.0, 46.0)
    >>> pos.setPos('41.15 46.56')
    LatLng(41.15, 46.56)
    >>> 
    >>> ne = LatLng('-13.0','-11.0')
    >>> pos = LatLng('-14.0','-12.3')
    >>> sw = LatLng('-15.0','-13.0')
    >>> pos.isBounded(ne,sw)
    LatLng(-14.0, -12.3)
    >>> pos = LatLng('-14.0','12.3')
    >>> pos.isBounded(ne,sw)
    False

    

Form field and widget
---------------------

Admin
^^^^^

If you use a ``LatLngField`` in the admin it will automatically
show a `Google Maps`_ widget with a marker at the currently stored
position. You can drag and drop the marker with the mouse and the
corresponding latitude and longitude fields will be updated
accordingly.

It looks like this:

|geopositionmap-widget-admin|


Manager in models
-----------------

Models
^^^^^^

You can use custom Manager to manage custom methods in your models object.
LatLngField object is a geo position coordinate, thus you can find out if your point is right
into a boud area (NE,SW).

- In your ``myapp/models.py``::

    from django.db import models
    from geopositionmap.geoFields import LatLngField
    from geopositionmap.geoManager import geoManager
    
    objects = geoManager()

    class POI(models.Model):
        name = models.CharField(max_length=100)
        position = LatLngField()
        
        def is_bounded(self):
            return self.position

- This enables the following simple API::

    >>> from myapp.models import POI
    >>> POI.objects.bound('42,13','40,10') #retrive POIs into bound rectangle, if are active
    [<POI: POI object>]
    >>> POI.objects.bound() #retrive all active POIs
    []

    
- Active on map method

    from django.db import models
    from geopositionmap.geoFields import LatLngField
    from geopositionmap.geoManager import geoManager
    
    objects = geoManager()

    class POI(models.Model):
        name = models.CharField(max_length=100)
        position = LatLngField()
        
        def active_OnMap(self):
            return False #return 'True' to active is_bounded method
        
        def is_bounded(self):
            return self.position
            
- Use active_OnMap method enables the following simple API::

    >>> from myapp.models import POI
    >>> POI.objects.bound('42,13','40,10')
    []
    >>> POI.objects.bound()
    []
    
    
Regular Forms
^^^^^^^^^^^^^

Using the map widget on a regular form outside of the admin requires
just a little more work. In your template make sure that

- `jQuery`_ is included
- the static files (JS, CSS) of the map widget are included (just use
  ``{{ form.media }}``)

**Example**::

    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.8/jquery.min.js"></script>
    <form method="POST" action="">{% csrf_token %}
        {{ form.media }}
        {{ form.as_p }}
    </form>


Settings
--------

You can customize the `MapOptions`_ and `MarkerOptions`_ used to initialize the
map and marker in JavaScript by defining ``GEOPOSITIONMAP_MAP_OPTIONS`` or
``GEOPOSITIONMAP_MARKER_OPTIONS`` in your ``settings.py``.
Set True GEOPOSITIONMAP_GOOGLE_VIEW.GOOGLE_VIEW and GEOPOSITIONMAP_OSM_VIEW.OSM_VIEW to view
Google maps or view OSM maps.

**Example**::

    GEOPOSITIONMAP_MAP_OPTIONS = {
        'minZoom': 3,
        'maxZoom': 15,
    }

    GEOPOSITIONMAP_MARKER_OPTIONS = {
        'cursor': 'move'
    }

    GEOPOSITIONMAP_GOOGLE_VIEW = False # default is True
    GEOPOSITIONMAP_OSM_VIEW    = False # default is True
    
Please note that you cannot use a value like ``new google.maps.LatLng(52.5,13.4)``
for a setting like ``center`` or ``position`` because that would end up as a
string in the JavaScript code and not be evaluated. Please use
`Lat/Lng Object Literals`_ for that purpose, e.g. ``{'lat': 52.5, 'lng': 13.4}``.

You can also customize the height of the displayed map widget by setting
``GEOPOSITION_MAP_WIDGET_HEIGHT`` to an integer value (default is 480).


License
-------

`MIT`_


.. _Google Maps: http://code.google.com/apis/maps/documentation/javascript/
.. |geopositionmap-widget-admin| image:: docs/images/admin.jpg
.. _jQuery: http://jquery.com
.. _MIT: http://philippbosch.mit-license.org/
.. _MapOptions: https://developers.google.com/maps/documentation/javascript/reference?csw=1#MapOptions
.. _MarkerOptions: https://developers.google.com/maps/documentation/javascript/reference?csw=1#MarkerOptions
.. _Lat/Lng Object Literals: https://developers.google.com/maps/documentation/javascript/examples/map-latlng-literal
