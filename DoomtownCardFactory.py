from DoomtownCard import DoomtownJoker
import DoomtownCard
__author__ = 'AdmiralGT'


class DoomtownCardFactory:
    @staticmethod
    def create_card(value, suit):
        return DoomtownCard.DoomtownCard(DoomtownJoker.NotJoker, suit, value)

    @staticmethod
    def create_joker(joker_type):
        return DoomtownCard.DoomtownCard(joker_type)
