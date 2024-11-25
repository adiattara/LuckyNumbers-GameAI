from PIL.ImagePalette import random

from model.HumanPlayer import HumanPlayer
from model.RandomPlayer import RandomPlayer
from Game import Game
from GameGUI import GameGUI
import numpy as np
import time


def main():
    # Initialiser les joueurs
    player1 = RandomPlayer("Joueur 1" )
    player2 = RandomPlayer("Joueur 2")
    players = [player1, player2]

    # Initialiser le jeu
    game = Game(players)

    # Variables de suivi
    turn = 0

    # Boucle de jeu
    while not game.game_over:  # Limite le nombre de tours pour éviter les boucles infinies
        current_player = game.players[game.current_player_index]

        # print(f"\nTour {turn + 1} - {current_player.name}'s turn:")

        # **Phase 1 : Piocher**
        if game.current_tile == 0:
            available_draw_actions = game.get_valid_actions()
#             print(available_draw_actions)
            available_draw_ids = [i for i, val in enumerate(available_draw_actions) if val != 0]
#             print(available_draw_ids)
            action = np.random.choice(available_draw_ids)

            # Exécuter l'action de piocher
            state, reward, done = game.step_action(action)
#             print(current_player.board.get_valid_vide_positions_bis(game.current_tile))
#             current_player.board.display_board()

            if done:
               game.determine_winner()

        # **Phase 2 : Placer ou Défausser**
        if game.current_tile != 0:
            available_action_ids = game.get_valid_actions()
#             print(current_player.board.get_valid_vide_positions_bis(game.current_tile))
            available_actions = [i for i, val in enumerate(available_action_ids) if val != 0]
#             print(available_actions)

            action_place_or_discard = np.random.choice(available_actions)


            # Exécuter l'action de placer ou défausser
            state, reward, done = game.step_action(action_place_or_discard)

            if done:
                game.determine_winner()

        # Passer au joueur suivant
        game.current_player_index = (game.current_player_index + 1) % len(game.players)
        turn += 1

    # Résultat final
    if game.game_over:
        winner = game.players[(game.current_player_index - 1) % len(game.players)]
#         print(f"\nLe gagnant est {winner.name} !")
    else:
#         print("\nLa partie a été arrêtée après 100 tours sans gagnant.")
        pass


if __name__ == "__main__":

    start = time.time()
    for i in range(50):
       main()
    end = time.time()
    time = end - start
    print(50/time)
