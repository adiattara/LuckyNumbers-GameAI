# controller.py

from model.RandomPlayer import RandomPlayer

class GameController:
    def __init__(self, game, view):
        self.game = game  # Le modèle
        self.view = view  # La vue
        self.current_tile = None
        self.state = "waiting_for_draw"  # État initial

    def handle_draw_tile(self, from_discard=False, tile=None):
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

        # Vérifier si le placement est valide
        if board.is_valid_move(row, col, tile):
            board.place_tile(row, col, tile)
            self.current_tile = None
            self.state = "waiting_for_draw"
            self.view.update_board()
            self.view.clear_current_tile()
            self.next_turn()
        else:
            self.view.display_message("Position invalide pour cette tuile.")

    def handle_discard_tile(self):
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
        if isinstance(current_player, RandomPlayer):
            # Laisser l'IA jouer son tour
            move_success = current_player.take_turn(self.game.tile_bag)
            self.view.update_board()
            # Vérifier si l'IA a gagné
            if current_player.board.is_complete():
                self.view.display_message("L'IA a complété sa grille ! Vous avez perdu.")
                self.state = "game_over"
            # Vérifier si le joueur a gagné
            elif self.game.players[0].board.is_complete():
                self.view.display_message("Vous avez complété votre grille ! Vous avez gagné !")
                self.state = "game_over"
            elif move_success:
                # Continue game
                self.state = "waiting_for_draw"
            else:
                # Si l'IA ne peut plus jouer et la pioche est vide
                self.determine_game_over()

    def determine_game_over(self):
        message = self.game.determine_winner()
        self.view.display_message(message)
        self.state = "game_over"

    def is_game_over(self):
        return self.state == "game_over"



