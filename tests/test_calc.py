import unittest
from src.calc import Calc


class TescCalc(unittest.TestCase):

    def test_say(self):
        c = Calc()
        self.assertEqual(c.getMaxExpectation('', '', '', '', '',), 0)
