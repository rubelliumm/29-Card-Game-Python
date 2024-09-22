import os, sys
sys.path.append(os.path.join(os.getcwd(), 'src'))

from game.twentynine import Game
g = Game()
g.run()
