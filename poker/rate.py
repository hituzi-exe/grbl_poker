from functools import lru_cache


class Rate1000:
    @lru_cache(maxsize=None)
    def NotPair(self):
        return -1

    @lru_cache(maxsize=None)
    def HighCard(self):
        return 0

    @lru_cache(maxsize=None)
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


class Rate0:
    @lru_cache(maxsize=None)
    def NotPair(self):
        return -1

    @lru_cache(maxsize=None)
    def HighCard(self):
        return 0

    @lru_cache(maxsize=None)
    def OnePair(self):
        return 1

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
