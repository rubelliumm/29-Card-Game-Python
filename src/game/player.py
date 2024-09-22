from data_structure.card_list import CardList
from game.card import Card, Club, Diamond, Heart, Jokar, Spade


class Player:
    def __init__(self, name):
        self.name = name
        self.cards = CardList([])
        self.bid = 0
        self.points = 0
        self.is_distributor = False

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def ask(self, what_to_ask: str = "") -> str:
        return input(f"[{self}]: {what_to_ask}")

    def _chooseTrump(self) -> Card:
        trump = None
        print(f"{self}: please chose Trump card. Your cards are: {self.cards}\n")
        res = input(
            "[+] 1: Heart\n[+] 2: Spade\n[+] 3: Diamond\n[+] 4: Club\n[+] 5: No Trump(Jokar)\n"
        )
        if res.lower() == "1":
            trump = Heart("heart", 0)
        elif res.lower() == "2":
            trump = Spade("spade", 0)
        elif res.lower() == "3":
            trump = Diamond("diamond", 0)
        elif res.lower() == "4":
            trump = Club("club", 0)
        elif res.lower() == "5":
            trump = Jokar("Jokar", 0)
        else:
            return self._chooseTrump()
        return trump
