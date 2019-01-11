import os
import time
import sys
import itertools
import subprocess

import poker.rate
import poker.cards
import poker.handrankchecker


def getMaxExpectation(hand1, hand2, hand3, hand4, hand5):
    if not os.path.isfile('poker/GrblPokerVB_NET.exe '):
        return getMaxExpectation2(hand1, hand2, hand3, hand4, hand5)

    cmd = 'poker/GrblPokerVB_NET.exe {0} {1} {2} {3} {4}'.format(hand1,
                                                                 hand2,
                                                                 hand3,
                                                                 hand4,
                                                                 hand5)
    returncode = subprocess.call(cmd)

    holdHands = []
    if 0b00001 & returncode:
        holdHands.append(hand1)

    if 0b00010 & returncode:
        holdHands.append(hand2)

    if 0b00100 & returncode:
        holdHands.append(hand3)

    if 0b01000 & returncode:
        holdHands.append(hand4)

    if 0b10000 & returncode:
        holdHands.append(hand5)

    return holdHands


def getMaxExpectation2(hand1, hand2, hand3, hand4, hand5):
    cards = poker.cards.Cards()

    hands = [cards.convert(i) for i in [hand1, hand2, hand3, hand4, hand5]]
    deck = cards.createDeck().tolist()

    for hand in hands:
        deck.remove(hand)

    rate = poker.rate.Rate1000()

    checker = poker.handrankchecker.HandRankChecker(rate)
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

            if maxExp < (sumExp / sumCount):
                maxExp = (sumExp / sumCount)
                maxExpHand = hand

    return [cards.convert2(i) for i in maxExpHand]


if __name__ == '__main__':
    pass
