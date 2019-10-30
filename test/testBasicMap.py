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
        themap = BasicMap(['abc', 'ABC', '25.'])
        p1 = themap.getRandomPosition()
        self.assertTrue(themap.isInside(p1))
        
    def test_getSquaresDict(self):
        themap = BasicMap(['.a.', '.b.', '..c'])
        squares = themap._getSquaresDict()
        self.assertEquals(6, len(squares['.']))
        self.assertEquals(1, len(squares['a']))
        self.assertEquals(1, len(squares['b']))
        self.assertEquals(1, len(squares['c']))
        self.assertTrue(array_equal(array([1, 0]), squares['a'][0]))

    def test_getMapPositions(self):
        themap = BasicMap(['.a.', '.b.', '..c'])
        self.assertTrue(array_equal(array([1, 0]), themap.getMapPositions('a')[0]))
        self.assertEqual(6, len(themap.getMapPositions('.')))
        self.assertEqual(7, len(themap.getMapPositions('.a')))
        self.assertEqual(0, len(themap.getMapPositions('X')))

    def test_getFreeMapPosition(self):
        themap = BasicMap(['.a.', '.b.', '..c'])
        pos = themap.getFreeMapPosition()
        self.assertTrue(themap.isInside(pos))
        
    def test_getFreeMapPositionNoFreeTile(self):
        themap = BasicMap(['ful', 'lyo', 'cup'])
        with self.assertRaises(Exception) as context:
            themap.getFreeMapPosition()
        self.assertEquals("The map does not contain any free tiles" , str(context.exception))
        
    def test_equal_and_hash(self):
        themap1 = BasicMap(['.a.', '.b.', '..c'])
        themap2 = BasicMap(['.a.', '.b.', '..c'])
        themap3 = BasicMap(['.a.', '.b.', '.c.'])

        self.assertEquals(themap1, themap2)        
        self.assertNotEqual(themap1, themap3)        
        self.assertEquals(hash(themap1), hash(themap2))
        self.assertNotEqual(hash(themap1), hash(themap3))
        
