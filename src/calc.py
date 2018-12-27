import numpy as np

import time


class Calc:
    def createDeck(self):
        num = 1 << np.arange(13, dtype=np.int32)
        sute = 1 << (np.arange(4, dtype=np.int32) + 13)

        roopcount = 1000000

        # time1
        start = time.time()
        for i in range(0, roopcount):
            deck = np.asarray([num + n for n in sute])

        elapsed_time = time.time() - start
        print("time1:{0}".format(elapsed_time) + "[sec]")

        # time2
        start = time.time()
        for i in range(0, roopcount):
            numx, sutex = np.ix_(num, sute)
            deck2 = sutex + numx

        elapsed_time = time.time() - start
        print("time2:{0}".format(elapsed_time) + "[sec]")

        # result
        # time1:10.297203063964844[sec]
        # time2:8.98630404472351[sec]


def getMaxExpectation(self, hand1, hand2, hand3, hand4, hand5):
    return 0


def main():
    c = Calc()

    c.createDeck()


if __name__ == '__main__':
    main()
