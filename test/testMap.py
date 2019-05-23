from aienvs.FactoryFloor.Map import Map
from LoggedTestCase import LoggedTestCase
from numpy import array


class TestMap(LoggedTestCase):

    def test_smoke(self):
        map = Map(['...', '...'])
        
    def test_smoke_not_square(self):
        self.assertRaises(ValueError, Map, ['123', '1234'])

    def test_getPart(self):
        map = Map(['123', 'abc', 'ABC'])
        part = map.getPart(array([[1, 1], [2, 2]]))
        self.assertEquals(2, part.getWidth())
        self.assertEquals(2, part.getHeight())
        self.assertEquals('b', part.get(array([0, 0])))
