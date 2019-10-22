from aienvs.FactoryFloor.Map import Map
from test.LoggedTestCase import LoggedTestCase
from numpy import array, array_equal


class TestMap(LoggedTestCase):

    def test_smoke(self):
        map = Map(['...', '...'], .8)
        
    def test_smoke_not_square(self):
        self.assertRaises(ValueError, Map, ['123', '1234'], .8)

    def test_map(self):
        map = Map(['...', '...'], .8)
        self.assertEquals(0.8, map.getTaskProbability())

    def test_getPartZeroNewWeight(self):
        map = Map(['123', 'abc', 'ABC'], 1)
        part = map.getPart(array([[1, 1], [2, 2]]))
        self.assertEquals(2, part.getWidth())
        self.assertEquals(2, part.getHeight())
        self.assertEquals('b', part.get(array([0, 0])))

    def test_getPartZeroOldWeight(self):
        map = Map(['abc', 'ABC'], .8)
        part = map.getPart(array([[0, 0], [1, 1]]))
        self.assertEquals(2, part.getWidth())
        self.assertEquals(2, part.getHeight())
        self.assertEquals('a', part.get(array([0, 0])))

    def test_getPartOldAndNewWeight(self):
        map = Map(['abc', 'ABC', '25.'], .8)
        part = map.getPart(array([[1, 2], [2, 2]]))  # 5.
        self.assertEquals(2, part.getWidth())
        self.assertEquals(1, part.getHeight())
        self.assertEquals('5', part.get(array([0, 0])))
        self.assertEquals(0.8 * 5 / (2 + 5), part.getTaskProbability())

    def test_smoke_getRandomPos(self):
        map = Map(['abc', 'ABC', '25.'], .8)
        p1 = map.getRandomPosition()
        
