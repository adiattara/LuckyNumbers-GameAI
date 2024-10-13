from ansible_collections.check_point.mgmt.plugins.module_utils.checkpoint import discard
from debugpy.common.timestamp import current

from model.TileBag import TileBag
import numpy as np


class Game:
    PLACE_TILE_START = 0
    PLACE_TILE_END = 15
    DISCARD_TILE = 16
    DRAW_FROM_DISCARD_START = 17
    DRAW_FROM_DISCARD_END = 36
    DRAW_FROM_BAG = 37

    def __init__(self, players):
        self.players = players
        self.tile_bag = TileBag(len(players))
        self.initialize_players()
        self.current_player_index = 0
        self.current_tile = 0
        self.game_over = False
        self.start = True
        self.PLACE_TILE_START = 0
        self.PLACE_TILE_END = 15
        self.DISCARD_TILE = 16
        self.DRAW_FROM_DISCARD_START = 17
        self.DRAW_FROM_DISCARD_END = 36
        self.DRAW_FROM_BAG = 37



    def initialize_players(self):
        """
        Initialise les joueurs en plaçant des tuiles aléatoires sur la diagonale principale de leur grille.
        :return:
        """
        for player in self.players:
            player.board.initialize_diagonal(self.tile_bag)

    def reset(self):
        """
        Réinitialise le jeu en remettant les tuiles dans le sac et en réinitialisant les grilles des joueurs.
        :return:
        """
        self.tile_bag.reset()
        for player in self.players:
            player.board.reset()
            self.current_tile = 0  #la main est vide
        self.current_player_index = 0

    def get_state_description(self):
        """Retourne le vecteur d'état complet."""

        player = self.players[self.current_player_index]

        adversary = self.players[(self.current_player_index + 1) % len(self.players)]

        # 1. Grille du joueur actuel (aplatie)
        player_bord_sate = player.board.get_discard_board_state_vector()


        # 2. Grille de l'adversaire (aplatie)
        adversary_board_state = adversary.board.get_discard_board_state_vector()


        # 3. Pile de défausse (count vector)
        discard_pile_state = self.tile_bag.get_discard_pile_state_vector()

        # Concatenation des vecteurs
        state_description = np.concatenate([
            player_bord_sate,
            adversary_board_state,
            discard_pile_state,
            self.current_tile
        ])

        return state_description.tolist()

    def get_valid_actions(self):
        """Retourne la liste des indices d'actions valides."""

        player = self.players[self.current_player_index]
        print(self.current_player_index)

        # Initialisation d'une liste de 38 actions valides (0 = invalide par défaut)
        valid_actions = [0] * 38

        # si la partie vient de commencer
        if (self.start == True):
            valid_actions[self.DRAW_FROM_BAG] = 1
            self.start = False
            return valid_actions

        # si le joueur n'a pas de tuile en main
        if(self.current_tile == 0):

            if len(self.tile_bag.tiles) > 0:
                valid_actions[self.DRAW_FROM_BAG] = 1

            if(len(self.tile_bag.tiles)==0):
                self.game_over = True

            if len(self.tile_bag.discard_pile)>0:
                valid_actions[self.DRAW_FROM_DISCARD_START:self.DRAW_FROM_DISCARD_END] = self.tile_bag.get_discard_pile_state_vector()

            return valid_actions

        # si le joueur a une tuile en main
        # 1. Placer la tuile actuelle
        for idx in range(self.PLACE_TILE_START, self.PLACE_TILE_END + 1):
            row, col = divmod(idx, 4)
            # Vérifie si la case est vide et si le coup est valide
            if player.board.is_valid_move(row, col, self.current_tile):

                valid_actions[idx] = 1

        # 2. Défausser la tuile actuelle (si elle existe)
        if self.current_tile !=0:
            valid_actions[self.DISCARD_TILE] = 1


        return valid_actions

    def available_actions_ids(self):
        """
        Retourne la liste des identifiants (indices) des actions disponibles pour le joueur actuel.
        """
        # Récupère les actions valides sous forme de liste avec des valeurs associées
        valid_actions = self.get_valid_actions()

        # Filtre les actions valides (les indices où l'action est possible)
        available_actions = [i for i, value in enumerate(valid_actions) if value != 0]


        return available_actions

    def step_action(self, action):

        """Exécute l'action choisie par l'agent."""
        player = self.players[self.current_player_index]

        reward = 0

        # 1. Piocher une tuile du sac (action 37)
        if action == 37:
                self.current_tile = self.tile_bag.draw_tile()
                # print(f"Le joueur a pioché la tuile {self.current_tile}")

        # 2. Placer une tuile sur la grille (actions 0 à 15)
        elif 0 <= action <= 15:
            row, col = divmod(action, 4)
            old_tile = player.board.place_tile(row, col, self.current_tile)
            if old_tile != 0:
                self.tile_bag.discard_tile(old_tile)

