class Pack:
    cards = []
    cards_identity = {"J": 3, "9": 2, "A": 1, "10": 1, "K": 0, "Q": 0, "8": 0, "7": 0}

    def __init__(self):
        self.cards = []
        for sym, val in self.cards_identity.items():
            self.cards.extend(
                [Heart(sym, val), Spade(sym, val), Club(sym, val), Diamond(sym, val)]
            )

    def __repr__(self) -> str:
        return f"{self.cards}"

    def __iter__(self):
        return iter(self.cards)

    @staticmethod
    def sorted_cards(cards: list):
        sorted_card = []
        cards_name = ["Heart", "Spade", "Diamond", "Club"]
        for card in cards_name:
            sorted_card.append(
                list(filter(lambda x: x.__class__.__name__ == card, cards))
            )
        return sorted_card

    def __str__(self) -> str:
        return f"{self.sorted_cards(self.cards)}"


class Card:

    def __init__(self, sym, value):
        self.value = value
        self.sym = sym

    @property
    def rank(self):
        __CARDS_RANKING = ["J", "9", "A", "10", "K", "Q", "8", "7"]
        return __CARDS_RANKING.index(self.sym) + 1

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __eq__(self, other):
        return (
            isinstance(other, Card)
            and self.sym == other.sym
            and self.__class__.__name__ == other.__class__.__name__
        )

    def _isHomogenous(self):
        return self.sym == self.sym

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"{self.sym}"


class Heart(Card):
    def __str__(self):
        return f"♥  {self.sym}"


class Spade(Card):
    def __str__(self):
        return f"♠  {self.sym}"


class Club(Card):
    def __str__(self):
        return f"♣  {self.sym}"


class Diamond(Card):
    def __str__(self):
        return f"♦  {self.sym}"


class Jokar(Card):
    def __str__(self):
        return f"Jokar"
