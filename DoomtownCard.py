from enum import Enum
__author__ = 'AdmiralGT'


class DoomtownSuit(Enum):
    Hearts = 'H'
    Clubs = 'C'
    Diamonds = 'D'
    Spades = 'S'


class DoomtownJoker(Enum):
    NotJoker = 0
    Base = 1
    Devils = 2


class DoomtownCard(object):
    def __init__(self, joker, suit=None, value=None):

        self.joker = joker
        if self.is_joker():
            return

        if value < 1 or value > 13:
            raise ValueError('Not a valid card')
        self.value = value

        if suit is 'C':
            self.suit = DoomtownSuit.Clubs
        elif suit is 'D':
            self.suit = DoomtownSuit.Diamonds
        elif suit is 'H':
            self.suit = DoomtownSuit.Hearts
        elif suit is 'S':
            self.suit = DoomtownSuit.Spades
        else:
            raise ValueError('Not a valid card')

    def __str__(self):
        if self.joker == DoomtownJoker.Base:
            return 'Joker'
        elif self.joker == DoomtownJoker.Devils:
            return 'Devil\'s Joker'
        return '%s%s' % (self.value, self.suit.value)

    def is_suit(self, suit):
        if self.is_joker() or self.suit == suit:
            return True
        return False

    def is_value(self, value):
        if self.is_joker() or self.value == value:
            return True
        return False

    def is_joker(self):
        if self.joker != DoomtownJoker.NotJoker:
            return True
        return False
