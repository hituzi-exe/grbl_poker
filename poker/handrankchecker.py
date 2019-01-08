import math
import collections
import poker.calc
from functools import lru_cache


class HandRankChecker:

    def __init__(self):
        self.rate = Rate1000()
        self.NumOfAKindMap = self.createNumOfAKindMap()

    def getHandRank(self, hand1, hand2, hand3, hand4, hand5):
        pair = self.getRateNumOfAKind(hand1, hand2, hand3, hand4, hand5)

        if pair != self.rate.NotPair():
            return pair

        flushFlg = self.isFlush(hand1, hand2, hand3, hand4, hand5)
        straightFlg = self.isStraight(hand1, hand2, hand3, hand4, hand5)

        if not (flushFlg | straightFlg):
            return self.rate.HighCard()

        if flushFlg & straightFlg:
            if self.isRoyalStraightFlush(hand1, hand2, hand3, hand4, hand5):
                return self.rate.RoyalStraightFlush()

            return self.rate.StraightFlush()

        if flushFlg:
            return self.rate.Flush()

        return self.rate.Straight()

    def getRateNumOfAKind(self, hand1, hand2, hand3, hand4, hand5):
        if bitCount((hand1 | hand2 | hand3 | hand4 | hand5) & (0x1fff)) == 5:
            return self.rate.NotPair()

        pairMax, pairNum = self.pairCount(hand1, hand2, hand3, hand4, hand5)

        return self.NumOfAKindMap[pairNum + (pairMax - 1) * 3]

    def createNumOfAKindMap(self):
        return [self.rate.NotPair(), self.rate.NotPair(), self.rate.NotPair(),
                self.rate.NotPair(), self.rate.OnePair(), self.rate.TwoPair(),
                self.rate.NotPair(), self.rate.ThreeOfAKind(), self.rate.FullHouse(),
                self.rate.NotPair(), self.rate.FourOfAKind(), self.rate.NotPair(),
                self.rate.NotPair(), self.rate.FiveOfAKind(), self.rate.NotPair(), ]

    def isStraight(self, hand1, hand2, hand3, hand4, hand5):
        handNum = (hand1 | hand2 | hand3 | hand4 | hand5) & (0x1fff)

        checkbit = int(handNum / (handNum & (-handNum)))
        if (checkbit == 0x1f):
            return True

        if checkbit == 0x1e01:
            return True

        if not (poker.cards.Cards.JOKER in [hand1, hand2, hand3, hand4, hand5]):
            return False

        if bitCount(checkbit & 0x1f) == 4:
            return True

        if bitCount(checkbit & 0x1e01) == 4:
            return True

        return False

    def isFlush(self, hand1, hand2, hand3, hand4, hand5):
        return (hand1 & hand2 & hand3 & hand4 & hand5 & (0xf0000)) > 0

    def isRoyalStraightFlush(self, hand1, hand2, hand3, hand4, hand5):
        if (poker.cards.Cards.JOKER in [hand1, hand2, hand3, hand4, hand5]):
            return False

        return (hand1 | hand2 | hand3 | hand4 | hand5) & (0x1fff) == (0x1e01)

    def pairCount(self, hand1, hand2, hand3, hand4, hand5):
        cntList = [0] * 14
        cnt = [hand1 & (0x1fff),
               hand2 & (0x1fff),
               hand3 & (0x1fff),
               hand4 & (0x1fff),
               hand5 & (0x1fff)]

        for c in cnt:
            cntList[mylog2(c)] += 1

        return max(cntList) + cntList[13], len([i for i in cntList if i > 1])


@lru_cache(maxsize=None)
def bitCount(x):
    # import gmpy2
    # return gmpy2.popcount(x)
    return bin(x).count("1")


@lru_cache(maxsize=None)
def mylog2(x):
    # Joker
    if x == 0:
        return 13

    return int(math.log2(x))


class Rate1000:
    @lru_cache(maxsize=None)
    def NotPair(self):
        return -1

    @lru_cache(maxsize=None)
    def HighCard(self):
        return 0

    @lru_cache(maxsize=None)
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


if __name__ == '__main__':
    pass
