# PyPoker #

#### Implements 3 basic classes for poker.

##### Card Represents a card #####
###### Usage ######
	from pypoker import Card
	ACCEPTABLE_SUITS = ['C', 'D', 'H', 'S']
	ACCEPTABLE_VALUES = ['2','3','4','5','6','7','8','9','T', 'J', 'Q', 'K', 'A']
	suit = 'C'
	value = 'T'
	card = Card(value, suit)
	card.numeric_value # For T returns the integer 10
	
###### Parsing card from string ######
	from pypoker import Card

	card = Card.parse_from_string('JS')
	card.suit # It returns J
	card.numeric_value # For J returns the integer 11
	
###### Comparing cards ######
The Card class implements the **\__cmp__** method so cards can be campared using the operands (**==**, **>=**, **<=**, **<**, **>**) as in the following code example:

	from pypoker import Card

	higher_card = Card.parse_from_string('JS')
	lower_card = Card.parse_from_string('TS')
	print higher_card > lower_card # It prints True	
	
##### Hand Represents a hand of cards #####
###### Usage ######
	from pypoker import Hand
	
    royal_flush = Hand([
        Card('T', 'C'),
        Card('J', 'C'),
        Card('Q', 'C'),
        Card('K', 'C'),
        Card('A', 'C'),
    ])
    
    straight_flush = Hand([
        Card('9', 'C'),
        Card('T', 'C'),
        Card('J', 'C'),
        Card('Q', 'C'),
        Card('K', 'C'),
    ])
    
    print straight_flush.hand_value # It prints Straight Flush
	
###### Parsing hand from string ######

	from pypoker import Hand

	three_of_a_kind = Hand.from_string('4D 4D 4D 7H 8D')
	print three_of_a_kind # It prints <hand [4D, 4D, 4D, 7H, 8D], 'Tree of a Kind'>
	
###### Comparing hands ######
The Hand class implements the **\__cmp__** method so hands can be campared using the operands (**==**, **>=**, **<=**, **<**, **>**) as in the following code example:

	from pypoker import Hand

	three_of_a_kind = Hand.from_string('4D 4D 4D 7H 8D')
	one_pair = Hand.from_string('4D 3D 3D 7H AD')

	print three_of_a_kind > one_pair # It prints True


###### The Tie Breaker ######
The Tie Breaker rules have been taken from the following [site.](https://www.adda52.com/poker/poker-rules/cash-game-rules/tie-breaker-rules)
