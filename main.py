# from HumanPlayer import HumanPlayer
# from RandomPlayer import RandomPlayer
# from Game import Game
# if __name__ == "__main__":
#     player1 = HumanPlayer("Joueur 1")
#     player2 = RandomPlayer("Ordinateur")
#
#     game = Game([player1, player2])
#     game.play()

# main.py

from model.HumanPlayer import HumanPlayer
from model.RandomPlayer import RandomPlayer
from Game import Game
from GameGUI import GameGUI

if __name__ == "__main__":
    player1 = HumanPlayer("Humain")
    player2 = RandomPlayer("Ordinateur")

    game = Game([player1, player2])
    game_gui = GameGUI(game)
    game_gui.run()
