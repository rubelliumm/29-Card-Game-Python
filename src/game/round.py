import random
from typing import Dict, List, Union

from data_structure.card_list import CardList
from game import utils
from game import player
from game.bidding import Bidding
from game.board import Board
from game.card import Card, Pack
from game.player import Player
from game.state import State


class RoundResult:
    _current_distributor: Player
    next_distributor: Player
    _round_winner: Player
    highest_bidder: Player
    highest_bid: int
    is_game_over: bool
    round_points: int

    def __str__(self) -> str:
        return f"RoundResult(current dist: {self.next_distributor})"

    def set_round_winner(self, players: Player):
        self._round_winner = players


class Round:
    _trumpCard: Union[Card, None]
    highest_bidder: Player
    highest_bid: int
    _is_trump_reaveled: bool = False
    round_points: int
    # this var will be set after distributing card.

    def __init__(
        self, name: str, players: List[Player], distributor: Player, game_state: State
    ):
        self.name = name
        self.board = Board()
        self.game_state = game_state
        self._players = players
        self._current_distributor = distributor
        self.distribute_card_and_start_bidding(distributor=self._current_distributor)

    def distribute_card_and_start_bidding(self, distributor: Player):
        print(f"distributing card..distributor is {distributor}\n")
        pack = Pack()
        random.shuffle(pack.cards)

        for player in self._players:
            player.cards.flush()
            # randomly distribute 4 cards among 4 players.
            random_items = random.sample(pack.cards, 4)
            player.cards.add_to_cardlist(random_items)
            for x in random_items:
                pack.cards.remove(x)

        bidding = Bidding(players=self._players, bid_starter=self._current_distributor)
        b = bidding.start()
        if b is None:  # all players passed.
            print("\n[+]All player passed, bidding again.\n")
            # reset bidding state everytime when new bidding starts.
            self.resetBiddingState(bidding)
            # current_dist = self.get_current_distributor()
            next_dist = self.get_next_distributor()
            self._current_distributor = next_dist
            self.distribute_card_and_start_bidding(distributor=next_dist)

        else:
            self.highest_bidder, self.highest_bid = b
            trump = self.highest_bidder._chooseTrump()
            self._trump_card = trump
            # asking double and redoubling...
            if self.ask_opponent_for_playing_double():
                redoubled = self.ask_bidder_for_playing_redouble()
                if redoubled:
                    self.round_points = 4
                else:
                    self.round_points = 2
                    # pass this in round result to update in state..
            else:
                self.round_points = 1
            for player in self._players:
                # randomly distribute 4 cards among 4 players.
                random_items = random.sample(pack.cards, 4)
                player.cards.add_to_cardlist(random_items)
                pack.cards = [item for item in pack.cards if item not in random_items]
            return

    def ask_opponent_for_playing_double(self) -> bool:
        _playing_double_lst: List = []
        for player in self.get_opponent_list():
            _playing_double_lst.append(
                player.ask(f"do you wanna play double?? {player.cards} 'y' for Yes>>\t")
            )
        return any(item == "y" for item in _playing_double_lst)

    def ask_bidder_for_playing_redouble(self) -> bool:
        print("Do you wanna play redouble bidder???")
        _response = []
        if (
            self.highest_bidder.name == "player1"
            or self.highest_bidder.name == "player3"
        ):
            _player_list = [self._players[0], self._players[2]]
        else:
            _player_list = [self._players[1], self._players[3]]
        for player in _player_list:
            _response.append(
                player.ask(f"Do you wanna redouble it?? {player.cards} 'y' for Yes>>\t")
            )
        return any(str(x).lower() == "y" for x in _response)

    def get_opponent_list(self) -> List[Player]:
        if (
            self.highest_bidder.name == "player1"
            or self.highest_bidder.name == "player3"
        ):
            return [self._players[1], self._players[3]]
        else:
            return [self._players[0], self._players[2]]

    @staticmethod
    def resetBiddingState(bidding: Bidding):
        print("clearing bidding state...")
        for player in bidding.players:
            bidding.players_bid_vals[player] = None
        bidding.current_bid = bidding.bidding_starts
        bidding.previous_bidder = None

    def get_current_distributor(self):
        return self._current_distributor

    def get_next_distributor(self) -> Player:
        current_dist = self.get_current_distributor()
        index = self._players.index(current_dist)
        try:
            return self._players[index + 1]
        except IndexError:
            return self._players[0]

    def get_next_player(self, player: Player) -> Player:
        index = self._players.index(player)
        try:
            return self._players[index + 1]
        except IndexError:
            return self._players[0]

    def get_trump(self):
        return self._trump_card

    def set_highest_bidder(self, highest_bidder: Player):
        self.highest_bidder = highest_bidder

    def set_highest_bid(self, highest_bid: int):
        self.highest_bid = highest_bid

    def reset_players_points(self):
        for player in self._players:
            player.points = 0

    def start(self) -> RoundResult:
        if self.get_trump() and self.highest_bid and self.highest_bidder:
            self.game_state.set_playing_as(self.highest_bidder)
            # self.game_state.set_highest_bid(self.highest_bid)
            self.game_state.highest_bid = self.highest_bid
            self.game_state.highest_bidder = self.highest_bidder
            while not self.game_state.is_single_round_closed():
                single_round = SingleCirculation(
                    round_obj=self, starter=self.highest_bidder
                )
                single_round.start()
                winner_and_points = single_round.get_single_round_winner()
                winner = list(winner_and_points.keys())[0]
                winner_points = winner_and_points.get(winner)
                print(
                    f"\n\033[42m!!!!! {winner} is winner ...taking all the card...\033[0m\n"
                )
                if isinstance(winner_points, int):
                    winner.points += winner_points
                else:
                    raise ValueError("winner points must be int.")
                self.highest_bidder = winner
                print(
                    "\n\033[35m===============================================================================\033[0m"
                )
                print(self.game_state.single_round_info)
                print(
                    "\033[35m===============================================================================\033[0m\n"
                )

            result = RoundResult()
            result.set_round_winner(winner)
            result.round_points = self.round_points
            result.highest_bidder = self.highest_bidder
            result.highest_bid = self.highest_bid
            result.is_game_over = self.game_state.is_game_over()
            result.next_distributor = self.get_next_distributor()
            return result
        else:
            raise ValueError("error  at round.py")


