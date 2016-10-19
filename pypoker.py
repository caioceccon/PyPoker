class Card(object):
    SUITS = {
        'C': True,
        'D': True,
        'H': True,
        'S': True
    }

    VALUES = {
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        'T': 10,
        'J': 11,
        'Q': 12,
        'K': 13,
        'A': 14
    }

    def __init__(self, value, suit):
        if not self.is_valid_card(value, suit):
            raise ValueError('Invalid suit or value %s%s' % (value, suit))

        self.value = value.upper()
        self.suit = suit.upper()

    def __str__(self):
        return '%s%s' % (self.value, self.suit)

    def __repr__(self):
        return self.__str__()

    def __cmp__(self, other):
        return cmp(self.numeric_value, other.numeric_value)

    @classmethod
    def is_valid_suit(cls, suit):
        return bool(cls.SUITS.get(suit))

    @classmethod
    def is_valid_value(cls, value):
        return bool(cls.VALUES.get(value))

    @classmethod
    def is_valid_card(cls, value, suit):
        return cls.is_valid_suit(suit) and cls.is_valid_value(value)

    @classmethod
    def parse_from_string(cls, card_string):
        if len(card_string) < 2:
            raise ValueError('Missing suit or value for Card %s' % card_string)

        suit = card_string[1]
        value = card_string[0]
        return cls(value, suit)

    @property
    def numeric_value(self):
        return self.VALUES.get(self.value)


class Hand(object):
    MAX_CARDS = 5

    def __init__(self, cards=[]):
        self.cards = cards

    def __str__(self):
        return "<hand %s, '%s'>" % (self.cards, self.hand_value)

    def __repr__(self):
        return self.__str__()

    def __cmp__(self, other_hand):
        hand_value = PokerRules.get_numeric_value_by_hand(self)
        other_hand_value = PokerRules.get_numeric_value_by_hand(other_hand)

        if hand_value == other_hand_value:
            return PokerRules.cmp_hands(self, other_hand, hand_value)
        return cmp(hand_value, other_hand_value)

    @classmethod
    def parse_cards_string(cls, cards_string, cards=[], number_of_cards=0):
        if not cards_string or number_of_cards >= cls.MAX_CARDS:
            return cards

        card = Card.parse_from_string(cards_string[:2])

        return cls.parse_cards_string(
            cards_string[3:],
            cards + [card],
            number_of_cards + 1
        )

    @classmethod
    def from_string(cls, cards_string):
        hand = Hand(cls.parse_cards_string(cards_string))
        if not hand.has_correct_amount_of_cards():
            raise ValueError('5 cards required %s given' % hand.amount_of_cards)
        return hand

    @property
    def hand_value(self):
        return PokerRules.get_value_by_hand(self)

    def amount_of_cards(self):
        return len(self.cards)

    def has_correct_amount_of_cards(self):
        return self.amount_of_cards() == 5

    @property
    def sorted_cards(self):
        return sorted(self.cards)


