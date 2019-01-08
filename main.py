import poker.calc
import time
import itertools

import poker.cards
import poker.rate


def main():
    # 時間計測
    start = time.time()

    res = poker.calc.getMaxExpectation('J', 's7', 'h4', 's5', 'sk',)
    print(res)

    elapsed_time = time.time() - start
    print("elapsed_time:{0}".format(elapsed_time) + "[sec]")


def search():
    cards = poker.cards.Cards()
    deck = [cards.convert2(i) for i in cards.createDeck().tolist()]

    rate = poker.rate.Rate0()

    checker = poker.handrankchecker.HandRankChecker(rate)

    for d1, d2, d3, d4, d5 in itertools.combinations(deck, 5):
        print('{0},{1},{2},{3},{4}'.format(d1, d2, d3, d4, d5))

        if checker.getHandRank(cards.convert(d1),
                               cards.convert(d2),
                               cards.convert(d3),
                               cards.convert(d4),
                               cards.convert(d5),) >= 1:
            continue

        res = poker.calc.getMaxExpectation(d1, d2, d3, d4, d5)
        print(res)

        if len(res) == 0:
            return


if __name__ == '__main__':
    search()