class SingleCirculation:
    # _is_trump_revealed: bool = False
    _valid_card_for_this_single_round: Card
    current_player: Player

    def __init__(self, round_obj: Round, starter: Player):
        self.__trump = round_obj.get_trump()
        self.board = round_obj.board
        self.round_obj = round_obj
        starter_card = self.ask_to_serve(starter, None)
        self._valid_card_for_this_single_round = starter_card
        served_card = starter.cards.serveCard(starter_card)
        self.board.add_to_board(starter, served_card)
        self.current_player = self.round_obj.get_next_player(starter)

    def start(self):
        for _ in range(3):
            player_res = self.ask_to_serve(
                self.current_player, self._valid_card_for_this_single_round
            )
            if isinstance(player_res, Card):
                self.current_player.cards.serveCard(player_res)
                board_res = self.board.add_to_board(self.current_player, player_res)
                if isinstance(board_res, Player):
                    self.current_player = board_res
                else:
                    self.current_player = self.round_obj.get_next_player(
                        self.current_player
                    )
            else:
                raise ValueError(
                    f"invalid type of player res:: {player_res} with type {type(player_res)}"
                )

    def ask_to_serve(
        self, player: Player, type_of_valid_card: Union[Card, None]
    ) -> Card:
        __type_of_card = type_of_valid_card
        __player = player
        available_cards = player.cards.get_similar_typeCards(__type_of_card)
        if not available_cards:  # no cards
            print(
                f"\033[31m!!!{self.current_player} has no card of type {__type_of_card}\033[0m"
            )
            if not self.round_obj._is_trump_reaveled:
                see_trump_card = input(
                    f"\033[1;32m[{player}]: Do you wanna see Trump Card?? type 'y' to reveal.\033[0m\t"
                )
                if see_trump_card.lower() == "y":
                    self.round_obj._is_trump_reaveled = True
                    self.board._is_trump_revealed = True  # TODO
                    print(f"\033[1;32mTrump Card is {self.__trump}\033[0m")
                    available_cards = player.cards.get_similar_typeCards(self.__trump)
                    if not available_cards:
                        # trump o nai... serve any card now..
                        print(
                            f"\033[43m[{player}]: You dont have any trump card,trump card is {self.__trump}. serve any card.\033[0m"
                        )
                        available_cards = player.cards.get_currentCard()
                else:
                    print(
                        f"[{player}]: not interested? You can serve any card of you. Trump is still hidden."
                    )
                    # player is not interested to reveal trump
                    available_cards = player.cards.get_currentCard()
            else:
                # trump is already revealed, can serve any card.
                print(
                    f"\033[46m[{player}]: Trump is already revealed.. Trump: {self.__trump}..you can choose any of your card.\033[0m"
                )
                available_cards = player.cards.get_currentCard()
        print(f"[{player}]: serve any of your cards from bellow: type number for:")
        for i, card in enumerate(available_cards):
            print(f"{i+1}: {card}")
        try:
            card_number = int(
                input(f"[{player}]: Enter the number of the card you want to serve:")
            )
        except:
            try:
                card_number = int(
                    input(
                        f"[{player}]: Enter the number of the card you want to serve:"
                    )
                )
            except:
                print("aborting for 2 failed attempt")
                raise ValueError("invalid input detected.")
            # return self.ask_to_serve(player=__player, type_of_valid_card=__type_of_card)
        if card_number > len(available_cards):
            print("Invalid card number")
            return self.ask_to_serve(player=__player, type_of_valid_card=__type_of_card)
        return available_cards[card_number - 1]

    def get_single_round_winner(self) -> Dict[Player, int]:
        opening_card = self._valid_card_for_this_single_round
        trump = self.__trump
        is_trump_revealed = self.round_obj._is_trump_reaveled
        board_cards = self.board.get_all_cards_on_board()
        board_points = self.board.get_total_points_on_board()
        self.board.flush()
        cards = list(board_cards.values())
        if is_trump_revealed and not self.__trump.__class__.__name__ == "Jokar":
            trump_cards_on_board = utils.get_similar_card_from_list(cards, trump)
            if not trump_cards_on_board:
                # trump revealed and board has no trump card.
                # proceed as usual...
                top_valid_card_served = utils.get_similar_card_from_list(
                    cards, opening_card
                )
                top_card = min(top_valid_card_served, key=lambda x: x.rank)
                winner = list(filter(lambda x: x[1] == top_card, board_cards.items()))[
                    0
                ][0]
                return {winner: board_points}
            top_card = min(trump_cards_on_board, key=lambda x: x.rank)
            winner = list(filter(lambda x: x[1] == top_card, board_cards.items()))[0][0]
            return {winner: board_points}
        else:
            top_valid_card_served = utils.get_similar_card_from_list(
                cards, opening_card
            )
            top_card = min(top_valid_card_served, key=lambda x: x.rank)
            winner = list(filter(lambda x: x[1] == top_card, board_cards.items()))[0][0]
            return {winner: board_points}