class PokerRules(object):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    TREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10

    VALUES = {
        HIGH_CARD: 'High Card',
        ONE_PAIR: 'One Pair',
        TWO_PAIR: 'Two Pair',
        TREE_OF_A_KIND: 'Tree of a Kind',
        STRAIGHT: 'Straight',
        FLUSH: 'Flush',
        FULL_HOUSE: 'Full House',
        FOUR_OF_A_KIND: 'Four of a Kind',
        STRAIGHT_FLUSH: 'Straight Flush',
        ROYAL_FLUSH: 'Royal Flush'
    }

    @classmethod
    def _get_cards_dict(cls, hand):
        cards_dict = {}

        for card in hand.cards:
            numeric_value = card.numeric_value
            cards_dict[numeric_value] = cards_dict.get(numeric_value, 0) + 1

        return cards_dict

    @classmethod
    def _get_amount_of_a_kind(cls, hand):
        return cls._get_cards_dict(hand).values()

    @classmethod
    def is_royal_flush(cls, hand):
        return (hand.sorted_cards[0].numeric_value == 10 and
                cls.is_straight_flush(hand))

    @classmethod
    def is_straight_flush(cls, hand):
        return cls.is_flush(hand) and cls.is_straight(hand)

    @classmethod
    def is_four_of_a_kind(cls, hand):
        if 4 in cls._get_amount_of_a_kind(hand):
            return True

        return False

    @classmethod
    def is_full_house(cls, hand):
        return all(x in cls._get_amount_of_a_kind(hand) for x in [2, 3])

    @classmethod
    def is_flush(cls, hand):
        first_card = hand.cards[0]
        suits = [first_card.suit]

        for card in hand.cards[1:]:
            if card.suit in suits:
                suits.append(card.suit)

        if len(suits) == hand.MAX_CARDS:
            return True

        return False

    @classmethod
    def is_straight(cls, hand):
        cards = hand.sorted_cards
        previous_card = cards[0]

        for card in cards[1:]:
            if not card.numeric_value == previous_card.numeric_value + 1:
                return False
            previous_card = card

        return True

    @classmethod
    def is_tree_of_a_kind(cls, hand):
        amount_of_a_kind = cls._get_amount_of_a_kind(hand)
        if amount_of_a_kind.count(3) == 1 and amount_of_a_kind.count(1) == 2:
            return True

        return False

    @classmethod
    def is_two_pair(cls, hand):
        if cls._get_amount_of_a_kind(hand).count(2) == 2:
            return True

        return False

    @classmethod
    def is_one_pair(cls, hand):
        if cls._get_amount_of_a_kind(hand).count(2) == 1:
            return True

        return False

    @classmethod
    def is_high_card(cls, hand):
        if cls._get_amount_of_a_kind(hand).count(1) == 5:
            return True

        return False

    @classmethod
    def _get_hand_is_methods(cls):
        return [
            cls.is_royal_flush, cls.is_straight_flush,
            cls.is_four_of_a_kind, cls.is_full_house,
            cls.is_flush, cls.is_straight,
            cls.is_tree_of_a_kind, cls.is_two_pair,
            cls.is_one_pair, cls.is_high_card
        ]

    @classmethod
    def _get_kind_by_amount(cls, hand):
        hand_dict = cls._get_cards_dict(hand)
        return {v: k for k, v in hand_dict.iteritems()}

    @classmethod
    def untie_royal_flush(cls, hand, other_hand):
        return cmp(cls.ROYAL_FLUSH, cls.ROYAL_FLUSH)

    @classmethod
    def untie_straight_flush(cls, hand, other_hand):
        return cls.untie_straight(hand, other_hand)

    @classmethod
    def untie_four_of_a_kind(cls, hand, other_hand):
        hand_four_of_kind = cls._get_kind_by_amount(hand)
        other_hand_four_of_kind = cls._get_kind_by_amount(other_hand)

        if hand_four_of_kind[4] == other_hand_four_of_kind[4]:
            return cmp(hand_four_of_kind[1], other_hand_four_of_kind[1])

        return cmp(hand_four_of_kind[4], other_hand_four_of_kind[4])

    @classmethod
    def untie_full_house(cls, hand, other_hand):
        hand_four_of_kind = cls._get_kind_by_amount(hand)
        other_hand_four_of_kind = cls._get_kind_by_amount(other_hand)

        if hand_four_of_kind[3] == other_hand_four_of_kind[3]:
            return cmp(hand_four_of_kind[2], other_hand_four_of_kind[2])

        return cmp(hand_four_of_kind[3], other_hand_four_of_kind[3])

    @classmethod
    def untie_flush(cls, hand, other_hand):
        return cls.untie_high_card(hand, other_hand)

    @classmethod
    def untie_straight(cls, hand, other_hand):
        hand_higher_card = hand.sorted_cards[-1]
        other_hand_higher_card = other_hand.sorted_cards[-1]
        return cmp(hand_higher_card.numeric_value,
                   other_hand_higher_card.numeric_value)

    @classmethod
    def get_kicker(cls, hand, of_a_kinds):
        hand_kicker = [
            card for card
            in hand.sorted_cards
            if card.numeric_value
            not in of_a_kinds
        ]
        return hand_kicker[-1]

    @classmethod
    def untie_tree_of_a_kind(cls, hand, other_hand):
        hand_four_of_kind = cls._get_kind_by_amount(hand)
        other_hand_four_of_kind = cls._get_kind_by_amount(other_hand)

        if hand_four_of_kind[3] == other_hand_four_of_kind[3]:
            return cls.untie_high_card(hand, other_hand)

        return cmp(hand_four_of_kind[3], other_hand_four_of_kind[3])

    @classmethod
    def get_hand_pairs(cls, hand):
        cards_dict = cls._get_cards_dict(hand)
        return [kind for kind, amount in cards_dict.iteritems() if amount == 2]

    @classmethod
    def untie_two_pair(cls, hand, other_hand):
        hand_pairs = sorted(cls.get_hand_pairs(hand))
        other_hand_pairs = sorted(cls.get_hand_pairs(other_hand))

        if hand_pairs[-1] == other_hand_pairs[-1]:

            if hand_pairs[0] == other_hand_pairs[0]:

                hand_kicker = cls.get_kicker(hand, hand_pairs)
                other_hand_kicker = cls.get_kicker(other_hand, other_hand_pairs)

                return cmp(hand_kicker, other_hand_kicker)

            return cmp(hand_pairs[0], other_hand_pairs[0])

        return cmp(hand_pairs[-1], other_hand_pairs[-1])

    @classmethod
    def untie_one_pair(cls, hand, other_hand):
        hand_pairs = sorted(cls.get_hand_pairs(hand))
        other_hand_pairs = sorted(cls.get_hand_pairs(other_hand))

        if hand_pairs[0] == other_hand_pairs[0]:
            return cls.untie_high_card(hand, other_hand)

        return cmp(hand_pairs[-1], other_hand_pairs[-1])

    @classmethod
    def untie_high_card(cls, hand, other_hand):
        hand_cards = hand.sorted_cards[::-1]
        other_hand_cards = other_hand.sorted_cards[::-1]

        for index, hand_card in enumerate(hand_cards):
            other_hand_card = other_hand_cards[index]
            if hand_card != other_hand_card:

                return cmp(hand_card.numeric_value,
                           other_hand_card.numeric_value)

        return cmp(hand.sorted_cards[-1], other_hand.sorted_cards[-1])

    @classmethod
    def _hand_untie_methods(cls):
        return {
            cls.ROYAL_FLUSH: cls.untie_royal_flush,
            cls.STRAIGHT_FLUSH: cls.untie_straight_flush,
            cls.FOUR_OF_A_KIND: cls.untie_four_of_a_kind,
            cls.FULL_HOUSE: cls.untie_full_house,
            cls.FLUSH: cls.untie_flush,
            cls.STRAIGHT: cls.untie_straight,
            cls.TREE_OF_A_KIND: cls.untie_tree_of_a_kind,
            cls.TWO_PAIR: cls.untie_two_pair,
            cls.ONE_PAIR: cls.untie_one_pair,
            cls.HIGH_CARD: cls.untie_high_card
        }

    @classmethod
    def cmp_hands(cls, hand, other_hand, hand_value):
        untie_method = cls._hand_untie_methods().get(hand_value)
        return untie_method(hand, other_hand)

    @classmethod
    def _get_value_by_hand(cls, hand, hand_methods=[], result=False, count=10):

        if not hand_methods:
            return None

        hand_method = hand_methods[0]
        result = hand_method(hand)

        if result:
            return count

        return cls._get_value_by_hand(hand, hand_methods[1:], result, count - 1)

    @classmethod
    def get_numeric_value_by_hand(cls, hand):
        return cls._get_value_by_hand(hand, cls._get_hand_is_methods())

    @classmethod
    def get_value_by_hand(cls, hand):
        return cls.VALUES.get(cls.get_numeric_value_by_hand(hand))
