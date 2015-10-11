import DoomtownCardFactory
import DoomtownDrawRank
import random
import argparse

__author__ = 'AdmiralGT'


class DoomtownDraw:
    def __init__(self):
        self.card_factory = DoomtownCardFactory.DoomtownCardFactory()
        self.deck = []
        self.debug = False
        self.stud = 2
        self.num_iterations = 10000
        self.ranks = {0: 'No hand', 1: 'High card', 2: 'One Pair', 3: 'Two Pair', 4: 'Three of a kind', 5: 'Straight',
                      6: 'Flush', 7: 'Full House', 8: 'Four of a kind', 9: 'Straight Flush', 10: 'Five of a kind',
                      11: 'Dead Mans Hand'}

    def import_deck(self, deck_file):
        count = 0
        num_jokers = 0
        for line in deck_file:
            line = line.rstrip()
            split_line = line.split(',')
            if len(split_line) < 2 and line.lower() != 'joker':
                raise ImportError('Error reading line %s' % str(line))
            count += 1

            if line.lower() == 'joker':
                num_jokers += 1
                self.deck.append(self.card_factory.create_joker())
            else:
                self.deck.append(self.card_factory.create_card(int(split_line[0]), split_line[1]))
        if num_jokers > 2:
            raise ImportError('Error, too many jokers in deck %s' % str(deck_file.name))
        if count < 46:
            raise ImportError('Error, not enough cards in deck %s' % str(deck_file.name))
        if count > 54:
            raise ImportError('Error, too many cards in deck %s' % str(deck_file.name))

    def determine_hand_ranks(self):
        cheating_sum_ranks = 0
        legal_sum_ranks = 0
        cheating_num_per_rank = {}
        legal_num_per_rank = {}

        for ii in range(0, 12):
            cheating_num_per_rank[ii] = 0
            legal_num_per_rank[ii] = 0

        for ii in range(0, self.num_iterations):
            random.shuffle(self.deck)
            draw_rank = DoomtownDrawRank.DoomtownDrawRank(self.deck[:5+self.stud], self.card_factory, self.debug)
            cheating_hand_rank, legal_hand_rank = draw_rank.get_rank()
            cheating_sum_ranks += cheating_hand_rank
            cheating_num_per_rank[cheating_hand_rank] += 1
            legal_sum_ranks += legal_hand_rank
            legal_num_per_rank[legal_hand_rank] += 1

        print('Average Cheating hand rank: %f' % (cheating_sum_ranks/self.num_iterations))
        print('Average Legal hand rank: %f' % (legal_sum_ranks/self.num_iterations))

        print('Cheating Hand rank breakdown')
        for ii in range(0, 12):
            print('{:16s}: {:d}'.format(self.ranks[ii], cheating_num_per_rank[ii]))

        print('Legal Hand rank breakdown')
        for ii in range(0, 12):
            print('{:16s}: {:d}'.format(self.ranks[ii], legal_num_per_rank[ii]))

    def main(self):
        parser = argparse.ArgumentParser(description="Calculate Doomtown Hand ranks.")
        parser.add_argument('filename', type=argparse.FileType('r'),
                            help='The file containing the deck to evaluate')
        parser.add_argument('--stud', type=int, action='store', help='The number of stud bullets in the posse.')
        parser.add_argument('--iterations', type=int, action='store',
                            help='The number of iterations to simulate hands for')
        parser.add_argument('--debug', action='store_true', help='Print debugging information')
        args = parser.parse_args()

        self.read_arguments(args)

        print("Importing Deck")
        try:
            self.import_deck(args.filename)
        except ImportError as e:
            print(e.msg)
            exit()

        print("Determining Hand Ranks")
        self.determine_hand_ranks()

    def read_arguments(self, args):
        if args.debug:
            self.debug = True

        if args.stud:
            self.stud = args.stud

        if args.iterations:
            self.num_iterations = args.iterations


if __name__ == '__main__':
    doomtown_draw = DoomtownDraw()
    DoomtownDraw.main(doomtown_draw)
