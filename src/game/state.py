from typing import Dict, List, Union
from game.player import Player
from game.constants import GAME_POINTS


class State:
    _playing_as: Player
    highest_bid: int
    highest_bidder: Player

    GAME_STATE = {}
    GAME_POINTS = {
        "team1_3": 0,
        "team2_4": 0,
    }

    def __init__(self, players: List[Player]) -> None:
        self.players: List[Player] = players
        self._single_round_info: Dict[Player, int] = {
            player: 0 for player in self.players
        }

    def update_round_info(self, round, winner: Player, round_points: int = 1):
        round_info = {"winner": winner}
        if (winner.name == "player1" or winner.name == "player3") and (
            self.highest_bidder.name == "player1"
            or self.highest_bidder.name == "player3"
        ):
            self.GAME_POINTS["team1_3"] += round_points
        elif (winner.name == "player2" or winner.name == "player4") and (
            self.highest_bidder.name == "player2"
            or self.highest_bidder.name == "player4"
        ):
            self.GAME_POINTS["team2_4"] += round_points
        elif (winner.name == "player2" or winner.name == "player4") and (
            self.highest_bidder.name == "player1"
            or self.highest_bidder.name == "player3"
        ):
            self.GAME_POINTS["team1_3"] -= round_points
        elif (winner.name == "player1" or winner.name == "player3") and (
            self.highest_bidder.name == "player2"
            or self.highest_bidder.name == "player4"
        ):
            self.GAME_POINTS["team2_4"] -= round_points
        else:
            print("passing....state.py")
        self.GAME_STATE[round] = round_info

    def is_game_over(self) -> bool:
        return (
            self.GAME_POINTS["team1_3"] >= GAME_POINTS
            or self.GAME_POINTS["team2_4"] <= -GAME_POINTS
        ) or (
            self.GAME_POINTS["team2_4"] >= GAME_POINTS
            or self.GAME_POINTS["team1_3"] <= -GAME_POINTS
        )

    def set_highest_bid(self, bid: int):
        self.highest_bid = bid

    def get_higest_bid(self):
        return self.highest_bid

    def set_playing_as(self, player: Player):
        self._playing_as = player

    def get_playing_as(self):
        return self._playing_as

    @property
    def single_round_info(self):
        player1_3 = self.players[0].points + self.players[2].points
        player2_4 = self.players[1].points + self.players[3].points
        return f"Player1_3({player1_3}) && Player2_4({player2_4}) \n highest_bid ({self.highest_bid}) || highest_bidder({self.highest_bidder})"

    def update_state_game_over(self):
        print("Game Over!!!")
        if self.GAME_POINTS["team1_3"] > self.GAME_POINTS["team2_4"]:
            print("team1_3 Won!!!")
        elif self.GAME_POINTS["team2_4"] > self.GAME_POINTS["team1_3"]:
            print("team2_4 Won!!!")
        else:
            print("Draw!!!")

    def is_single_round_closed(self):
        player1_3 = self.players[0].points + self.players[2].points
        player2_4 = self.players[1].points + self.players[3].points
        if (
            self.get_playing_as().name == "player1"
            or self.get_playing_as().name == "player3"
        ):
            return (
                player1_3 >= self.get_higest_bid()
                or player2_4 > 28 - self.get_higest_bid()
            )
        elif (
            self.get_playing_as().name == "player2"
            or self.get_playing_as().name == "player4"
        ):
            return (
                player2_4 >= self.get_higest_bid()
                or player1_3 > 28 - self.get_higest_bid()
            )
        else:
            raise ValueError("Invalid player")

    def __repr__(self) -> str:
        return f"Game Points({self.GAME_POINTS}) \n Game State({self.GAME_STATE})"
