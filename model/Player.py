from .Board import Board
class Player:
    def __init__(self, name):
        self.name = name
        self.board = Board()

    def take_turn(self, tile_bag):
        # Cette méthode sera implémentée dans les sous-classes
        pass


