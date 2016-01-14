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
    # It results in much quicker computation to pass an is_joker parameter rather than performing an if test on each
    # lookup so while it looks a bit "messier" it saves us all time.
    def __init__(self, is_joker, joker, suit=None, value=None):

        self.joker_type = joker
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
        if self.joker_type == DoomtownJoker.Base:
            return 'Joker'
        elif self.joker_type == DoomtownJoker.Devils:
            return 'Devil\'s Joker'
        return '%s%s' % (self.value, self.suit.value)

    def is_suit(self, suit):
        if self.joker or self.suit == suit:
            return True
        return False

    def is_value(self, value):
        if self.joker or self.value == value:
            return True
        return False