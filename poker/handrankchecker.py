import math
import collections
import poker.calc
import poker.rate
from functools import lru_cache


class HandRankChecker:

    def __init__(self, r):
        self.rate = r
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

        return checkbit in [0b1111, 0b11101, 0b11011, 0b10111,
                            0b1110000000001, 0b1011000000001,
                            0b1101000000001, 0b0110000000001]

    def isFlush(self, hand1, hand2, hand3, hand4, hand5):
        return (hand1 & hand2 & hand3 & hand4 & hand5 & (0xf0000)) > 0

    def isRoyalStraightFlush(self, hand1, hand2, hand3, hand4, hand5):
        if (poker.cards.Cards.JOKER in [hand1, hand2, hand3, hand4, hand5]):
            return False

        return (hand1 | hand2 | hand3 | hand4 | hand5) & (0x1fff) == (0x1e01)


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


if __name__ == '__main__':
    pass
