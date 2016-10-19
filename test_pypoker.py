import unittest
from pypoker import Card
from pypoker import Hand
from pypoker import PokerRules


class TestCard(unittest.TestCase):

    def setUp(self):
        self.suit = 'C'
        self.invalid_suit = 'X'
        self.value = 'A'
        self.invalid_value = 'X'
        self.card = Card(self.value, self.suit)

    def test__init__(self):
        self.assertEquals(self.card.suit, self.suit)
        self.assertEquals(self.card.value, self.value)

    def test__init__raise_error(self):
        with self.assertRaises(ValueError):
            Card(self.value, self.invalid_suit)

        with self.assertRaises(ValueError):
            Card(self.invalid_value, self.suit)

    def test_is_valid_suit(self):
        self.assertTrue(Card.is_valid_suit(self.suit))
        self.assertFalse(Card.is_valid_suit(self.invalid_suit))

    def test_is_valid_value(self):
        self.assertTrue(Card.is_valid_value(self.value))
        self.assertFalse(Card.is_valid_value(self.invalid_value))

    def test_is_valid_card_when_is_invalid(self):
        self.assertFalse(Card.is_valid_card(self.suit, self.invalid_value))
        self.assertFalse(Card.is_valid_card(self.invalid_suit, self.value))
        self.assertFalse(
            Card.is_valid_card(self.invalid_suit, self.invalid_value)
        )

    def test_is_valid_card_when_is_valid(self):
        self.assertTrue(Card.is_valid_card(self.value, self.suit))

    def test_parse_from_string(self):
        card = Card.parse_from_string('4C')
        self.assertEquals(card.suit, 'C')
        self.assertEquals(card.value, '4')

    def test_parse_from_string_when_has_invalid_string(self):
        with self.assertRaises(ValueError):
            Card.parse_from_string('4')

    def test_card__cmp__(self):
        card1 = Card('4', 'C')
        card2 = Card('T', 'C')

        self.assertTrue(card1 < card2)
        self.assertTrue(card2 > card1)
        self.assertTrue(card1 == card1)


class TestHand(unittest.TestCase):

    def setUp(self):
        self.cards_string = '4D 4D 4D 7H 8D'
        self.expected_cards = [
            Card('4', 'D'),
            Card('4', 'D'),
            Card('4', 'D'),
            Card('7', 'H'),
            Card('8', 'D'),
        ]

    def test__init__(self):
        self.hand = Hand(self.expected_cards)
        self.assertEquals(self.hand.cards, self.expected_cards)

    def test__str__(self):
        hand = Hand(self.expected_cards)
        self.assertEquals(
            str(hand),
            "<hand [4D, 4D, 4D, 7H, 8D], 'Straight Flush'>"
        )

    def test_parse_cards_string(self):
        cards = Hand.parse_cards_string(self.cards_string)
        for index, card in enumerate(cards):
            expected_card = self.expected_cards[index]
            self.assertEquals(expected_card.suit, card.suit)
            self.assertEquals(expected_card.value, card.value)

    def test_from_string(self):
        hand = Hand.from_string(self.cards_string)
        self.assertIsInstance(hand, Hand)

    def test_from_string_check_the_amount_of_cards(self):
        with self.assertRaises(ValueError):
            Hand.from_string(self.cards_string[:3])

    def test_amount_of_cards(self):
        hand = Hand()
        self.assertEquals(hand.amount_of_cards(), 0)

        hand.cards = self.expected_cards
        self.assertEquals(hand.amount_of_cards(), 5)

    def test_has_correct_amount_of_cards(self):
        hand = Hand()
        self.assertFalse(hand.has_correct_amount_of_cards())

        hand.cards = self.expected_cards
        self.assertTrue(hand.has_correct_amount_of_cards())


class TestPokerRules(unittest.TestCase):
    def test_is_straight_flush(self):
        hand = Hand([
            Card('T', 'D'),
            Card('J', 'D'),
            Card('Q', 'D'),
            Card('A', 'D'),
            Card('K', 'D'),
        ])
        self.assertTrue(PokerRules.is_royal_flush(hand))

    def test_is_straight_flush(self):
        hand = Hand([
            Card('2', 'D'),
            Card('3', 'D'),
            Card('6', 'D'),
            Card('4', 'D'),
            Card('5', 'D'),
        ])

        self.assertTrue(PokerRules.is_straight_flush(hand))

    def test_is_four_of_a_kind(self):
        hand = Hand([
            Card('2', 'C'),
            Card('3', 'D'),
            Card('3', 'H'),
            Card('3', 'S'),
            Card('3', 'D'),
        ])

        self.assertTrue(PokerRules.is_four_of_a_kind(hand))


    def test_is_full_house(self):
        hand = Hand([
            Card('2', 'C'),
            Card('3', 'S'),
            Card('2', 'D'),
            Card('3', 'D'),
            Card('2', 'H'),
        ])

        self.assertTrue(PokerRules.is_full_house(hand))

    def test_is_flush(self):
        hand = Hand([
            Card('A', 'D'),
            Card('2', 'D'),
            Card('3', 'D'),
            Card('4', 'D'),
            Card('5', 'D')
        ])

        self.assertTrue(PokerRules.is_flush(hand))

    def test_is_straight(self):
        hand = Hand([
            Card('2', 'C'),
            Card('3', 'D'),
            Card('6', 'D'),
            Card('4', 'H'),
            Card('5', 'S'),
        ])

        self.assertTrue(PokerRules.is_straight(hand))

    def test_is_tree_of_a_kind(self):
        hand = Hand([
            Card('2', 'C'),
            Card('2', 'D'),
            Card('3', 'S'),
            Card('4', 'D'),
            Card('2', 'H'),
        ])

        self.assertTrue(PokerRules.is_tree_of_a_kind(hand))

    def test_is_two_pair(self):
        hand = Hand([
            Card('2', 'C'),
            Card('2', 'D'),
            Card('3', 'S'),
            Card('4', 'D'),
            Card('3', 'H'),
        ])

        self.assertTrue(PokerRules.is_two_pair(hand))

    def test_is_one_pair(self):
        hand = Hand([
            Card('2', 'C'),
            Card('T', 'D'),
            Card('6', 'S'),
            Card('4', 'D'),
            Card('2', 'H'),
        ])

        self.assertTrue(PokerRules.is_one_pair(hand))

    def test_is_high_card(self):
        hand = Hand([
            Card('2', 'C'),
            Card('T', 'D'),
            Card('6', 'S'),
            Card('4', 'D'),
            Card('8', 'H'),
        ])

        self.assertTrue(PokerRules.is_high_card(hand))


if __name__ == '__main__':
    #unittest.main()

    hand = Hand([
        Card('2', 'C'),
        Card('2', 'D'),
        Card('4', 'S'),
        Card('4', 'D'),
        Card('9', 'H'),
    ])

    hand2 = Hand([
        Card('2', 'C'),
        Card('2', 'D'),
        Card('4', 'S'),
        Card('4', 'D'),
        Card('8', 'H'),
    ])

    hand = Hand([
        Card('3', 'C'),
        Card('T', 'D'),
        Card('J', 'S'),
        Card('K', 'D'),
        Card('A', 'H'),
    ])

    hand2 = Hand([
        Card('2', 'C'),
        Card('T', 'D'),
        Card('J', 'S'),
        Card('K', 'D'),
        Card('A', 'H'),
    ])

    print hand > hand2
