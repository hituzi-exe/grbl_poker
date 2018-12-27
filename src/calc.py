import numpy as np

import time


class Calc:
    def createDeck(self):
        # (0x2001 == 0b10 0000 0000 0001)
        # (0x3fff == 0b11 1111 1111 1111)
        num = (0x2001 << np.arange(13, dtype=np.int32)) & 0x3fff
        suit = 0x0001 << (np.arange(4, dtype=np.int32) + 14)

        numx, suitx = np.ix_(num, suit)
        deck = suitx + numx

        return deck.flatten()

    def getMaxExpectation(self, hand1, hand2, hand3, hand4, hand5):
        return 0

    def getHandRank(self, hand1, hand2, hand3, hand4, hand5):
        pass

#   一番右側から連続してる0の数だけ右にシフト
#   x / (x & -x)


def main():
    c = Calc()
    c.createDeck()


if __name__ == '__main__':
    main()
