from DoomtownCard import DoomtownSuit
__author__ = 'AdmiralGT'


class DoomtownDrawRank:
    def __init__(self, hand, debug):
        self.hand = hand
        self.debug = debug

    # Determine the hand rank of this hand
    def get_rank(self):
        cheating = self.get_hand_rank(self.hand)
        self.legal_hand = self.remove_duplicate_cards(self.hand)
        legal = self.get_hand_rank(self.legal_hand)
        return cheating, legal

    # Determine the hand rank of this hand
    def get_hand_rank(self, hand):
        if self.debug:
            self.print_hand(self.hand)
        if len(hand) < 5:
            return 0

        number_of_jokers = self.remove_jokers_from_hand(hand)
        cards_by_value = self.get_cards_by_value(hand)
        cards_by_suit = self.get_cards_by_suit(hand)
        cards_of_value = self.get_number_of_each_value(hand)
        return self.determine_hand_rank(hand, cards_by_value, cards_by_suit, cards_of_value, number_of_jokers)

    # Determine the hand rank of this hand
    def determine_hand_rank(self, hand, cards_by_value, cards_by_suit, cards_of_value, num_jokers):
        if self.is_dead_mans_hand(hand, num_jokers):
            return 11
        if self.is_x_of_a_kind(5, cards_by_value, num_jokers):
            return 10
        if self.is_straight_flush(cards_by_suit, num_jokers):
            return 9
        if self.is_x_of_a_kind(4, cards_by_value, num_jokers):
            return 8
        if self.is_x_y(3, 2, cards_of_value, num_jokers):
            return 7
        if self.is_flush(cards_by_suit, num_jokers):
            return 6
        if self.is_straight(hand, num_jokers):
            return 5
        if self.is_x_of_a_kind(3, cards_by_value, num_jokers):
            return 4
        if self.is_x_y(2, 2, cards_of_value, num_jokers):
            return 3
        if self.is_x_of_a_kind(2, cards_by_value, num_jokers):
            return 2
        return 1

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
            if len(cards_by_suit[suit]) >= 5:
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
            if len(value) + num_jokers > num_kind:
                return True
        return False

    # Create a list of cards of each value
    @staticmethod
    def get_cards_by_value(hand):
        cards_by_value = {}
        for ii in range(1, 13):
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
            for jj in range(1, 13):
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
        for card in hand:
            if card.joker:
                jokers.append(card)

        for card in jokers:
            hand.remove(card)

        return len(jokers)

    # Prints a hand, useful for debugging
    @staticmethod
    def print_hand(hand):
        s = 'Hand: '
        for card in hand:
            s += str(card)
            s += ' '
        print(s)

    # An attempt to remove duplicate cards so as to disallow cheating hands. Currently not working
    @staticmethod
    def remove_duplicate_cards(hand):
        index = len(hand)
        cards_to_remove = []
        for card in hand:
            index -= 1

            if index is 0:
                break

            for check_card in hand[-index:]:
                if card.value == check_card.value and card.suit == check_card.suit and card.joker and \
                                check_card not in cards_to_remove:
                    cards_to_remove.append(check_card)

        for card in cards_to_remove:
            hand.remove(card)

        return hand
