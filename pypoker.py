SUITS = 1

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

    def  __repr__(self):
        return self.__str__()

    def __cmp__(self, other):
        return cmp(self.get_real_value(), other.get_real_value())

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

    def get_real_value(self):
        return self.VALUES.get(self.value)

    @property
    def numeric_value(self):
        return self.VALUES.get(self.value)


class Hand(object):
    MAX_CARDS = 5

    def __init__(self, cards=[]):
        self.cards = cards

    def __str__(self):
        return "<hand %s, '%s'>" % (self.cards, self.hand_value())

    def  __repr__(self):
        return self.__str__()

    def __cmp__(self, other):
        return cmp(
            PokerRules.get_value_by_hand(self),
            PokerRules.get_value_by_hand(other)
        )

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
        HIGH_CARD : 'High Card',
        ONE_PAIR : 'One Pair',
        TWO_PAIR : 'Two Pair',
        TREE_OF_A_KIND : 'Tree of a Kind',
        STRAIGHT : 'Straight',
        FLUSH : 'Flush',
        FULL_HOUSE : 'Full House',
        FOUR_OF_A_KIND : 'Four of a Kind',
        STRAIGHT_FLUSH : 'Straight Flush',
        ROYAL_FLUSH : 'Royal Flush'
    }

    @classmethod
    def _get_amount_of_a_kind(cls, hand):
        values = {}

        for card in hand.cards:
            values[card.value] = values.get(card.value, 0) + 1

        return values.values()

    @classmethod
    def is_royal_flush(cls, hand):
        return (hand.sorted_cards[0].get_real_value() == 10 and
                is_straight_flush(hand))

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
    def _get_value_by_hand(cls, hand, hand_methods=[], result=None, count=10):
        if result is not None:
            return count

        if not hand_methods:
            return None

        hand_method = hand_methods[0]
        result = hand_method(hand)

        return cls._get_value_by_hand(hand, hand_methods[1:], result, count - 1)

    @classmethod
    def get_numeric_value_by_hand(cls, hand):
        return cls._get_value_by_hand(hand, cls._get_hand_is_methods())

    @classmethod
    def get_value_by_hand(cls, hand):
        return cls.VALUES.get(cls.get_numeric_value_by_hand(hand))
