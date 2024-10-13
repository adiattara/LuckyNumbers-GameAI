import numpy as np


class Board:
    def __init__(self):
        self.grid = np.zeros((4, 4), dtype=int)

    def reset(self):
            """Réinitialise la grille à l'état vide."""
            self.grid = np.zeros((4, 4), dtype=int)


    def initialize_diagonal(self, tile_bag):
        """
        Initialise la grille en plaçant des tuiles triées sur la diagonale principale.
        :param tile_bag:
        :return:
        """
        tiles = [tile_bag.draw_tile() for _ in range(4)]
        tiles.sort()  # Assure que les tuiles sont en ordre croissant
        for i in range(4):
            self.grid[i, i] = tiles[i]

    def is_valid_move(self, row, col, tile):
        """
        Vérifie si le placement de la tuile est valide en respectant les règles :
        - Les tuiles dans une ligne doivent être strictement croissantes de gauche à droite.
        - Les tuiles dans une colonne doivent être strictement croissantes de haut en bas.
        - Placement libre sur la diagonale principale sans contraintes supplémentaires.
        """

        # Vérification pour la ligne (horizontalement)
        # Toutes les tuiles à gauche doivent être strictement inférieures
        for c in range(0, col):
            if self.grid[row, c] != 0 and tile <= self.grid[row, c]:
                return False

        # Toutes les tuiles à droite doivent être strictement supérieures
        for c in range(col + 1, 4):
            if self.grid[row, c] != 0 and tile >= self.grid[row, c]:
                return False

        # Vérification pour la colonne (verticalement)
        # Toutes les tuiles au-dessus doivent être strictement inférieures
        for r in range(0, row):
            if self.grid[r, col] != 0 and tile <= self.grid[r, col]:
                return False

        # Toutes les tuiles en dessous doivent être strictement supérieures
        for r in range(row + 1, 4):
            if self.grid[r, col] != 0 and tile >= self.grid[r, col]:
                return False

        # **Supprimer les contraintes diagonales**
        # Si vous souhaitez toujours placer sur la diagonale sans restrictions, ne pas ajouter de vérifications ici

        # Si aucune des règles n'est violée, le mouvement est valide
        return True

    def get_valid_vide_positions(self, tile):
        """
        Retourne les positions vides où la tuile peut être placée en respectant les règles de placement.
        """
        valid_positions = []
        for row in range(4):
            for col in range(4):
                if self.grid[row, col] == 0 and self.is_valid_move(row, col, tile):
                    valid_positions.append((row, col))
        return valid_positions

    def get_valid_vide_positions_bis(self, tile):
        """
        Retourne les positions vides où la tuile peut être placée en respectant les règles de placement.
        """
        valid_positions = []
        for row in range(4):
            for col in range(4):
                 if (self.is_valid_move(row, col, tile)):
                            valid_positions.append((row, col))
        return valid_positions




    def get_not_empty_valid_positions(self, tile):
        """
        Retourne une liste de positions occupées où la tuile donnée peut être placée
        en échangeant avec la tuile existante, tout en respectant les règles du jeu.
        """
        valid_positions = []
        for row in range(4):
            for col in range(4):
                if self.grid[row, col] != 0:
                    # Sauvegarder la tuile existante
                    temp_tile = self.grid[row, col]
                    # Simuler l'échange
                    self.grid[row, col] = tile

                    # Vérifier si l'échange respecte les règles du jeu
                    if self.is_valid_move(row, col, tile):
                        valid_positions.append((row, col))

                    # Restaurer la tuile d'origine
                    self.grid[row, col] = temp_tile
        return valid_positions




    def is_tile_placement_valid(self, row, col):
        """
        Check if placing a tile at (row, col) does not violate any placement rules.
        """
        # Check horizontal and vertical rules by calling is_valid_move
        return all(self.is_valid_move(row, c, self.grid[row, col]) for c in range(4)) and \
            all(self.is_valid_move(r, col, self.grid[r, col]) for r in range(4))

    def display_board(self):
        """
        Affiche la grille actuelle.
        """
        grid = self.grid
        print("\nVotre grille :")
        # Afficher les indices de colonnes
        header = "    " + "   ".join(str(col) for col in range(4))
        print(header)
        print("   " + "-" * 29)
        for row_idx, row in enumerate(grid):
            row_display = [str(row_idx)]  # Commencer par l'indice de ligne
            for col_idx, tile in enumerate(row):
                if tile != 0:
                    cell = str(int(tile)).rjust(2)
                else:
                    cell = "  "
                row_display.append(cell)
            print(' | '.join(row_display))
            print("   " + "-" * 29)

    def display_board_with_valid_positions(self, valid_positions):
        """
        Affiche la grille actuelle en mettant en évidence les positions valides.
        Les positions valides sont indiquées par un point '.'.
        """
        grid = self.grid
        print("\nVotre grille :")
        # Afficher les indices de colonnes
        header = "     " + "   ".join(str(col) for col in range(4))
        print(header)
        print("   " + "-" * 20)
        for row_idx, row in enumerate(grid):
            row_display = [str(row_idx)]  # Commencer par l'indice de ligne
            for col_idx, tile in enumerate(row):
                if tile != 0:
                    cell = str(int(tile)).rjust(2)
                elif (row_idx, col_idx) in valid_positions:
                    cell = " ."
                else:
                    cell = "  "
                row_display.append(cell)
            print(' | '.join(row_display))
            print("   " + "-" * 20)

    def place_tile(self, row, col, tile):
        """
        Place la tuile donnée à la position donnée.
        :param row:
        :param col:
        :param tile:
        :return:
        """
        old_tile = self.grid[row, col]
        self.grid[row, col] = tile
        return old_tile

    def get_tile(self, row, col):

        """
        Retourne la tuile à la position donnée.
        :param row:
        :param col:
        :return:
        """
        return self.grid[row, col]

    def is_complete(self):

        """
        Vérifie si la grille est complète.
        :return:
        """
        return np.all(self.grid != 0)

    def put_tile(self, tile, tile_bag, row, col):

        """
        Place la tuile donnée à la position donnée.
        :param tile:
        :param tile_bag:
        :param row:
        :param col:
        :return:
        """

        valid_empty_positions = self.get_valid_vide_positions(tile)
        valid_not_empty_positions = self.get_not_empty_valid_positions(tile)

        # Afficher les positions valides sous forme de liste
        print(f"Positions valides pour la tuile {tile} : {valid_empty_positions}")
        print(f"Positions occupées valides pour la tuile {tile} : {valid_not_empty_positions}")

        # Vérifier si la position est vide et  valide
        if (row, col) in valid_empty_positions:
            # Placer la tuile sur la grille
            self.place_tile(row, col, tile)
            print(f"Vous avez placé la tuile {tile} en position ({row}, {col}).")
            return True, tile_bag

        ## Vérifier si la position est occupée et valide
        elif (row, col) in valid_not_empty_positions:
            # recuperer la tuile existante
            old_tile = self.get_tile(row, col)
            # Défausser la tuile existante
            tile_bag.discard_pile = tile_bag.discard_tile(old_tile)
            # Placer la nouvelle tuile sur la grille
            self.place_tile(row, col, tile)
            print(f"Vous avez échangé la tuile {tile} avec la tuile existante en position ({row}, {col}).")

            return True, tile_bag
        else:
            print("Position invalide. Veuillez choisir parmi les positions valides.")
            return False, tile_bag

    def is_available_positions(self, tile):

        """
        Vérifie si le joueur peut placer la tuile donnée sur la grille.
        :param tile:
        :return:
        """

        valid_empty_positions = self.get_valid_vide_positions(tile)
        valid_not_empty_positions = self.get_not_empty_valid_positions(tile)
        if valid_empty_positions or valid_not_empty_positions:
            return True
        else:
            return False

    def get_discard_board_state_vector(self):
        state = self.grid.copy()
        return state.flatten()