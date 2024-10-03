from .Player import Player
class HumanPlayer(Player):

    def choose_pile_or_discard(self, tile_bag):
        """
        Demander au joueur de choisir entre piocher dans le sac de tuiles ou dans la défausse.
        Permet au joueur de choisir une tuile spécifique dans la défausse si disponible.
        :param tile_bag: TileBag object contenant le sac de tuiles et la défausse.
        :return: La tuile choisie par le joueur.
        """
        # Afficher les tuiles dans la défausse si elle n'est pas vide
        if len(tile_bag.discard_pile) > 0:
            print("Tuiles dans la défausse :", tile_bag.discard_pile)
        else:
            print("La défausse est vide, piochez dans le sac de tuiles.")
            return 'p'

        action_game_list = ['p', 'd']
        while True:
            chosen_action = input("Voulez-vous piocher dans le sac de tuiles ou dans la défausse ? (pile_bag/discard_bag)(p or d) : ")
            if chosen_action not in action_game_list:
                print("Veuillez entrer une action valide.")
            elif chosen_action == 'd':
                if len(tile_bag.discard_pile) == 0:
                    print("La défausse est vide. Vous devez piocher dans le sac de tuiles.")
                else:
                    # Le joueur choisit une tuile dans la défausse
                    return self.choose_discarded_tile(tile_bag)
            else:
                return 'p'

    def choose_discarded_tile(self, tile_bag):
        """
        Permet au joueur de choisir une tuile spécifique dans la défausse.
        :param tile_bag: Objet TileBag contenant les tuiles et la défausse.
        :return: La tuile choisie par le joueur.
        """
        print("Tuiles disponibles dans la défausse :", tile_bag.discard_pile)
        while True:
            try:
                tile_choice = int(input("Entrez le numéro de la tuile que vous souhaitez prendre dans la défausse : "))
                if tile_choice in tile_bag.discard_pile:
                    tile_bag.discard_pile.remove(tile_choice)
                    return tile_choice
                else:
                    print("Cette tuile n'est pas dans la défausse, veuillez choisir une autre tuile.")
            except ValueError:
                print("Veuillez entrer un nombre valide.")

    def take_turn(self, tile_bag):
        """
        Prendre un tour pour le joueur humain.
        :param tile_bag:
        :return:
        """

        # Choisir de piocher dans le sac de tuiles ou dans la défausse
        human_choice = self.choose_pile_or_discard(tile_bag)

        # Si le joueur a choisi de piocher, alors appeler la fonction de pioche
        if human_choice == 'p':
            tile = tile_bag.piocher('p')
        else:
            # Si le joueur a choisi une tuile dans la défausse, la tuile est directement retournée
            tile = human_choice

        # Vérifier si la pioche est épuisée
        if tile == -1:
            print(f"{self.name}, il n'y a plus de tuiles à piocher.")
            return False, tile_bag  # Retourner False pour indiquer que la partie est terminée

        # Afficher les informations pour le joueur
        self.display_human_information(tile)

        # Demander au joueur s'il veut placer la tuile ou la défausser
        action = input("Voulez-vous placer la tuile (p) ou la défausser (d) ? ")
        if action == 'd':
            tile_bag.discard_tile(tile)
            print(f"Tuile {tile} défaussée.")
            return True, tile_bag

        # Demander au joueur où placer la tuile, si placable
        while True:
            try:
                row = int(input("Entrez le numéro de ligne : "))
                col = int(input("Entrez le numéro de colonne : "))
                state, tile_bag = self.board.put_tile(tile, tile_bag, row, col)
                if state:
                    return True, tile_bag
            except ValueError:
                print("Veuillez entrer des nombres entiers valides.")


    def display_human_information(self,tile):

            print(f"{self.name}, vous avez pioché la tuile {tile}.")

            # Obtenir les placement vide valides pour la tuile
            valid_empty_positions = self.board.get_valid_vide_positions(tile)

            # Obtenir les placements non vides valides pour la tuile
            valid_not_empty_positions = self.board.get_not_empty_valid_positions(tile)

            # Afficher la grille avec les positions valides
            self.board.display_board_with_valid_positions(valid_empty_positions)

            # Afficher les positions valides sous forme de liste
            print(f"Positions valides pour la tuile {tile} : {valid_empty_positions}")
            print(f"Positions occupées valides pour la tuile {tile} : {valid_not_empty_positions}")

# Compare this snippet from TileBag.py:
