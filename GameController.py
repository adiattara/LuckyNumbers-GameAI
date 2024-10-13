# controller.py

from model.RandomPlayer import RandomPlayer
import numpy as np

class GameController:
    def __init__(self, game, view):
        self.game = game  # Le modèle
        self.view = view  # La vue
        self.current_tile = None
        self.state = "waiting_for_draw"  # État initial

    def handle_draw_tile(self, from_discard=False, tile=None):
        """
        Piocher une tuile depuis la pioche ou la défausse.
        :param from_discard:
        :param tile:
        :return:
        """

        if self.state != "waiting_for_draw":
            self.view.display_message("Vous ne pouvez pas piocher maintenant.")
            return

        if tile is not None:
            # Piocher une tuile spécifique depuis la défausse
            if tile in self.game.tile_bag.discard_pile:
                self.game.tile_bag.discard_pile.remove(tile)
                self.current_tile = tile
                self.state = "waiting_for_move"
                self.view.update_current_tile(tile)
            else:
                self.view.display_message("La tuile sélectionnée n'est pas dans la défausse.")
        else:
            # Piocher depuis la pioche ou la défausse
            pile = 'd' if from_discard else 'p'
            tile = self.game.tile_bag.piocher(pile)
            if tile == -1:
                message = "La défausse est vide." if from_discard else "La pioche est vide."
                self.view.display_message(message)
                # Vérifier si la pioche est vide pour déterminer la fin de la partie
                if pile == 'p':
                    self.determine_game_over()
                return
            self.current_tile = tile
            self.state = "waiting_for_move"
            self.view.update_current_tile(tile)

    def handle_place_tile(self, row, col):
        if self.state != "waiting_for_move" or self.current_tile is None:
            self.view.display_message("Vous devez piocher une tuile.")
            return

        board = self.game.players[0].board
        tile = self.current_tile
        old_tile = board.get_tile(row, col)

        # Vérifier si le placement est valide
        if board.is_valid_move(row, col, tile):
            # défausser l'ancienne tuile
            if old_tile is not None and old_tile > 0:
                self.game.tile_bag.discard_tile(old_tile)
                board.place_tile(row, col, tile)
                self.current_tile = None
                self.state = "waiting_for_draw"
                self.view.update_board()
                self.view.clear_current_tile()
                #print("joueur courant", self.game.players[self.game.current_player_index].name)
                self.next_turn()
                return
            board.place_tile(row, col, tile)
            self.current_tile = None
            self.state = "waiting_for_draw"
            self.view.update_board()
            self.view.clear_current_tile()
            self.next_turn()

        else:
            self.view.display_message("Position invalide pour cette tuile.")

    def handle_discard_tile(self):
        """
        Défausser la tuile courante.
        :return:
        """
        if self.current_tile is not None:
            self.game.tile_bag.discard_tile(self.current_tile)
            self.current_tile = None
            self.state = "waiting_for_draw"
            self.view.clear_current_tile()

            self.next_turn()
        else:
            self.view.display_message("Aucune tuile à défausser.")

    def next_turn(self):
        # Passer au joueur suivant
        self.game.next_player()
        current_player = self.game.get_current_player()
        print(self.game.current_player_index)
        if isinstance(current_player, RandomPlayer):
            # # Laisser l'IA jouer son tour
            # move_success = current_player.take_turn(self.game.tile_bag)
            # self.next_turn()
            # self.view.update_board()
            # # Vérifier si l'IA a gagné
            # if current_player.board.is_complete():
            #     self.view.display_message("L'IA a complété sa grille ! Vous avez perdu.")
            #     self.state = "game_over"
            # # Vérifier si le joueur a gagné
            # elif self.game.players[0].board.is_complete():
            #     self.view.display_message("Vous avez complété votre grille ! Vous avez gagné !")
            #     self.state = "game_over"
            # elif move_success:
            #     # Continue game
            #     self.state = "waiting_for_draw"
            # else:
            #     # Si l'IA ne peut plus jouer et la pioche est vide
            #     self.determine_game_over()

            if current_player.board.is_complete():
                self.view.display_message("L'IA a complété sa grille ! Vous avez perdu.")
                self.state = "game_over"
                return

            if self.game.players[0].board.is_complete():
                self.view.display_message("Vous avez complété votre grille ! Vous avez gagné !")
                self.state = "game_over"
                return

            if self.game.current_tile == 0:

                print("ordianteur n'a pas de tuile et veut piocher")

                available_draw_actions = self.game.get_valid_actions()

                print("les action disponibles pour piocher",available_draw_actions)

                available_draw_ids = [i for i, val in enumerate(available_draw_actions) if val != 0]

                action = np.random.choice(available_draw_ids)

                if action == 37 :
                    print("ordinateur a piocher dans le bag", action)

                else:
                    print("il a piocher dans la défause",action)

                # Exécuter l'action de piocher
                state, reward, done = self.game.step_action(action)

                print(current_player.board.get_valid_vide_positions_bis(self.game.current_tile))

                if done:
                    self.determine_game_over()
                else:
                    self.state = "waiting_for_draw"

            if self.game.current_tile != 0:
                    tile = self.game.current_tile
                    print("ordinateur a piocher ",self.game.current_tile)

                    print("il doit décider s'il doit le placer ou pas ")

                    print("choix des actions disponibles")


                    available_action_ids = self.game.get_valid_actions()
                    print(current_player.board.get_valid_vide_positions_bis(self.game.current_tile))
                    available_actions = [i for i, val in enumerate(available_action_ids) if val != 0]

                    print("voici les actions disponibles ",available_actions)


                    action_place_or_discard = np.random.choice(available_actions)

                    print("action_choisit",action_place_or_discard)

                    if action_place_or_discard == 16:
                        print("ordinateur a défaussé la tuile: ", tile)
                    # Exécuter l'action de placer ou défausser
                    state, reward, done = self.game.step_action(action_place_or_discard)
                    print("ordinateur a placer",tile)

                    if done:
                        self.determine_game_over()
                    else:
                        self.state = "waiting_for_draw"





            self.next_turn()
            self.view.update_board()
            current_player.board.display_board()


    def determine_game_over(self):
        message = self.game.determine_winner()
        self.view.display_message(message)
        self.state = "game_over"

    def is_game_over(self):
        return self.state == "game_over"



