# from ansible_collections.check_point.mgmt.plugins.module_utils.checkpoint import discard
# from debugpy.common.timestamp import current

from model.TileBag import TileBag
import numpy as np
import random


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
            player.board.initialize_diagonal(self.tile_bag)
        self.current_tile = 0  # la main est vide
        self.current_player_index = 0
        self.game_over = False
        self.start = True

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

        # Convert current_tile to a numpy array with the correct dimensions
        current_tile_array = np.array([self.current_tile])

        # Concatenation des vecteurs
        state_description = np.concatenate([
            player_bord_sate,
            adversary_board_state,
            discard_pile_state,
            current_tile_array
        ])

        return state_description.tolist()

    def get_valid_actions(self):
        """Retourne la liste des indices d'actions valides."""
        player = self.players[self.current_player_index]
        # print(f"Current player index: {self.current_player_index}")

        # Initialisation d'une liste de 38 actions valides (0 = invalide par défaut)
        valid_actions = [0] * 38
        # print(f"État actuel du jeu pour {self.players[self.current_player_index].name}:")
        # print(f"Tuile courante: {self.current_tile}")
        # print(f"Tuiles restantes dans le sac: {len(self.tile_bag.tiles)}")
        # print(f"Tuiles dans la défausse: {self.tile_bag.get_discard_pile_state_vector()}")

        # Si la partie vient de commencer
        if self.start:
            valid_actions[self.DRAW_FROM_BAG] = 1
            self.start = False
            print("Start of the game, only DRAW_FROM_BAG is valid")
            return valid_actions
        # print("start situation : ", self.start)
        # Si le joueur n'a pas de tuile en main
        if (self.current_tile == 0):

            if len(self.tile_bag.tiles) > 0:
                valid_actions[self.DRAW_FROM_BAG] = 1

            if (len(self.tile_bag.tiles) == 0):
                self.game_over = True

            if len(self.tile_bag.discard_pile) > 0:
                valid_actions[
                self.DRAW_FROM_DISCARD_START:self.DRAW_FROM_DISCARD_END] = self.tile_bag.get_discard_pile_state_vector()

            print(f"Tuile en main: {self.current_tile}.\n Actions valides: {valid_actions}")
            return valid_actions

        # Si le joueur a une tuile en main
        # 1. Placer la tuile actuelle
        for idx in range(self.PLACE_TILE_START, self.PLACE_TILE_END + 1):
            row, col = divmod(idx, 4)
            if player.board.is_valid_move(row, col, self.current_tile):
                valid_actions[idx] = 1

        # 2. Défausser la tuile actuelle
        valid_actions[self.DISCARD_TILE] = 1

        # print(f"Actions valides actuelles: {[i for i, v in enumerate(valid_actions) if v == 1]}")
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
        """Exécute l'action choisie par l'agent et gère la progression du jeu."""
        player = self.players[self.current_player_index]
        reward = 0

        if action == self.DRAW_FROM_BAG:
            print("Action : Piocher une tuile depuis le sac.")
            # Piocher une nouvelle tuile si le sac n'est pas vide
            self.current_tile = self.tile_bag.draw_tile() if len(self.tile_bag.tiles) > 0 else 0
            # print(f"Nouvelle tuile tirée: {self.current_tile}")
            reward += 10 if self.current_tile else -10  # Récompense si tirage réussi

        elif self.DRAW_FROM_DISCARD_START <= action <= self.DRAW_FROM_DISCARD_END:

            discard_index = action - self.DRAW_FROM_DISCARD_START
            if discard_index < len(self.tile_bag.discard_pile):
                self.current_tile = self.tile_bag.discard_pile[discard_index]
                self.tile_bag.discard_pile.pop(discard_index)
                reward += 3
                # print(f"Tuile piochée depuis la défausse: {self.current_tile}")
            else:
                reward -= 10  # Pénalité si tirage de défausse invalide

        elif action == self.DISCARD_TILE:
            print("Action : Défausser la tuile.")
            # Défausser la tuile si elle est valide
            if self.current_tile != 0:
                self.tile_bag.discard_tile(self.current_tile)
                self.current_tile = 0
                reward += 1
                # print("Tuile défaussée.")

        elif 0 <= action <= 15:
            print(f"Action : placer la tuile {action} à la position correspondante à l'action {action}.")
            # Placer la tuile sur la grille
            row, col = divmod(action, 4)
            if player.board.is_valid_move(row, col, self.current_tile):
                old_tile = player.board.place_tile(row, col, self.current_tile)
                if old_tile != 0:
                    self.tile_bag.discard_tile(old_tile)
                self.current_tile = 0
                reward += 50
                # print(f"Tuile placée en position ({row}, {col})")

                if player.board.is_complete():
                    self.game_over = True
                    print("Grille complète ! Fin du jeu.")

        else:
            reward -= 10  # Pénalité pour action invalide

        if not self.tile_bag.tiles and not self.tile_bag.discard_pile:
            print("Pioche et défausse vides, fin de la partie.")
            self.game_over = True

        if not self.tile_bag.tiles and self.tile_bag.discard_pile:
            self.tile_bag.tiles = self.tile_bag.discard_pile[:]
            self.tile_bag.discard_pile = []
            random.shuffle(self.tile_bag.tiles)
            print("Refilled tile bag from discard pile.")

        # Vérifie si une tuile doit être piochée pour le prochain tour
        if self.current_tile == 0 and not self.game_over:
            self.current_tile = self.tile_bag.draw_tile() if len(self.tile_bag.tiles) > 0 else 0
            # print(f"Nouvelle tuile après action: {self.current_tile}")

        self.done = self.game_over
        return player, reward, self.done

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
        print(f"Changement de joueur, joueur actuel avant changement: {self.players[self.current_player_index].name}")
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        print(f"Joueur actuel après changement: {self.players[self.current_player_index].name}")

    def get_current_player(self):
            return self.players[self.current_player_index]
