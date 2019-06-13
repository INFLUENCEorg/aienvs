from aienvs.listener.DefaultListenable import DefaultListenable
from test.LoggedTestCase import LoggedTestCase
from unittest.mock import Mock


class testDefaultListenable(LoggedTestCase):

    def test_smoke(self):
        DefaultListenable()

    def test_subscribe(self):
        listenable = DefaultListenable()
        l = Mock()
        listenable.addListener(l)

        l.notifyChange.assert_not_called()
        listenable.notifyChange("hello")
        l.notifyChange.assert_called_with("hello")
        
    def test_unsubscribe(self):
        listenable = DefaultListenable()
        l = Mock()
        listenable.addListener(l)
        listenable.removeListener(l)

        l.notifyChange.assert_not_called()
        listenable.notifyChange("hello")
        l.notifyChange.assert_not_called()
        
