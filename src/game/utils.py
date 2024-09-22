from typing import List

from game.card import Card, Heart, Pack


def get_similar_card_from_list(list_of_cards: List[Card], card: Card):
    return list(
        filter(
            lambda x: x.__class__.__name__ == card.__class__.__name__,
            list_of_cards,
        )
    )
