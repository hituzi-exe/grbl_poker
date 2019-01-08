import time
import math
import itertools
import numpy as np
import handrankchecker
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
        hands = [self.convert(i) for i in [hand1, hand2, hand3, hand4, hand5]]
        deck = self.createDeck().tolist()

        for hand in hands:
            deck.remove(hand)

        checker = handrankchecker.HandRankChecker()
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


def main():
    # 時間計測
    start = time.time()

    c = Calc()

    res = c.getMaxExpectation('J', 's7', 'h4', 's5', 'sk',)
    print(res)

    elapsed_time = time.time() - start
    print("elapsed_time:{0}".format(elapsed_time) + "[sec]")


if __name__ == '__main__':
    main()
