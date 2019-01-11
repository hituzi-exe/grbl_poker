import math
import numpy as np
from functools import lru_cache


class Cards:

    # (0x2c000 == 0b1111 0000 0000 0000 0000)
    JOKER = 0xF0000

    def createDeck(self):
        # S = suit bit(sdhc), N = num bit(a23456789tjqk)
        # card : chds ---k qjt9 8765 432a
        num = (0x0001 << np.arange(13, dtype=np.int32))
        suit = 0x0001 << (np.arange(4, dtype=np.int32) + 16)

        numx, suitx = np.ix_(num, suit)
        deck = suitx + numx

        return np.append(deck.flatten(), Cards.JOKER)

    def convert(self, hand):
        if hand == 'J':
            return Cards.JOKER

        suits = list('sdhc')
        nums = list('123456789tjqk')
        suit, num = list(hand)

        try:
            return (1 << (suits.index(suit) + 16)) | (1 << nums.index(num))
        except ValueError as ex:
            return (-1)

    def convert2(self, hand):
        if hand == Cards.JOKER:
            return 'J'

        suits = (hand & 0xf0000) >> 16
        num = hand & 0x01fff

        suitsStr = list('sdhc')
        numsStr = list('123456789tjqk')

        return suitsStr[mylog2(suits)] + numsStr[mylog2(num)]


@lru_cache(maxsize=None)
def mylog2(x):
    return int(math.log2(x))


if __name__ == '__main__':
    pass
