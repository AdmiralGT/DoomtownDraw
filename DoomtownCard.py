from enum import Enum
__author__ = 'AdmiralGT'


class DoomtownSuit(Enum):
    Hearts = 'H'
    Clubs = 'C'
    Diamonds = 'D'
    Spades = 'S'


class DoomtownCard(object):
    def __init__(self, is_joker, suit=None, value=None):

        self.joker = is_joker
        if is_joker:
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
        if self.joker:
            return 'Joker'
        return '%s%s' % (self.value, self.suit.value)

    def is_suit(self, suit):
        if self.joker or self.suit == suit:
            return True
        return False

    def is_value(self, value):
        if self.joker or self.value == value:
            return True
        return False
