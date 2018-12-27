import unittest
import numpy as np
from src.calc import Calc
from src.calc import HandRankChecker


class TescCalc(unittest.TestCase):

    # def test_calcMaxExpectation(self):
    #     c = Calc()
    #     self.assertEqual(c.calcMaxExpectation('', '', '', '', '',), 0)

    def test_createDeck(self):
        c = Calc()
        deck = c.createDeck()
        self.assertTrue(
            (deck == np.array([65537, 131073, 262145, 524289, 65538, 131074,
                               262146, 524290, 65540, 131076, 262148, 524292,
                               65544, 131080, 262152, 524296, 65552, 131088,
                               262160, 524304, 65568, 131104, 262176, 524320,
                               65600, 131136, 262208, 524352,  65664, 131200,
                               262272, 524416, 65792, 131328, 262400, 524544,
                               66048, 131584, 262656, 524800, 66560, 132096,
                               263168, 525312, 67584, 133120, 264192, 526336,
                               69632, 135168, 266240, 528384, 983040])).all())

    def test_convert_s1(self):
        c = HandRankChecker()
        self.assertEqual(c.convert('sa'), 0b00010000000000000001)

    def test_convert_s5(self):
        c = HandRankChecker()
        self.assertEqual(c.convert('s5'), 0b00010000000000010000)

    def test_convert_dt(self):
        c = HandRankChecker()
        self.assertEqual(c.convert('dt'), 0b00100000001000000000)

    def test_convert_Joker(self):
        c = HandRankChecker()
        self.assertEqual(c.convert('J0'), 0b11110000000000000000)

    def test_convert_exception(self):
        c = HandRankChecker()
        self.assertEqual(c.convert('hg'), -1)

    def test_JOKER(self):
        c = Calc()
        self.assertEqual(c.JOKER, 0b11110000000000000000)
