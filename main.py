import poker.calc
import time
import itertools

import poker.cards
import poker.rate


def main():
    # 時間計測
    start = time.time()

    res = poker.calc.getMaxExpectation('s1', 's2', 'd3', 'd7', 'd8',)
    print(res)

    elapsed_time = time.time() - start
    print("elapsed_time:{0}".format(elapsed_time) + "[sec]")


if __name__ == '__main__':
    main()
