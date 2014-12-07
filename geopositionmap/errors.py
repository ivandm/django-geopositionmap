from __future__ import unicode_literals

import sys, traceback
from django.utils.translation import ugettext_lazy as _

        
class LatLngError(Exception):
    def __init__(self, value):
        self.value = value
     
    def __str__(self):
        return self.value

    def __unicode__(self):
        return self.value

 
class InvalidCoordinateType(LatLngError):
    def __init__(self):
        super(InvalidCoordinateType, self)
        self.value = "%s"%_("Values are not coordiates type.")
         
class IncompatibleCoordinateType(LatLngError):
    def __init__(self):
        super(IncompatibleCoordinateType, self)
        self.value = "%s"%_("Values aren't coordinate compatible format. String must is '-xxx.dddddddd,-xxx.dddddddd' (lat,lng)")

class StringTypeError(LatLngError):
    def __init__(self, msg):
        super(StringTypeError, self)
        self.value = "%s"%_("Values is type %s. It must be a string object."%msg)

class LenArgsError(LatLngError):
    def __init__(self, msg):
        super(LenArgsError, self)
        self.value = "%s"%_("Values are %s. LatLng wants max 2 values in args."%msg)

class KwargsError(LatLngError):
    def __init__(self):
        super(KwargsError, self)
        self.value = "%s"%_("LatLng want keys 'lat' and 'lng' in kwargs")

class OutOfRangeLatError(LatLngError):
    def __init__(self):
        super(OutOfRangeLatError, self)
        self.value = "%s"%_("Lat is must between -90 and +90 degrees")

class OutOfRangeLngError(LatLngError):
    def __init__(self):
        super(OutOfRangeLngError, self)
        self.value = "%s"%_("Lng is must between -180 and +180 degrees")

class NELatLngObjectError(LatLngError):
    def __init__(self):
        super(OutOfRangeLngError, self)
        self.value = "%s"%_("NE value must an LatLng object instance")

class SWLatLngObjectError(LatLngError):
    def __init__(self):
        super(OutOfRangeLngError, self)
        self.value = "%s"%_("SW value must an LatLng object instance")

class FloatError(LatLngError):
    def __init__(self, value):
        super(FloatError, self)
        self.value = "%s"%_("%s. Coodinate must be type '-xxx.dddddddd'"%value)
