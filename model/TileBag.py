import random

import numpy as np


class TileBag:
    def __init__(self, nb_players):

        self.tiles = list(range(1, 21)) * 2
        random.shuffle(self.tiles)
        self.discard_pile = []

    def reset(self):
        self.tiles = list(range(1, 21)) * 2
        random.shuffle(self.tiles)
        self.discard_pile = []

    def draw_tile(self):
        if not self.tiles and not self.discard_pile:
            #print("Pioche et défausse vides, fin de la partie.")
            return -1
        elif not self.tiles and self.discard_pile:
            #print("Reconstitution de la pioche à partir de la défausse.")
            self.tiles = self.discard_pile[:]
            self.discard_pile = []
            random.shuffle(self.tiles)
        tile = self.tiles.pop()
        #print(f"Pioché la tuile: {tile}")
        return tile

    def discard_tile(self, tile):
        self.discard_pile.append(tile)
        # print(f"Tuile {tile} défaussée.")
        return self.discard_pile

    def piocher(self, policy):
        ## s'il choisit de piocher dans le sac de défausse
        if policy == 'd':
            if self.discard_pile:
                tile = self.discard_pile.pop()
            else:
                print("Défausse vide, pioche dans le sac de tuiles.")
                tile = self.draw_tile()

        elif policy == 'p':
                tile = self.draw_tile()

        return tile

    def get_discard_pile(self):
        # Retourner la défausse
        return self.discard_pile

    def get_tile_list(self):
        return self.tiles

    def get_discard_pile_state_vector(self):
        """
        Retourne un vecteur d'état de la défausse.
        :return:
        """
        # la taille du vecteur est de 20
        discard_pile_vector = np.zeros(20, dtype=int)
        for tile in self.discard_pile:
            discard_pile_vector[tile - 1] += 1

        return discard_pile_vector.flatten()
