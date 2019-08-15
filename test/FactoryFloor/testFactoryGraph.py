from test.LoggedTestCase import LoggedTestCase
from unittest.mock import Mock
from aienvs.FactoryFloor.FactoryGraph import FactoryGraph
from numpy import array
from aienvs.FactoryFloor.Map import Map


class testFactoryGraph(LoggedTestCase):

    def test_smoke(self):
        map = Mock()
        map.getWidth.return_value = 4
        map.getHeight.return_value = 4
        FactoryGraph(map)

    def test_graph_smoke(self):
        # bing lazy, using map is easier than mocking it.
        map = Map(['...', '.*.', '...'], .8)
        FactoryGraph(map)

    def test_graph_neighbours(self):
        # bing lazy, using map is easier than mocking it.
        map = Map(['...', '.*.', '...'], .8)
        g = FactoryGraph(map)
        self.assertTrue(g.has_node('[0 0]'))
        self.assertTrue(g.has_edge('[0 0]', '[0 1]'))
        self.assertFalse(g.has_node('[1 1]'))
        self.assertFalse(g.has_edge('[0 1]', '[1 1]'))
        
