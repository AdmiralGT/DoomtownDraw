import DoomtownCard
__author__ = 'AdmiralGT'


class DoomtownCardFactory:
    @staticmethod
    def create_card(value, suit):
        return DoomtownCard.DoomtownCard(False, suit, value)

    @staticmethod
    def create_joker():
        return DoomtownCard.DoomtownCard(True)
