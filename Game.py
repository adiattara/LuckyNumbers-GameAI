from model.TileBag import TileBag
import numpy as np
class Game:
    def __init__(self, players):
        self.players = players
        self.tile_bag = TileBag(len(players))
        self.initialize_players()
        self.current_player_index = 0
        self.game_over = False


    def initialize_players(self):
        """
        Initialise les joueurs en plaçant des tuiles aléatoires sur la diagonale principale de leur grille.
        :return:
        """
        for player in self.players:
            player.board.initialize_diagonal(self.tile_bag)

    def play(self):
        """
        Démarre le jeu et gère les tours des joueurs jusqu'à ce qu'un joueur gagne ou que la pioche soit épuisée.
        :return:
        """
        game_over = False
        self.current_player_index = 0

        while not game_over:
            current_player = self.players[self.current_player_index]
            print(f"\nC'est au tour de {current_player.name}.")
            # Demander au joueur de jouer
            turn_result ,tile_bag = current_player.take_turn(self.tile_bag)

            # Mettre à jour le sac de tuiles
            self.tile_bag = tile_bag

            # Vérifier si le joueur a pu effectuer son tour
            if turn_result is False:
                # Le joueur n'a pas pu effectuer son tour (plus de tuiles)
                print("\nLa pioche est épuisée et il n'y a plus de tuiles disponibles.")
                print("Le jeu se termine.")
                game_over = True
                self.determine_winner()
                break

            if current_player.board.is_complete():
                print(f"\n{current_player.name} a complété sa grille et a gagné la partie !")
                game_over = True
            else:
                self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def determine_winner(self):
        """
        Détermine le joueur gagnant en comptant le nombre de tuiles sur sa grille.
        :return:
        """
        # Déterminer le joueur avec le plus de tuiles sur sa grille
        max_tiles = -1
        winners = []
        for player in self.players:
            num_tiles = np.count_nonzero(player.board.grid) # Compter les éléments non nuls
            print(f"{player.name} a {num_tiles} tuiles sur sa grille.")
            if num_tiles > max_tiles:
                max_tiles = num_tiles
                winners = [player]
            elif num_tiles == max_tiles:
                winners.append(player)

        if len(winners) == 1:
            print(f"\n{winners[0].name} a gagné la partie avec {max_tiles} tuiles sur sa grille !")
            message = f"\n{winners[0].name} a gagné la partie avec {max_tiles} tuiles sur sa grille !"
        else:
            print(f"\nÉgalité entre les joueurs suivants avec {max_tiles} tuiles :")
            message = f"\nÉgalité entre les joueurs suivants avec {max_tiles} tuiles :"
            for winner in winners:
                print(f"- {winner.name}")

        return message

    def next_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def get_current_player(self):
        return self.players[self.current_player_index]