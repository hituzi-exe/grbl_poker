import numpy as np
import collections
from functools import lru_cache


class Calc:

    # (0x2c000 == 0b1111 0000 0000 0000 0000)
    JOKER = 0xF0000

    def createDeck(self):
        # S = suit bit(sdhc), N = num bit(a23456789tjqk)
        # card : chds ---k qjt9 8765 432a
        num = (0x0001 << np.arange(13, dtype=np.int32))
        suit = 0x0001 << (np.arange(4, dtype=np.int32) + 16)

        numx, suitx = np.ix_(num, suit)
        deck = suitx + numx

        return np.append(deck.flatten(), Calc.JOKER)

    def getMaxExpectation(self, hand1, hand2, hand3, hand4, hand5):
        return -1


class HandRankChecker:

    def __init__(self):
        self.rate = Rate()
        self.NumOfAKindMap = self.createNumOfAKindMap()

    def getHandRank(self, hand1, hand2, hand3, hand4, hand5):
        pair = getPareHand(hand1, hand2, hand3, hand4, hand5)

        if pair != self.rate.NotPair():
            return pair

        return -1

    def getRateNumOfAKind(self, hand1, hand2, hand3, hand4, hand5):
        handNum = (hand1 | hand2 | hand3 | hand4 | hand5) & (0x1fff)
        bitNum = self.bitCount(handNum)

        if bitNum == 5:
            return self.rate.NotPair()

        j = self.inJoker(hand1, hand2, hand3, hand4, hand5)

        pairMax, pairNum = self.pairCount(hand1, hand2, hand3, hand4, hand5)

        return self.NumOfAKindMap[pairNum + (pairMax - 1 + j) * 3]

    def inJoker(self, hand1, hand2, hand3, hand4, hand5):
        if Calc.JOKER in [hand1, hand2, hand3, hand4, hand5]:
            return 1

        return 0

    def createNumOfAKindMap(self):
        return [self.rate.NotPair(), self.rate.NotPair(), self.rate.NotPair(),
                self.rate.NotPair(), self.rate.OnePair(), self.rate.TwoPair(),
                self.rate.NotPair(), self.rate.ThreeOfAKind(), self.rate.FullHouse(),
                self.rate.NotPair(), self.rate.FourOfAKind(), self.rate.NotPair(),
                self.rate.NotPair(), self.rate.FiveOfAKind(), self.rate.NotPair(), ]

    def isStraight(self, hand1, hand2, hand3, hand4, hand5):
        handNum = (hand1 | hand2 | hand3 | hand4 | hand5) & (0x1fff)

        if handNum == 0x1e01:
            return True

        return (int(handNum / (handNum & (-handNum))) == 0x1f)

    def isFlush(self, hand1, hand2, hand3, hand4, hand5):
        return (hand1 & hand2 & hand3 & hand4 & hand5 & (0xf0000)) > 0

    def convert(self, hand):
        if hand == 'J0':
            return Calc.JOKER

        suits = list('sdhc')
        nums = list('a23456789tjqk')
        suit, num = list(hand)

        try:
            return (1 << (suits.index(suit) + 16)) | (1 << nums.index(num))
        except ValueError as ex:
            return (-1)

    def bitCount(self, x):
        # import gmpy2
        # return gmpy2.popcount(x)
        return bin(x).count("1")

    def pairCount(self, hand1, hand2, hand3, hand4, hand5):
        cnt = [x & (0x1fff) for x in [hand1, hand2, hand3, hand4, hand5]]
        values, counts = zip(*collections.Counter(cnt).most_common())
        return max(counts), len([i for i in counts if i > 1])


class Rate:
    def NotPair(self):
        return -1

    def HighCard(self):
        return 0

    def OnePair(self):
        return 0

    def TwoPair(self):
        return 1

    def ThreeOfAKind(self):
        return 1

    def FullHouse(self):
        return 10

    def FourOfAKind(self):
        return 20

    def FiveOfAKind(self):
        return 60

    def Straight(self):
        return 3

    def Flush(self):
        return 4

    def StraightFlush(self):
        return 25

    def RoyalStraightFlush(self):
        return 250


def main():
    # c = Calc()
    # print(c.createDeck())

    checker = HandRankChecker()
    #  checker.bitCount(0b0010011)

    checker.pairCount(0b00010000000000000010,
                      0b00100000000000001000,
                      0b00010000000000001000,
                      0b00010000000000010000,
                      0b00010000000000001000,
                      )


if __name__ == '__main__':
    main()
