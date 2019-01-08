import time
import math
import itertools
import src.cards
import src.handrankchecker


class Calc:

    def getMaxExpectation(self, hand1, hand2, hand3, hand4, hand5):
        cards = Cards()

        hands = [cards.convert(i) for i in [hand1, hand2, hand3, hand4, hand5]]
        deck = cards.createDeck().tolist()

        for hand in hands:
            deck.remove(hand)

        checker = src.handrankchecker.HandRankChecker()
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

        return [cards.convert2(i) for i in maxExpHand]


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
