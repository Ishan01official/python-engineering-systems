"""
The famous FrenchDeck example from Fluent Python Ch. 1.

Implements just __len__ and __getitem__. Gets indexing, slicing,
iteration, `in`, `random.choice`, and `sorted` for FREE because
they all use the data-model protocols.

Run:
    python 19-fluent-deep-dives/examples/01_french_deck.py
"""
import random
from collections import namedtuple


Card = namedtuple("Card", ["rank", "suit"])


class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list("JQKA")
    suits = "spades diamonds clubs hearts".split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]


# A custom ordering for sortability
SUIT_VALUES = {"clubs": 0, "diamonds": 1, "hearts": 2, "spades": 3}


def card_rank(card: Card) -> int:
    rank_value = FrenchDeck.ranks.index(card.rank)
    return rank_value * 4 + SUIT_VALUES[card.suit]


if __name__ == "__main__":
    deck = FrenchDeck()

    print(f"len(deck):           {len(deck)}")
    print(f"deck[0]:             {deck[0]}")
    print(f"deck[-1]:            {deck[-1]}")
    print(f"deck[:3]:            {deck[:3]}")
    print(f"random.choice(deck): {random.choice(deck)}")
    print(f"Card('Q','hearts') in deck: {Card('Q', 'hearts') in deck}")

    print()
    print("first 5 of sorted deck (by rank, then suit):")
    for card in sorted(deck, key=card_rank)[:5]:
        print(f"  {card}")

    print()
    print("Notice: we only implemented __len__ and __getitem__.")
    print("Iteration, slicing, `in`, random.choice, and sorted ALL came for free.")
    print("That's the Python data model.")
