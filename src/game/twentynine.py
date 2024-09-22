from random import choice, random
from game.constants import NUMBER_OF_ROUND
from game.player import Player
from game.round import Round
from game.state import State


class Game:
    current_distributor: Player

    def __init__(self):
        self.players = [Player(f"player{i}") for i in range(1, 5)]
        self.state = State(self.players)
        # initially choose a random distributor.
        random_distributor = choice(self.players)
        self.current_distributor = random_distributor
        # grouping teams:

    def run(self):
        number_of_round: int = NUMBER_OF_ROUND
        for x in range(1, number_of_round + 1):  # total of 8 round
            print(
                f"\n\033[32m++++++++++++++++++++++++++ Round{x} ++++++++++++++++++++++++++\033[0m"
            )
            round = Round(
                name=f"round{x}",
                players=self.players,
                distributor=self.current_distributor,
                game_state=self.state,
            )
            round_result = round.start()
            round.reset_players_points()
            if round_result.is_game_over:
                break
            self.current_distributor = round_result.next_distributor
            self.round_winner = round_result._round_winner
            print(
                "\n\033[31m-------------------------------------------------------------------------------------------\033[0m"
            )
            self.state.update_round_info(
                round.name, round_result._round_winner, round_result.round_points
            )
            print(
                "\n========================================================================="
            )
            print(f"Number of round: {number_of_round}")
            print(f"round: {round.name}")
            print(self.state)  # print game state. repr fun
            print(
                "=========================================================================\n"
            )
        self.state.update_state_game_over()

    def __str__(self) -> str:
        return f"TwentyNine Game {self.players}"

    def __repr__(self) -> str:
        return self.__str__()
