import math
import collections
import src.calc
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

        if flushFlg & straightFlg:
            if self.isRoyalStraightFlush(hand1, hand2, hand3, hand4, hand5):
                return self.rate.RoyalStraightFlush()
            else:
                return self.rate.StraightFlush()

        if flushFlg:
            return self.rate.Flush()

        if straightFlg:
            return self.rate.Straight()

        return self.rate.HighCard()

    def getRateNumOfAKind(self, hand1, hand2, hand3, hand4, hand5):
        handNum = (hand1 | hand2 | hand3 | hand4 | hand5) & (0x1fff)
        bitNum = self.bitCount(handNum)

        if bitNum == 5:
            return self.rate.NotPair()

        pairMax, pairNum = self.pairCount(hand1, hand2, hand3, hand4, hand5)

        if (src.calc.Cards.JOKER in [hand1, hand2, hand3, hand4, hand5]):
            pairMax += 1

        return self.NumOfAKindMap[pairNum + (pairMax - 1) * 3]

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

        checkbit = int(handNum / (handNum & (-handNum)))
        if (checkbit == 0x1f):
            return True

        if not (src.calc.Cards.JOKER in [hand1, hand2, hand3, hand4, hand5]):
            return False

        if self.bitCount(checkbit & 0x1f) == 4:
            return True

        if self.bitCount(checkbit & 0x1e01) == 4:
            return True

        return False

    def isFlush(self, hand1, hand2, hand3, hand4, hand5):
        return (hand1 & hand2 & hand3 & hand4 & hand5 & (0xf0000)) > 0

    def isRoyalStraightFlush(self, hand1, hand2, hand3, hand4, hand5):
        if (src.calc.Cards.JOKER in [hand1, hand2, hand3, hand4, hand5]):
            return False

        return (hand1 | hand2 | hand3 | hand4 | hand5) & (0x1fff) == (0x1e01)

    def bitCount(self, x):
        # import gmpy2
        # return gmpy2.popcount(x)
        return bin(x).count("1")

    def pairCount(self, hand1, hand2, hand3, hand4, hand5):

        cntList = [0] * 13
        cnt = [x & (0x1fff) for x in [hand1, hand2, hand3, hand4, hand5]]

        for c in cnt:
            if c == 0:
                continue
            cntList[mylog2(c)] += 1

        return max(cntList), len([i for i in cntList if i > 1])

    def pairCount_old1(self, hand1, hand2, hand3, hand4, hand5):
        cnt = [x & (0x1fff) for x in [hand1, hand2, hand3, hand4, hand5]]
        values, counts = zip(*collections.Counter(cnt).most_common())
        return max(counts), len([i for i in counts if i > 1])


@lru_cache(maxsize=None)
def mylog2(x):
    return int(math.log2(x))


class Rate1000:
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


if __name__ == '__main__':
    pass
