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
            "<hand [4D, 4D, 4D, 7H, 8D], 'Tree of a Kind'>"
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

        hand = Hand([
            Card('2', 'C'),
            Card('2', 'D'),
            Card('6', 'S'),
            Card('4', 'D'),
            Card('8', 'H'),
        ])

        self.assertFalse(PokerRules.is_high_card(hand))

    def test_untie_royal_flush(self):
        royal_flush1 = Hand([
            Card('T', 'C'),
            Card('J', 'C'),
            Card('Q', 'C'),
            Card('K', 'C'),
            Card('A', 'C'),
        ])

        royal_flush2 = Hand([
            Card('T', 'D'),
            Card('J', 'D'),
            Card('Q', 'D'),
            Card('K', 'D'),
            Card('A', 'D'),
        ])

        self.assertEquals(royal_flush1, royal_flush2)

    def test_untie_straight_flush(self):
        straight_flush1 = Hand([
            Card('9', 'C'),
            Card('T', 'C'),
            Card('J', 'C'),
            Card('Q', 'C'),
            Card('K', 'C'),
        ])

        straight_flush2 = Hand([
            Card('9', 'D'),
            Card('T', 'D'),
            Card('J', 'D'),
            Card('Q', 'D'),
            Card('K', 'D'),
        ])
        self.assertEquals(straight_flush1, straight_flush2)

        lower_straight_flush = Hand([
            Card('8', 'C'),
            Card('9', 'C'),
            Card('T', 'C'),
            Card('J', 'C'),
            Card('Q', 'C'),
        ])

        higher_straight_flush = Hand([
            Card('9', 'D'),
            Card('T', 'D'),
            Card('J', 'D'),
            Card('Q', 'D'),
            Card('K', 'D'),
        ])
        self.assertGreater(higher_straight_flush, lower_straight_flush)

    def test_untie_four_of_a_kind(self):
        four_of_a_kind1 = Hand([
            Card('9', 'C'),
            Card('9', 'D'),
            Card('9', 'H'),
            Card('9', 'S'),
            Card('K', 'C'),
        ])

        four_of_a_kind2 = Hand([
            Card('9', 'C'),
            Card('9', 'D'),
            Card('9', 'H'),
            Card('9', 'S'),
            Card('K', 'C'),
        ])
        self.assertEquals(four_of_a_kind1, four_of_a_kind2)

        lower_four_of_a_kind = Hand([
            Card('8', 'C'),
            Card('8', 'D'),
            Card('8', 'H'),
            Card('8', 'S'),
            Card('K', 'C'),
        ])

        higher_four_of_a_kind = Hand([
            Card('9', 'C'),
            Card('9', 'D'),
            Card('9', 'H'),
            Card('9', 'S'),
            Card('A', 'C'),
        ])
        self.assertGreater(higher_four_of_a_kind, lower_four_of_a_kind)

        lower_four_of_a_kind1 = Hand([
            Card('9', 'C'),
            Card('9', 'D'),
            Card('9', 'H'),
            Card('9', 'S'),
            Card('K', 'C'),
        ])

        higher_four_of_a_kind1 = Hand([
            Card('9', 'C'),
            Card('9', 'D'),
            Card('9', 'H'),
            Card('9', 'S'),
            Card('A', 'C'),
        ])
        self.assertGreater(higher_four_of_a_kind1, lower_four_of_a_kind1)

    def test_untie_full_house(self):
        full_house1 = Hand([
            Card('9', 'C'),
            Card('9', 'D'),
            Card('9', 'H'),
            Card('K', 'S'),
            Card('K', 'C'),
        ])

        full_house2 = Hand([
            Card('9', 'C'),
            Card('9', 'D'),
            Card('9', 'H'),
            Card('K', 'S'),
            Card('K', 'C'),
        ])
        self.assertEquals(full_house1, full_house2)

        lower_full_house = Hand([
            Card('7', 'C'),
            Card('7', 'D'),
            Card('7', 'H'),
            Card('K', 'S'),
            Card('K', 'C'),
        ])

        higher_full_house = Hand([
            Card('9', 'C'),
            Card('9', 'D'),
            Card('9', 'H'),
            Card('A', 'S'),
            Card('A', 'C'),
        ])
        self.assertGreater(higher_full_house, lower_full_house)

        lower_full_house1 = Hand([
            Card('9', 'C'),
            Card('9', 'D'),
            Card('9', 'H'),
            Card('K', 'S'),
            Card('K', 'C'),
        ])

        higher_full_house1 = Hand([
            Card('9', 'C'),
            Card('9', 'D'),
            Card('9', 'H'),
            Card('A', 'S'),
            Card('A', 'C'),
        ])
        self.assertGreater(higher_full_house1, lower_full_house1)

    def test_untie_flush(self):
        flush1 = Hand([
            Card('9', 'C'),
            Card('A', 'C'),
            Card('J', 'C'),
            Card('K', 'C'),
            Card('8', 'C'),
        ])

        flush2 = Hand([
            Card('9', 'C'),
            Card('A', 'C'),
            Card('J', 'C'),
            Card('K', 'C'),
            Card('8', 'C'),
        ])
        self.assertEquals(flush1, flush2)

        lower_flush = Hand([
            Card('9', 'C'),
            Card('A', 'C'),
            Card('J', 'C'),
            Card('K', 'C'),
            Card('5', 'C'),
        ])

        higher_flush = Hand([
            Card('9', 'C'),
            Card('A', 'C'),
            Card('J', 'C'),
            Card('K', 'C'),
            Card('8', 'C'),
        ])
        self.assertGreater(higher_flush, lower_flush)

    def test_untie_straight(self):
        straight1 = Hand([
            Card('2', 'C'),
            Card('3', 'D'),
            Card('4', 'H'),
            Card('5', 'S'),
            Card('6', 'S'),
        ])

        straight2 = Hand([
            Card('2', 'C'),
            Card('3', 'D'),
            Card('4', 'H'),
            Card('5', 'S'),
            Card('6', 'S'),
        ])
        self.assertEquals(straight1, straight2)

        lower_straight = Hand([
            Card('2', 'C'),
            Card('3', 'D'),
            Card('4', 'H'),
            Card('5', 'S'),
            Card('6', 'S'),
        ])

        higher_straight = Hand([
            Card('3', 'D'),
            Card('4', 'H'),
            Card('5', 'S'),
            Card('6', 'S'),
            Card('7', 'C'),
        ])
        self.assertGreater(higher_straight, lower_straight)

    def test_untie_tree_of_a_kind(self):
        tree_of_a_kind1 = Hand([
            Card('2', 'C'),
            Card('2', 'D'),
            Card('2', 'H'),
            Card('5', 'S'),
            Card('6', 'S'),
        ])

        tree_of_a_kind2 = Hand([
            Card('2', 'C'),
            Card('2', 'D'),
            Card('2', 'H'),
            Card('5', 'S'),
            Card('6', 'S'),
        ])
        self.assertEquals(tree_of_a_kind1, tree_of_a_kind2)

        lower_tree_of_a_kind = Hand([
            Card('2', 'D'),
            Card('4', 'S'),
            Card('2', 'H'),
            Card('6', 'S'),
            Card('2', 'C'),
        ])

        higher_tree_of_a_kind = Hand([
            Card('2', 'D'),
            Card('5', 'S'),
            Card('2', 'H'),
            Card('6', 'S'),
            Card('2', 'C'),
        ])
        self.assertGreater(higher_tree_of_a_kind, lower_tree_of_a_kind)

    def test_untie_two_pair(self):
        two_pair1 = Hand([
            Card('2', 'C'),
            Card('6', 'S'),
            Card('2', 'D'),
            Card('5', 'H'),
            Card('5', 'S'),
        ])

        two_pair2 = Hand([
            Card('2', 'C'),
            Card('6', 'S'),
            Card('5', 'H'),
            Card('2', 'D'),
            Card('5', 'S'),
        ])
        self.assertEquals(two_pair1, two_pair2)

        lower_two_pair = Hand([
            Card('2', 'C'),
            Card('2', 'D'),
            Card('5', 'S'),
            Card('5', 'H'),
            Card('9', 'S'),
        ])

        higher_two_pair = Hand([
            Card('2', 'C'),
            Card('2', 'D'),
            Card('6', 'H'),
            Card('6', 'S'),
            Card('4', 'S'),
        ])
        self.assertGreater(higher_two_pair, lower_two_pair)

        lower_two_pair1 = Hand([
            Card('2', 'C'),
            Card('2', 'D'),
            Card('5', 'S'),
            Card('5', 'H'),
            Card('6', 'S'),
        ])

        higher_two_pair1 = Hand([
            Card('2', 'C'),
            Card('2', 'D'),
            Card('5', 'H'),
            Card('5', 'S'),
            Card('7', 'S'),
        ])
        self.assertGreater(higher_two_pair1, lower_two_pair1)

        lower_two_pair1 = Hand([
            Card('2', 'C'),
            Card('2', 'D'),
            Card('6', 'S'),
            Card('6', 'H'),
            Card('9', 'S'),
        ])

        higher_two_pair1 = Hand([
            Card('3', 'C'),
            Card('3', 'D'),
            Card('6', 'H'),
            Card('6', 'S'),
            Card('7', 'S'),
        ])
        self.assertGreater(higher_two_pair1, lower_two_pair1)

    def test_untie_one_pair(self):
        one_pair1 = Hand([
            Card('2', 'C'),
            Card('2', 'D'),
            Card('7', 'H'),
            Card('5', 'S'),
            Card('6', 'S'),
        ])

        one_pair2 = Hand([
            Card('2', 'C'),
            Card('2', 'D'),
            Card('7', 'H'),
            Card('5', 'S'),
            Card('6', 'S'),
        ])
        self.assertEquals(one_pair1, one_pair2)

        lower_one_pair = Hand([
            Card('2', 'C'),
            Card('2', 'D'),
            Card('7', 'H'),
            Card('5', 'S'),
            Card('6', 'S'),
        ])

        higher_one_pair = Hand([
            Card('3', 'C'),
            Card('3', 'D'),
            Card('7', 'H'),
            Card('5', 'S'),
            Card('8', 'S'),
        ])
        self.assertGreater(higher_one_pair, lower_one_pair)

        lower_one_pair1 = Hand([
            Card('2', 'C'),
            Card('2', 'D'),
            Card('7', 'H'),
            Card('5', 'S'),
            Card('6', 'S'),
        ])

        higher_one_pair1 = Hand([
            Card('2', 'C'),
            Card('2', 'D'),
            Card('7', 'H'),
            Card('5', 'S'),
            Card('8', 'S'),
        ])
        self.assertGreater(higher_one_pair1, lower_one_pair1)

    def test_untie_high_card(self):
        high_card1 = Hand([
            Card('A', 'C'),
            Card('2', 'D'),
            Card('7', 'H'),
            Card('5', 'S'),
            Card('6', 'S'),
        ])

        high_card2 = Hand([
            Card('A', 'C'),
            Card('2', 'D'),
            Card('7', 'H'),
            Card('5', 'S'),
            Card('6', 'S'),
        ])
        self.assertEquals(high_card1, high_card2)

        lower_high_card = Hand([
            Card('2', 'D'),
            Card('7', 'H'),
            Card('5', 'S'),
            Card('6', 'S'),
            Card('9', 'C'),
        ])

        higher_high_card = Hand([
            Card('7', 'H'),
            Card('5', 'S'),
            Card('A', 'D'),
            Card('6', 'S'),
            Card('9', 'C'),
        ])
        self.assertGreater(higher_high_card, lower_high_card)

if __name__ == '__main__':
    unittest.main()
