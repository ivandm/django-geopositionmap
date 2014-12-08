#from decimal import float
from django.test import SimpleTestCase
from geopositionmap import LatLng
from example.models import POI


class GeopositionTestCase(SimpleTestCase):
    def test_init_with_decimals(self):
        gp = LatLng(float('52.5'), float('-13.4'))
        self.assertEqual(gp.lat, float('52.5'))
        self.assertEqual(gp.lng, float('-13.4'))

    def test_init_with_strs(self):
        gp = LatLng('52.5', '-13.4')
        self.assertEqual(gp.lat, float('52.5'))
        self.assertEqual(gp.lng, float('-13.4'))

    def test_init_with_setter(self):
        gp = LatLng()
        gp.lat = 52.5
        gp.lng = -13.4
        self.assertEqual(gp.lat, float('52.5'))
        self.assertEqual(gp.lng, float('-13.4'))

    def test_init_with_floats(self):
        gp = LatLng(52.5, -13.4)
        self.assertEqual(gp.lat, float('52.5'))
        self.assertEqual(gp.lng, float('-13.4'))

        
    def test_repr(self):
        gp = LatLng(52.5, -13.4)
        self.assertEqual(repr(gp), 'LatLng(+052.5000000000000000,-013.4000000000000004)')

    def test_equality(self):
        gp1 = LatLng(52.5, -13.4)
        gp2 = LatLng(52.5, -13.4)
        self.assertEqual(gp1, gp2)

    def test_inequality(self):
        gp1 = LatLng(52.5, -13.4)
        gp2 = LatLng(52.4, -13.4)
        self.assertNotEqual(gp1, gp2)

    def test_equality_with_none(self):
        gp1 = LatLng(52.5, -13.4)
        gp2 = None
        self.assertFalse(gp1 == gp2)

    def test_inequality_with_none(self):
        gp1 = LatLng(52.5, -13.4)
        gp2 = None
        self.assertTrue(gp1 != gp2)

    def test_db_value_to_python_object(self):
        obj = POI.objects.create(name='Foo', position=LatLng(52.5,-13.4))
        poi = POI.objects.get(id=obj.id)
        self.assertIsInstance(poi.position, LatLng)
