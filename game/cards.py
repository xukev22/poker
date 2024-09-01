from enum import Enum, auto
import random

# Define the Suit enum
class Suit(Enum):
    HEARTS = 'HEARTS'
    DIAMONDS = 'DIAMONDS'
    CLUBS = 'CLUBS'
    SPADES = 'SPADES'

# Define the Rank enum
class Rank(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

# Define the Card class
class Card:
    def __init__(self, rank: Rank, suit: Suit):
        if not isinstance(rank, Rank):
            raise TypeError(f"Expected rank to be of type Rank, got {type(rank).__name__} instead.")
        if not isinstance(suit, Suit):
            raise TypeError(f"Expected suit to be of type Suit, got {type(suit).__name__} instead.")
        
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f'{self.rank} of {self.suit}'

    def __repr__(self):
        return self.__str__()


# Define the Deck class
class Deck:
    def __init__(self, predefined_cards=None):
        if predefined_cards is not None:
            # Use the predefined list of cards
            self.cards = predefined_cards
        else:
            # Default to a standard deck if no predefined order is provided
            self.cards = [Card(rank, suit) for suit in Suit for rank in Rank]

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        cards_str = '\n'.join(str(card) for card in self.cards)
        return f'Deck of {len(self)} cards:\n{cards_str}'

    def __repr__(self):
        return self.__str__()
    
    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, amount: int):
        # Check if there are enough cards to deal
        if amount <= 0 or amount > len(self.cards):
            raise ValueError("Not enough cards in the deck to deal, or passed value < 0")
        # Remove the first n cards from the deck
        dealt_cards = self.cards[:amount]
        self.cards = self.cards[amount:]
        return dealt_cards

Rank(2)
card = Card(Rank(2), Suit('CLUBS'))
print(card)
deck = Deck()
print(deck)
deck.shuffle()
print(deck)
# deck.deal(55)
# deck.deal(0)
print(deck.deal(3))
print(deck)