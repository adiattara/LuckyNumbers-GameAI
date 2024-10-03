import random

class TileBag:
    def __init__(self,nb_players):
        #TODO: Initialiser la pioche avec les tuiles numérotées de  1 à 20 (inclus) pour chaque joueur
        self.tiles = list(range(1, 21))*nb_players
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
