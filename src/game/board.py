from typing import Dict, Iterable

from game.card import Card
from game.player import Player


class Board:
    _trumpCard: Card
    _is_trump_revealed: bool

    def __init__(self):
        self._board_items: Dict[Player, Card] = {}

    def set_trumpCard_to_board(self, trumpCard: Card):
        self._trumpCard = trumpCard

    def add_to_board(self, player: Player, card: Card):
        self._board_items[player] = card
        print(
            "\n\033[33m+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\033[0m"
        )
        print(f"{self._board_items}")
        print(
            "\033[33m+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\033[0m\n"
        )

        return self._board_items

    def _get_top_player(self) -> Player:
        return min(self._board_items.items(), key=lambda item: item[1].rank)[0]

    def get_total_points_on_board(self) -> int:
        return sum(card.value for card in self._board_items.values())

    def get_all_cards_on_board(self) -> Dict[Player, Card]:
        return self._board_items

    def board_len(self) -> int:
        return len(self._board_items)

    def flush(self) -> None:
        self._board_items = {}

    def __repr__(self) -> str:
        return f"Board({self._board_items})"

    def __iter__(self) -> Iterable:
        return iter(self._board_items)
