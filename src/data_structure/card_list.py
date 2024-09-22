from typing import List, Union

from game.card import Card


class CardList:
    _Cards: List[Card] = []

    def __init__(self, card_list: Union[List[Card], Card]):
        # self.cards: List[Card] = []
        if isinstance(card_list, list):
            self._Cards = card_list
        else:
            self._Cards.append(card_list)

    def add_to_cardlist(self, card: Union[Card, List[Card]]):
        """Add a card or a list of cards to the card list."""
        if isinstance(card, list):
            if len(self._Cards) + len(card) >= 9:
                raise OverflowError("Can't have more than 8 items in one CardList")
            if all(isinstance(x, Card) for x in card):
                new_items_only = list(filter(lambda x: x not in self._Cards, card))
                self._Cards.extend(new_items_only)
        elif isinstance(card, Card):
            if len(self._Cards) + 1 >= 9:
                raise OverflowError("Can't have more than 8 items in one CardList")
            if card not in self._Cards:
                self._Cards.append(card)
        else:
            pass

    # @staticmethod
    # def sort_key(card: Card):
    #     custom_order = {"J": 0, "9": 1, "A": 2, "10": 3, "K": 4, "Q": 5, "8": 6, "7": 7}
    #     return (card.__class__.__name__, custom_order[card.sym])

    def get_similar_typeCards(self, card_type: Union[Card, str, None]) -> List[Card]:
        """Return a list of cards with the same type as the given card."""
        if isinstance(card_type, str):
            if (
                card_type == "Heart"
                or card_type == "Spade"
                or card_type == "Diamond"
                or card_type == "Club"
            ):
                return list(
                    filter(lambda x: x.__class__.__name__ == card_type, self._Cards)
                )
            else:
                raise ValueError("Invalid string of card name provided.")
        elif isinstance(card_type, Card):
            return list(
                filter(
                    lambda x: x.__class__.__name__ == card_type.__class__.__name__,
                    self._Cards,
                )
            )
        else:
            return self.get_currentCard()

    def serveCard(self, card: Card):
        """Remove the specified card from the card list."""
        if card in self._Cards:
            self._Cards.remove(card)
            return card
        else:
            raise ValueError("Card not found in the card list")

    def get_currentCard(self) -> List[Card]:
        """Get the current card from the list (if there are any)."""
        if self._Cards:
            return self._Cards
        else:
            raise ValueError("No cards in the card list")

    def flush(self):
        """Remove the all card."""
        self._Cards.clear()

    def __repr__(self):

        sortedCards = sorted(self._Cards, key=lambda x: (x.__class__.__name__, x.rank))
        return f"CardList({sortedCards})"

    def __iter__(self):
        return iter(self._Cards)

    def __len__(self):
        return len(self._Cards)
