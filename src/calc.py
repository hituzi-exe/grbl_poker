import numpy as np


class Calc:

    # (0x2c000 == 0b1111 0000 0000 0000 0000)
    JOKER = 0xF0000

    def createDeck(self):
        # S = suit bit, N = num bit
        # card : SSSS xxxN NNNN NNNN NNNN
        num = (0x0001 << np.arange(13, dtype=np.int32))
        suit = 0x0001 << (np.arange(4, dtype=np.int32) + 16)

        numx, suitx = np.ix_(num, suit)
        deck = suitx + numx

        return np.append(deck.flatten(), Calc.JOKER)

    def getMaxExpectation(self, hand1, hand2, hand3, hand4, hand5):
        return -1


class HandRankChecker:

    def getHandRank(self, hand1, hand2, hand3, hand4, hand5):
        return -1

    def isStraight(self, hand1, hand2, hand3, hand4, hand5):
        return False

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


def main():
    c = Calc()
    # print(c.createDeck())


if __name__ == '__main__':
    main()
