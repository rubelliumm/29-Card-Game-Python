from typing import List
from game.player import Player


class Bidding:
    bidding_starts = 17
    bidding_stops = 29
    players = []
    players_bid_vals = {}
    current_bidder = None
    previous_bidder = None
    current_bid = bidding_starts  # will change...

    def __init__(self, players: List[Player], bid_starter: Player) -> None:
        self.players = players
        self.current_bidder = bid_starter

        for x in players:
            self.players_bid_vals[x] = None

    @property
    def isAllPlayerDoneBidding(self) -> bool:
        # everyone passed.
        if all(x == "pass" for x in list(self.players_bid_vals.values())):
            return True
        # if 1 item has bid and 3 item has pass.
        if (
            len(
                list(
                    filter(
                        lambda x: isinstance(x, int),
                        list(self.players_bid_vals.values()),
                    )
                )
            )
            == 1
        ) and len(
            list(filter(lambda x: x == "pass", list(self.players_bid_vals.values())))
        ) == 3:
            return True
        else:
            return False

    def getNextBidder(self):
        data = self.players_bid_vals
        current_elem = self.current_bidder
        keys = list(data.keys())
        current_index = keys.index(current_elem)

        # Check subsequent elements
        for i in range(current_index + 1, len(keys)):
            next_key = keys[i]
            if data[next_key] is None:
                return next_key

        # If no suitable element is found, check from the beginning
        for i in range(0, current_index):
            if data[keys[i]] is None:
                return keys[i]
        return None  # Return None if no suitable element is found at all

    @staticmethod
    def ask(player, forValue):
        print(
            f"[{player}]: current bid is {forValue}. type 'b' for bid and 'p' for pass."
        )
        res = input(">>")
        if res.lower() == "b":
            return True
        else:
            return False

    def start(self):
        while not self.isAllPlayerDoneBidding:
            print(f"{self.current_bidder}: your card is ", self.current_bidder.cards)  # type: ignore
            is_bidding = self.ask(self.current_bidder, self.current_bid)
            if not is_bidding:
                self.players_bid_vals[self.current_bidder] = "pass"
                self.current_bidder = self.getNextBidder()
                continue
            else:
                self.players_bid_vals[self.current_bidder] = self.current_bid
                if self.previous_bidder is not None:
                    self.current_bidder, self.previous_bidder = (
                        self.previous_bidder,
                        self.current_bidder,
                    )
                    self.current_bid += 1
                else:
                    self.previous_bidder = self.current_bidder
                    self.current_bidder = self.getNextBidder()
                    self.current_bid += 1
        try:
            return [
                [key, value]
                for key, value in self.players_bid_vals.items()
                if isinstance(value, int)
            ][0]
        except IndexError:
            return None
