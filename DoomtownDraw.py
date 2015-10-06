import DoomtownCardFactory
import DoomtownDrawRank
import random
import argparse

__author__ = 'AdmiralGT'


class DoomtownDraw:
    def __init__(self):
        self.cardFactory = DoomtownCardFactory.DoomtownCardFactory()
        self.deck = []
        self.debug = False

    def import_deck(self, deck_file):
        count = 0
        num_jokers = 0
        for line in deck_file:
            line = line.rstrip()
            split_line = line.split(',')
            if len(split_line) < 2 and line != 'Joker':
                raise ImportError('Error reading line %s' % str(line))
            count += 1

            if len(split_line) == 2:
                self.deck.append(self.cardFactory.create_card(int(split_line[0]), split_line[1]))
            else:
                num_jokers += 1
                self.deck.append(self.cardFactory.create_joker())
        if num_jokers > 2:
            raise ImportError('Error, too many jokers in deck %s' % str(deck_file.name))
        if count < 47:
            raise ImportError('Error, not enough cards in deck %s' % str(deck_file.name))
        if count > 54:
            raise ImportError('Error, too many cards in deck %s' % str(deck_file.name))

    def determine_hand_ranks(self, stud):
        random.shuffle(self.deck)
        draw_rank = DoomtownDrawRank.DoomtownDrawRank(self.deck[:5+stud], self.debug)

        cheating = draw_rank.get_rank(True)
        if self.debug:
            print(cheating)
        return cheating

    def main(self):
        parser = argparse.ArgumentParser(description="Calculate Doomtown Hand ranks.")
        parser.add_argument('filename', type=argparse.FileType('r'),
                            help='The file containing the deck to evaluate')
        parser.add_argument('--stud', type=int, action='store', help='The number of stud bullets in the posse.')
        parser.add_argument('--iterations', type=int, action='store',
                            help='The number of iterations to simulate hands for')
        parser.add_argument('--debug', action='store_true', help='Print debugging information')
        args = parser.parse_args()

        if args.debug:
            self.debug = True

        stud = 2
        if args.stud:
            stud = args.stud

        print("Importing Deck")
        try:
            self.import_deck(args.filename)
        except ImportError as e:
            print(e.msg)
            exit()

        print("Determining Hand Ranks")
        num_iterations = 10000
        if args.iterations:
            num_iterations = args.iterations
        sum_ranks = 0
        num_per_rank = {}
        for ii in range(1, 12):
            num_per_rank[ii] = 0
        for ii in range(0, num_iterations):
            hand_rank = self.determine_hand_ranks(stud)
            sum_ranks += hand_rank
            num_per_rank[hand_rank] += 1
        print('Average hand rank: %f' % (sum_ranks/num_iterations))
        print('Hand rank breakdown')
        for ii in range(1, 12):
            print('Rank %d: %d' % (ii, num_per_rank[ii]))

if __name__ == '__main__':
    doomtown_draw = DoomtownDraw()
    DoomtownDraw.main(doomtown_draw)
