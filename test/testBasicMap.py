from aienvs.BasicMap import BasicMap
from test.LoggedTestCase import LoggedTestCase
from numpy import array, array_equal


class TestBasicMap(LoggedTestCase):

    def test_smoke(self):
        map = BasicMap(['...', '...'])
        
    def test_smoke_not_square(self):
        self.assertRaises(ValueError, BasicMap, ['123', '1234'])

    def test_map(self):
        map = BasicMap(['...', '...'])

    def test_getPartZeroNewWeight(self):
        map = BasicMap(['123', 'abc', 'ABC'])
        part = map.getPart(array([[1, 1], [2, 2]]))
        self.assertEquals(2, part.getWidth())
        self.assertEquals(2, part.getHeight())
        self.assertEquals('b', part.get(array([0, 0])))

    def test_getPartZeroOldWeight(self):
        map = BasicMap(['abc', 'ABC'])
        part = map.getPart(array([[0, 0], [1, 1]]))
        self.assertEquals(2, part.getWidth())
        self.assertEquals(2, part.getHeight())
        self.assertEquals('a', part.get(array([0, 0])))

    def test_getPartOldAndNewWeight(self):
        map = BasicMap(['abc', 'ABC', '25.'])
        part = map.getPart(array([[1, 2], [2, 2]]))  # 5.
        self.assertEquals(2, part.getWidth())
        self.assertEquals(1, part.getHeight())
        self.assertEquals('5', part.get(array([0, 0])))

    def test_smoke_getRandomPos(self):
        map = BasicMap(['abc', 'ABC', '25.'])
        p1 = map.getRandomPosition()
        
