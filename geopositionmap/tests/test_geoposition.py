from django.test import SimpleTestCase
from geopositionmap import LatLng
from example.models import POI


class GeopositionTestCase(SimpleTestCase):

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
        self.assertEqual(repr(gp), 'LatLng(52.5, -13.4)')

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
        
    def test_bound_method_true(self):
        ne = LatLng('-13.0','-11.0')
        pos = LatLng('-14.0','-12.3')
        sw = LatLng('-15.0','-13.0')
        self.assertTrue(pos.isBounded(ne,sw) == pos)   
    
    def test_bound_method_false(self):
        ne = LatLng('-13.0','-11.0')
        pos = LatLng('-14.0','12.3')
        sw = LatLng('-15.0','-13.0')
        self.assertTrue(pos.isBounded(ne,sw) == False)   
