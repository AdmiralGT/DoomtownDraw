from DoomtownCard import DoomtownJoker
from DoomtownCard import DoomtownSuit
__author__ = 'AdmiralGT'


class DoomtownDrawRank:
    def __init__(self, hand, card_factory, debug):
        self.debug = debug
        self.card_factory = card_factory
        self.legal_hand = self.copy_hand(hand)
        self.cheating_hand = self.copy_hand(hand)

    # Create a local copy of a hand
    def copy_hand(self, hand):
        copy_hand = []
        for card in hand:
            if card.joker == DoomtownJoker.Base:
                copy_hand.append(self.card_factory.create_joker(DoomtownJoker.Base))
            elif card.joker == DoomtownJoker.Devils:
                copy_hand.append(self.card_factory.create_joker(DoomtownJoker.Devils))
            else:
                copy_hand.append(self.card_factory.create_card(card.value, card.suit.value))
        return copy_hand

    # Determine the hand rank of this hand
    def get_rank(self):
        cheating = self.get_hand_rank(self.cheating_hand)
        if self.debug:
            print(cheating)
        self.legal_hand = self.remove_illegal_cards(self.legal_hand)
        legal = self.get_hand_rank(self.legal_hand)
        if self.debug:
            print(legal)
        return cheating, legal

    # Determines the lowball hand rank of this hand
    def get_lowball_rank(self):
        hand_rank = self.get_hand_rank(self.cheating_hand, True)
        if self.debug:
            print(hand_rank)
        legal = self.is_hand_legal(self.cheating_hand)
        return hand_rank, legal

    # Determines if a hand is legal or not
    def is_hand_legal(self, hand):
        illegal_cards = self.get_illegal_cards(hand)
        if len(illegal_cards) > 0:
            return False
        return True

    # Determine the hand rank of this hand
    def get_hand_rank(self, hand, lowball=False):
        if self.debug:
            self.print_hand(hand)
        if len(hand) < 5:
            return 0

        num_jokers, num_devils = self.remove_jokers_from_hand(hand)
        if lowball:
            # In lowball, Jokers never improve our hand, hence count them as 0. However, we must still remember how
            # many Devil's Jokers we had since these will increase our hand rank.
            num_jokers = 0
        cards_by_value = self.get_cards_by_value(hand)
        cards_by_suit = self.get_cards_by_suit(hand)
        cards_of_value = self.get_number_of_each_value(hand)
        return self.determine_hand_rank(hand, cards_by_value, cards_by_suit, cards_of_value, num_jokers, num_devils)

    # Determine the hand rank of this hand
    def determine_hand_rank(self, hand, cards_by_value, cards_by_suit, cards_of_value, num_jokers, num_devils):
        hand_rank = 1
        if self.is_dead_mans_hand(hand, num_jokers):
            hand_rank = 11
        elif self.is_x_of_a_kind(5, cards_by_value, num_jokers):
            hand_rank = 10
        elif self.is_straight_flush(cards_by_suit, num_jokers):
            hand_rank = 9
        elif self.is_x_of_a_kind(4, cards_by_value, num_jokers):
            hand_rank = 8
        elif self.is_x_y(3, 2, cards_of_value, num_jokers):
            hand_rank = 7
        elif self.is_flush(cards_by_suit, num_jokers):
            hand_rank = 6
        elif self.is_straight(hand, num_jokers):
            hand_rank = 5
        elif self.is_x_of_a_kind(3, cards_by_value, num_jokers):
            hand_rank = 4
        elif self.is_x_y(2, 2, cards_of_value, num_jokers):
            hand_rank = 3
        elif self.is_x_of_a_kind(2, cards_by_value, num_jokers):
            hand_rank = 2
        return min(11, hand_rank + (2 * num_devils))

    # Is this a Dead Man's hand?
    def is_dead_mans_hand(self, hand, num_jokers):
        num_matches = 0
        if self.hand_contains_card(hand, DoomtownSuit.Spades, 1):
            num_matches += 1
        if self.hand_contains_card(hand, DoomtownSuit.Spades, 8):
            num_matches += 1
        if self.hand_contains_card(hand, DoomtownSuit.Clubs, 1):
            num_matches += 1
        if self.hand_contains_card(hand, DoomtownSuit.Clubs, 8):
            num_matches += 1
        if self.hand_contains_card(hand, DoomtownSuit.Diamonds, 11):
            num_matches += 1

        if num_matches + num_jokers >= 5:
            return True
        return False

    # Is this a Straight Flush?
    def is_straight_flush(self, cards_by_suit, num_jokers):
        for suit in cards_by_suit:
            if (len(cards_by_suit[suit]) + num_jokers) >= 5:
                if self.is_straight(cards_by_suit[suit], num_jokers):
                    return True
        return False

    # Do we have a straight in this set of cards?
    def is_straight(self, cards, num_jokers):
        # A straight can only possibly start at A-9, a straight starting at 9 is 9,10,J,Q,K
        for ii in range(1, 10):
            jokers = num_jokers
            found = 0
            for jj in range(ii, ii + 5):
                if self.hand_contains_card_of_value(cards, jj):
                    found += 1
                    continue
                elif jokers > 0:
                    found += 1
                    jokers -= 1
                    continue
                else:
                    break

            if found >= 5:
                return True
        return False

    # An attempt to remove cards that make this hand cheating. This means we need to remove any duplicate cards and
    # any Devil's jokers.
    def remove_illegal_cards(self, hand):
        cards_to_remove = self.get_illegal_cards(hand)

        for card in cards_to_remove:
            hand.remove(card)

        return hand
    # Do we have a full house or two pair?
    @staticmethod
    def is_x_y(x, y, cards_by_value, num_jokers):
        if num_jokers == 2:
            if len(cards_by_value[x]) > 0:
                return True
            if len(cards_by_value[x-1]) > 0 and len(cards_by_value[y-1]) > 1:
                return True
            return False
        elif num_jokers == 1:
            if len(cards_by_value[x]) > 0 and len(cards_by_value[y-1]) > 1:
                return True
            if len(cards_by_value[x-1]) > 1 and len(cards_by_value[y]) > 0:
                return True
            return False
        else:
            if len(cards_by_value[x]) > 0 and len(cards_by_value[y]) > 1:
                return True
        return False

    # Dp we have a flush?
    @staticmethod
    def is_flush(cards_by_suit, num_jokers):
        for suit in cards_by_suit:
            if len(cards_by_suit[suit]) + num_jokers >= 5:
                return True
        return False

    # Do we have an X of a kind (5,4,3,2), we always have high card :P
    @staticmethod
    def is_x_of_a_kind(num_kind, cards_by_value, num_jokers):
        for value in cards_by_value.values():
            if len(value) + num_jokers >= num_kind:
                return True
        return False

    # Create a list of cards of each value
    @staticmethod
    def get_cards_by_value(hand):
        cards_by_value = {}
        for ii in range(1, 14):
            cards = []
            for card in hand:
                if card.is_value(ii):
                    cards.append(card)
            cards_by_value[ii] = cards
        return cards_by_value

    # Create a list of cards of each suit
    @staticmethod
    def get_cards_by_suit(hand):
        cards_by_suit = {}
        for suit in DoomtownSuit:
            cards = []
            for card in hand:
                if card.is_suit(suit):
                    cards.append(card)
            cards_by_suit[suit] = cards
        return cards_by_suit

    # Create a dictionary of how many of each value there is
    @staticmethod
    def get_number_of_each_value(hand):
        cards_of_each_value = {}
        for ii in range(1, len(hand) + 1):
            cards_of_this_value = []
            for jj in range(1, 14):
                cards_of_value = 0
                for card in hand:
                    if card.value == jj:
                        cards_of_value += 1
                    if cards_of_value >= ii:
                        break
                if cards_of_value >= ii:
                    cards_of_this_value.append(jj)
            cards_of_each_value[ii] = cards_of_this_value
        return cards_of_each_value

    # Determines if a hand contains a given card
    @staticmethod
    def hand_contains_card(hand, suit, value):
        for card in hand:
            if card.suit == suit and card.value == value:
                return True
        return False

    # Determines if a hand contains a given value
    @staticmethod
    def hand_contains_card_of_value(cards, value):
        for card in cards:
            if card.value == value:
                return True
        return False

    # Removes jokers from a hand, returns the number of jokers found
    @staticmethod
    def remove_jokers_from_hand(hand):
        jokers = []
        devils_jokers = []
        for card in hand:
            if card.is_joker():
                jokers.append(card)
            if card.joker == DoomtownJoker.Devils:
                devils_jokers.append(card)

        for card in jokers:
            hand.remove(card)

        return len(jokers), len(devils_jokers)

    # Prints a hand, useful for debugging
    @staticmethod
    def print_hand(hand):
        s = 'Hand: '
        for card in hand:
            s += str(card)
            s += ' '
        print(s)

    # A method to get duplicate cards
    @staticmethod
    def get_illegal_cards(hand):
        index = len(hand)
        cards_to_remove = []
        for card in hand:
            index -= 1

            if index is 0:
                break
            if card.is_joker:
                if card.joker == DoomtownJoker.Devils:
                    cards_to_remove.append(card)
                continue

            for check_card in hand[-index:]:
                if check_card.is_joker():
                    continue
                if card.value == check_card.value and card.suit == check_card.suit and \
                                check_card not in cards_to_remove:
                    cards_to_remove.append(check_card)
        return cards_to_remove
