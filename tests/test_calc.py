import unittest
from src.calc import Calc


class TescCalc(unittest.TestCase):

    def test_say(self):
        c = Calc()
        self.assertEqual(c.getMaxExpectation('', '', '', '', '',), 0)

    def test_convert_s1(self):
        c = Calc()
        self.assertEqual(c.convert('s1'), 0x00010000000000000001)

    def test_convert_dt(self):
        c = Calc()
        self.assertEqual(c.convert('dt'), 0x00100000001000000000)

    def test_convert_Joker(self):
        c = Calc()
        self.assertEqual(c.convert('J0'), 0x11110000000000000000)

    def test_JOKER(self):
        c = Calc()
        self.assertEqual(c.JOKER, 0b11110000000000000000)
