import random

import numpy as np
class TileBag:
    def __init__(self,nb_players=2):

        self.tiles = list(range(1, 21))*2
        random.shuffle(self.tiles)
        self.discard_pile = []

    def reset(self):
        self.tiles = list(range(1, 21)) * 2
        random.shuffle(self.tiles)
        self.discard_pile = []

    def draw_tile(self):
        #TODO: Gérer le cas où la pioche est vide
        if not self.tiles:
            # Reconstituer la pioche à partir de la défausse
            return -1
        return self.tiles.pop()

    def discard_tile(self, tile):
        self.discard_pile.append(tile)
        return self.discard_pile


    def piocher(self, policy):
        ## s'il choisit de piocher dans le sac de défausse
        if policy == 'd':

            if self.discard_pile:

                tile = self.discard_pile.pop()

            else:
                tile = self.draw_tile()
        ## s'il choisit de piocher dans le sac de tuiles
        if policy == 'p':
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