#             print(f"Le joueur a placé la tuile {self.current_tile} à ({row}, {col})")
            self.current_tile = 0  # Réinitialise la tuile après le placement

            if player.board.is_complete():
                self.game_over = True

        # 3. Défausser la tuile actuelle (action 16)
        elif action == 16:
                self.tile_bag.discard_tile(self.current_tile)
                self.current_tile = 0  # Le joueur n'a plus de tuile après la défausse
#                 print(f"Le joueur a défaussé la tuile.")


        # 4. Piocher une tuile de la pile de défausse (actions 17 à 36)
        elif 17 <= action <= 36:
            tile_index = action - 17
            self.current_tile = tile_index +1
            self.tile_bag.discard_pile.remove(tile_index+1)
#             print("Le joueur a pioché la tuile {tile_index} de la défausse.")

        return  player,reward,self.game_over





    def play(self):
        """
        Démarre le jeu et gère les tours des joueurs jusqu'à ce qu'un joueur gagne ou que la pioche soit épuisée.
        :return:
        """
        game_over = False
        self.current_player_index = 0

        while not game_over:
            current_player = self.players[self.current_player_index]
# #             print(f"\nC'est au tour de {current_player.name}.")
            # Demander au joueur de jouer
            turn_result, tile_bag = current_player.take_turn(self.tile_bag)

# #             print(self.get_state_description())

            # Mettre à jour le sac de tuiles
            self.tile_bag = tile_bag

            # Vérifier si le joueur a pu effectuer son tour
            if turn_result is False:
                # Le joueur n'a pas pu effectuer son tour (plus de tuiles)
# #                 print("\nLa pioche est épuisée et il n'y a plus de tuiles disponibles.")
# #                 print("Le jeu se termine.")
                game_over = True
                self.determine_winner()
                break

            if current_player.board.is_complete():
# #                 print(f"\n{current_player.name} a complété sa grille et a gagné la partie !")
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
            num_tiles = np.count_nonzero(player.board.grid)  # Compter les éléments non nuls
# #             print(f"{player.name} a {num_tiles} tuiles sur sa grille.")
            if num_tiles > max_tiles:
                max_tiles = num_tiles
                winners = [player]
            elif num_tiles == max_tiles:
                winners.append(player)

        if len(winners) == 1:
# #             print(f"\n{winners[0].name} a gagné la partie avec {max_tiles} tuiles sur sa grille !")
            message = f"\n{winners[0].name} a gagné la partie avec {max_tiles} tuiles sur sa grille !"
        else:
# #             print(f"\nÉgalité entre les joueurs suivants avec {max_tiles} tuiles :")
            message = f"\nÉgalité entre les joueurs suivants avec {max_tiles} tuiles :"
            for winner in winners:
# #                 print(f"- {winner.name}")
                    pass

        return message


    def next_player(self):
            self.current_player_index = (self.current_player_index + 1) % len(self.players)


    def get_current_player(self):
            return self.players[self.current_player_index]
