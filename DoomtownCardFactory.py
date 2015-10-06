import DoomtownCard
__author__ = 'AdmiralGT'


class DoomtownCardFactory:
    def create_card(self, value, suit):
        return DoomtownCard.DoomtownCard(False, suit, value)

    def create_joker(self):
        return DoomtownCard.DoomtownCard(True)
