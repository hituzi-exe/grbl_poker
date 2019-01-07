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
        c = Calc()
        self.assertEqual(c.convert('sa'), 0b00010000000000000001)

    def test_convert_s5(self):
        c = Calc()
        self.assertEqual(c.convert('s5'), 0b00010000000000010000)

    def test_convert_dt(self):
        c = Calc()
        self.assertEqual(c.convert('dt'), 0b00100000001000000000)

    def test_convert_Joker(self):
        c = Calc()
        self.assertEqual(c.convert('J'), 0b11110000000000000000)

    def test_convert_exception(self):
        c = Calc()
        self.assertEqual(c.convert('hg'), -1)

    def test_JOKER(self):
        c = Calc()
        self.assertEqual(c.JOKER, 0b11110000000000000000)

    def test_isFlush_true(self):
        c = HandRankChecker()
        self.assertTrue(c.isFlush(0b10000000000000001,
                                  0b10001000000000000,
                                  0b10000100000000000,
                                  0b10000010000000000,
                                  0b10000001000000000,))

    def test_isFlush_true_in_joker(self):
        c = HandRankChecker()
        self.assertTrue(c.isFlush(65537, 65538, 65540, 65544, 983040,))

    def test_isFlush_false(self):
        c = HandRankChecker()
        self.assertFalse(c.isFlush(262272, 262400, 264192, 262152, 524304,))

    def test_isStraightA_T_true(self):
        c = HandRankChecker()
        self.assertTrue(c.isStraight(0b10000000000000001,
                                     0b10001000000000000,
                                     0b10000100000000000,
                                     0b10000010000000000,
                                     0b10000001000000000,))

    def test_isStraight2_J_false(self):
        c = HandRankChecker()
        self.assertFalse(c.isStraight(0b10000000000000001,
                                      0b10001000000000000,
                                      0b10000100000000000,
                                      0b10000010000000000,
                                      0b10000000000000010,))

    def test_isStraight_true(self):
        c = HandRankChecker()
        self.assertTrue(c.isStraight(0b10000000000000001,
                                     0b10000000000000010,
                                     0b10000000000000100,
                                     0b10000000000001000,
                                     0b10000000000010000,))

    def test_isStraight_true2(self):
        c = HandRankChecker()
        self.assertTrue(c.isStraight(0b10000000000000010,
                                     0b10000000000000100,
                                     0b10000000000001000,
                                     0b10000000000010000,
                                     0b10000000000100000,))

    def test_isStraight_true3(self):
        c = HandRankChecker()
        self.assertTrue(c.isStraight(0b11110000000000000000,
                                     0b00010000000010000000,
                                     0b00100000000000001000,
                                     0b00010000000000010000,
                                     0b00100000000000100000,))

    def test_isStraight_false(self):
        c = HandRankChecker()
        self.assertFalse(c.isStraight(0b00010000000100000000,
                                      0b00010000000100000000,
                                      0b00010000000000001000,
                                      0b00010000000000010000,
                                      0b00010000000000100000,))

    def test_isStraight_false2(self):
        c = HandRankChecker()
        self.assertFalse(c.isStraight(0b00010000000100000000,
                                      0b00010000000010000000,
                                      0b00100000000000001000,
                                      0b00010000000000010000,
                                      0b00100000000000100000,))

    def test_bitCount_case1(self):
        c = HandRankChecker()
        self.assertEqual(c.bitCount(0b00000000010000010), 2)

    def test_bitCount_case2(self):
        c = HandRankChecker()
        self.assertEqual(c.bitCount(0b00001110010000010), 5)

    def test_bitCount_case3(self):
        c = HandRankChecker()
        self.assertEqual(c.bitCount(0b1000111001000001), 6)

    def test_pairCount_case1(self):
        c = HandRankChecker()
        self.assertEqual(c.pairCount(0b10000000000000010,
                                     0b10000000100000000,
                                     0b10000000000001000,
                                     0b10000000000010000,
                                     0b10000000000100000,), (1, 0))

    def test_getRateNumOfAKind_case1(self):
        c = HandRankChecker()
        self.assertEqual(c.getRateNumOfAKind(0b10000000000000010,
                                             0b10000000100000000,
                                             0b10000000000001000,
                                             0b10000000000010000,
                                             0b10000000000100000,), -1)

    def test_getRateNumOfAKind_OnePair(self):
        c = HandRankChecker()
        self.assertEqual(c.getRateNumOfAKind(0b10000000000001000,
                                             0b10000000100000000,
                                             0b10000000000001000,
                                             0b10000000000010000,
                                             0b10000000000100000,), 0)

    def test_getRateNumOfAKind_TwoPair(self):
        c = HandRankChecker()
        self.assertEqual(c.getRateNumOfAKind(0b010000000000001000,
                                             0b010000000100000000,
                                             0b100000000000001000,
                                             0b010000000000010000,
                                             0b100000000000010000,), 1)

    def test_getHandRank_onePair(self):
        c = HandRankChecker()
        self.assertEqual(c.getHandRank(0b00010000000001000000,
                                       0b00010000000100000000,
                                       0b00100000000000001000,
                                       0b00010000000000010000,
                                       0b00100000000000010000,), 0)

    def test_getHandRank_TwoPair(self):
        c = HandRankChecker()
        self.assertEqual(c.getHandRank(0b00010000000001000000,
                                       0b01000000000001000000,
                                       0b00100000000000001000,
                                       0b00010000000000010000,
                                       0b00100000000000010000,), 1)

    def test_getHandRank_ThreeOfAKind(self):
        c = HandRankChecker()
        self.assertEqual(c.getHandRank(0b01000000000000010000,
                                       0b00010000000100000000,
                                       0b00100000000000001000,
                                       0b00010000000000010000,
                                       0b00100000000000010000,), 1)

    def test_getHandRank_ThreeOfAKind_inJoker(self):
        c = HandRankChecker()
        self.assertEqual(c.getHandRank(0b11110000000000000000,
                                       0b00010000000100000000,
                                       0b00100000000000001000,
                                       0b00010000000000010000,
                                       0b00100000000000010000,), 1)

    def test_getHandRank_FourOfAKind(self):
        c = HandRankChecker()
        self.assertEqual(c.getHandRank(0b10000000000000010000,
                                       0b01000000000000010000,
                                       0b00100000000000010000,
                                       0b00010000000000010000,
                                       0b00100000000000001000,), 20)

    def test_getHandRank_FourOfAKind_inJoker(self):
        c = HandRankChecker()
        self.assertEqual(c.getHandRank(0b11110000000000000000,
                                       0b01000000000000010000,
                                       0b00100000000000010000,
                                       0b00010000000000010000,
                                       0b00100000000000001000,), 20)

    def test_getHandRank_FullHouse(self):
        c = HandRankChecker()
        self.assertEqual(c.getHandRank(0b01000000000000001000,
                                       0b01000000000000010000,
                                       0b00100000000000010000,
                                       0b00010000000000010000,
                                       0b00100000000000001000,), 10)

    def test_getHandRank_FullHouse_inJoker(self):
        c = HandRankChecker()
        self.assertEqual(c.getHandRank(0b01000000000000001000,
                                       0b01000000000000010000,
                                       0b11110000000000000000,
                                       0b00010000000000010000,
                                       0b00100000000000001000,), 10)

    def test_getHandRank_FiveOfAKind(self):
        c = HandRankChecker()
        self.assertEqual(c.getHandRank(0b11110000000000000000,
                                       0b01000000000000010000,
                                       0b00100000000000010000,
                                       0b00010000000000010000,
                                       0b10000000000000010000,), 60)

    def test_getHandRank_Straight(self):
        c = HandRankChecker()
        self.assertEqual(c.getHandRank(0b10000000000001000000,
                                       0b00010000000010000000,
                                       0b00100000000000001000,
                                       0b00010000000000010000,
                                       0b00100000000000100000,), 3)

    def test_getHandRank_Straight_inJoker(self):
        c = HandRankChecker()
        self.assertEqual(c.getHandRank(0b11110000000000000000,
                                       0b00010000000010000000,
                                       0b00100000000000001000,
                                       0b00010000000000010000,
                                       0b00100000000000100000,), 3)

    def test_getHandRank_Flush(self):
        c = HandRankChecker()
        self.assertEqual(c.getHandRank(0b00010000000100000000,
                                       0b00010000000010000000,
                                       0b00010000000000001000,
                                       0b00010000000000010000,
                                       0b00010000000000100000,), 4)

    def test_getHandRank_Flush_inJoker(self):
        c = HandRankChecker()
        self.assertEqual(c.getHandRank(0b11110000000000000000,
                                       0b00010000010000000000,
                                       0b00010000000000001000,
                                       0b00010000000000010000,
                                       0b00010000000000100000,), 4)

    def test_getHandRank_StraightFlush(self):
        c = HandRankChecker()
        self.assertEqual(c.getHandRank(0b00010000000010000000,
                                       0b00010000000001000000,
                                       0b00010000000000001000,
                                       0b00010000000000010000,
                                       0b00010000000000100000,), 25)

    def test_getHandRank_StraightFlush2(self):
        c = HandRankChecker()
        self.assertEqual(c.getHandRank(0b00010000000000000001,
                                       0b00010000000000000010,
                                       0b00010000000000000100,
                                       0b00010000000000001000,
                                       0b00010000000000010000,), 25)

    def test_getHandRank_StraightFlush_inJoker(self):
        c = HandRankChecker()
        self.assertEqual(c.getHandRank(0b11110000000000000000,
                                       0b00010000001000000000,
                                       0b00010000010000000000,
                                       0b00010000100000000000,
                                       0b00010001000000000000,), 250)

    def test_getHandRank_RoyalStraightFlush(self):
        c = HandRankChecker()
        self.assertEqual(c.getHandRank(0b00010000000000000001,
                                       0b00010000001000000000,
                                       0b00010000010000000000,
                                       0b00010000100000000000,
                                       0b00010001000000000000,), 250)

    def test_getHandRank_StraightFlush_inJoker(self):
        c = HandRankChecker()
        self.assertEqual(c.getHandRank(0b11110000000000000000,
                                       0b00010000000001000000,
                                       0b00010000000000001000,
                                       0b00010000000000010000,
                                       0b00010000000000100000,), 25)

    def test_getHandRank_HighCard(self):
        c = HandRankChecker()
        self.assertEqual(c.getHandRank(0b10000000100000000000,
                                       0b00100000000010000000,
                                       0b00010000000000001000,
                                       0b00010000000000010000,
                                       0b00010000000000100000,), 0)
