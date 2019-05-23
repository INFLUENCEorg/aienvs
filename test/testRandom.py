
from LoggedTestCase import LoggedTestCase
from random import random, Random


class testRandom(LoggedTestCase):
    """
    This tests whether we have a custom random generator
    that is not affected by others calling random()
    """

    def test_repeatability(self):
        rnd1 = Random(42)
        randomnrs1 = [rnd1.random() for i in range(10)]
        rnd2 = Random(42)
        randomnrs2 = [rnd2.random() for i in range(10)]
        self.assertEquals(randomnrs1, randomnrs2)

    def test_notinfluenced(self):
        """
        We generate random list, and another one that is made while also
        calling random() (the global one) and compare the two
        """
        rnd1 = Random(42)
        randomnrs1 = [rnd1.random() for i in range(10)]
        rnd2 = Random(42)
        randomnrs2 = [ rnd2.random() for i in range(10) if random() > -1]
        self.assertEquals(randomnrs1, randomnrs2)
        
