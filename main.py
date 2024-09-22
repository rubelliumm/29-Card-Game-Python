import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.game.twentynine import Game

if __name__ == "__main__":
    game = Game()
    game.run()
