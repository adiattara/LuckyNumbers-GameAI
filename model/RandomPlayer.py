import random
from .Player import Player

class RandomPlayer(Player):

    def take_turn(self, tile_bag):
        """
        Prendre un tour pour le joueur ordinateur de manière aléatoire.
        :param tile_bag:
        :return:
        """

        if random.choice(['p', 'd']) == 'p' or len(tile_bag.discard_pile) == 0:
            # Pioche dans le sac
            tile = tile_bag.piocher('p')
            if tile == -1:
                # Si la pioche est vide, retourner False pour indiquer la fin de la partie
                return False, tile_bag

            print(f"Ordinateur a pioché la tuile {tile}.")
        else:
            # Choisir une tuile dans la défausse
            tile = random.choice(tile_bag.discard_pile)
            tile_bag.discard_pile.remove(tile)
            print(f"Ordinateur a pris la tuile {tile} de la défausse.")

        # Obtenir les positions vides valides
        valid_empty_positions = self.board.get_valid_vide_positions(tile)
        # Obtenir les positions occupées valides pour un échange
        valid_not_empty_positions = self.board.get_not_empty_valid_positions(tile)

        if valid_empty_positions or valid_not_empty_positions:
            # Si des positions valides existent, choisir aléatoirement parmi elles
            if random.choice(['place', 'exchange']) == 'place' and valid_empty_positions:
                # Placer la tuile dans une position vide aléatoirement
                position = random.choice(valid_empty_positions)
                row, col = position
                self.board.place_tile(row, col, tile)
                print(f"Ordinateur a placé la tuile {tile} en position {row}, {col}.")
            elif valid_not_empty_positions:
                # Échanger la tuile avec une position occupée aléatoirement
                position = random.choice(valid_not_empty_positions)
                row, col = position
                old_tile = self.board.get_tile(row, col)
                tile_bag.discard_tile(old_tile)
                self.board.place_tile(row, col, tile)
                print(f"Ordinateur a échangé la tuile {tile} avec la tuile {old_tile} en position {row}, {col}.")
        else:
            # Si aucune position valide, défausser la tuile
            tile_bag.discard_tile(tile)
            print(f"Ordinateur a défaussé la tuile {tile}.")

        # Afficher la grille de l'ordinateur après son tour
        print("\nGrille de l'ordinateur :")
        self.board.display_board()  # Affiche la grille actuelle de l'ordinateur

        return True, tile_bag
