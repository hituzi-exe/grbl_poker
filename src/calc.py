import time
import math
import itertools
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
        # 時間計測
        start = time.time()

        hands = [self.convert(i) for i in [hand1, hand2, hand3, hand4, hand5]]
        deck = self.createDeck().tolist()

        for hand in hands:
            deck.remove(hand)

        checker = HandRankChecker()
        maxExp = 0
        maxExpHand = []

        for i in [0, 1, 2, 3, 4, 5]:
            for hand in itertools.combinations(hands, i):
                sumCount = 0
                sumExp = 0

                for d in itertools.combinations(deck, 5 - i):
                    c = hand + d
                    sumExp += checker.getHandRank(c[0], c[1], c[2], c[3], c[4])
                    sumCount += 1

                if maxExp < (sumExp/sumCount):
                    maxExp = (sumExp / sumCount)
                    maxExpHand = hand

        elapsed_time = time.time() - start
        print("elapsed_time:{0}".format(elapsed_time) + "[sec]")

        return [self.convert2(i) for i in maxExpHand]

    def convert(self, hand):
        if hand == 'J':
            return Calc.JOKER

        suits = list('sdhc')
        nums = list('a23456789tjqk')
        suit, num = list(hand)

        try:
            return (1 << (suits.index(suit) + 16)) | (1 << nums.index(num))
        except ValueError as ex:
            return (-1)

    def convert2(self, hand):
        if hand == Calc.JOKER:
            return 'J'

        suits = (hand & 0xf0000) >> 16
        num = hand & 0x01fff

        suitsStr = list('sdhc')
        numsStr = list('a23456789tjqk')

        return suitsStr[int(math.log2(suits))] + numsStr[int(math.log2(num))]


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

        if (Calc.JOKER in [hand1, hand2, hand3, hand4, hand5]):
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

        if not (Calc.JOKER in [hand1, hand2, hand3, hand4, hand5]):
            return False

        if self.bitCount(checkbit & 0x1f) == 4:
            return True

        return False

    def isFlush(self, hand1, hand2, hand3, hand4, hand5):
        return (hand1 & hand2 & hand3 & hand4 & hand5 & (0xf0000)) > 0

    def isRoyalStraightFlush(self, hand1, hand2, hand3, hand4, hand5):
        if (Calc.JOKER in [hand1, hand2, hand3, hand4, hand5]):
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
            cntList[int(math.log2(c))] += 1

        return max(cntList), len([i for i in cntList if i > 1])

    def pairCount_old1(self, hand1, hand2, hand3, hand4, hand5):
        cnt = [x & (0x1fff) for x in [hand1, hand2, hand3, hand4, hand5]]
        values, counts = zip(*collections.Counter(cnt).most_common())
        return max(counts), len([i for i in counts if i > 1])


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


def main():
    c = Calc()
    res = c.getMaxExpectation('J', 's7', 'h4', 's5', 'sk',)

    print(res)


if __name__ == '__main__':
    main()
