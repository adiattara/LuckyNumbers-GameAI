# import pygame
# class GameGUI:
#     def __init__(self, game):
#         self.game = game  # Instance du jeu
#         pygame.init()
#         # Initialiser la fenêtre avec une taille fixe de 800x600 pixels
#         self.screen_width = 800
#         self.screen_height = 600
#         self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
#         pygame.display.set_caption("Lucky Numbers")
#         self.clock = pygame.time.Clock()
#         # Définir la taille fixe des cellules
#         self.cell_size = 80  # Taille fixe des cellules en pixels
#         # Calculer l'origine de la grille pour la centrer horizontalement
#         grid_total_width = self.cell_size * 4  # La grille fait 4 cellules de large
#         self.grid_origin_x = (self.screen_width - grid_total_width) // 2  # Centrer horizontalement
#         self.grid_origin_y = 50  # Position Y de la grille
#         # Variables pour gérer l'état du jeu
#         self.current_tile = None
#         self.state = "waiting_for_draw"  # État initial
#         self.message = ""
#         self.message_timer = 0  # Pour afficher les messages pendant un certain temps
#         # Initialiser les rectangles pour les boutons
#         self.draw_button_rect = None
#         self.discard_current_tile_button_rect = None
#         # Rectangles des tuiles de la défausse
#         self.discard_tiles_rects = []
#
#     def run(self):
#         running = True
#         while running:
#             self.clock.tick(60)  # Limite à 60 FPS
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     running = False
#                 elif event.type == pygame.MOUSEBUTTONDOWN:
#                     pos = pygame.mouse.get_pos()
#                     self.handle_click(pos)
#             # Mettre à jour l'affichage
#             self.draw()
#             pygame.display.flip()
#             # Vérifier si le jeu est terminé
#             if self.state == "game_over":
#                 # Afficher un message de fin de partie
#                 self.draw()
#                 pygame.display.flip()
#                 pygame.time.wait(5000)  # Attendre 5 secondes
#                 running = False
#             elif self.game.players[0].board.is_complete():
#                 # Le joueur a complété sa grille
#                 self.message = "Vous avez complété votre grille ! Vous avez gagné !"
#                 self.message_timer = pygame.time.get_ticks()
#                 self.state = "game_over"
#             elif self.game.players[1].board.is_complete():
#                 # L'IA a complété sa grille
#                 self.message = "L'IA a complété sa grille ! Vous avez perdu."
#                 self.message_timer = pygame.time.get_ticks()
#                 self.state = "game_over"
#
#
#
#         pygame.quit()
#
#     def draw(self):
#         # Effacer l'écran
#         self.screen.fill((255, 255, 255))  # Fond blanc
#         # Dessiner la grille du joueur
#         self.draw_board()
#         # Dessiner la tuile actuelle
#         self.draw_current_tile()
#         # Dessiner le bouton pour piocher
#         self.draw_draw_button()
#         # Dessiner la pile de défausse
#         self.draw_discard_pile()
#         # Dessiner le bouton pour défausser la tuile actuelle si nécessaire
#         if self.state == "waiting_for_move" and self.current_tile is not None:
#             self.draw_discard_current_tile_button()
#
#         # Afficher les messages
#         self.draw_message()
#
#     def draw_board(self):
#         board = self.game.players[0].board.grid  # Grille du joueur humain
#         for row in range(4):
#             for col in range(4):
#                 rect = pygame.Rect(
#                     self.grid_origin_x + col * self.cell_size,
#                     self.grid_origin_y + row * self.cell_size,
#                     self.cell_size,
#                     self.cell_size
#                 )
#                 pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)  # Contour de la cellule
#
#                 tile_value = board[row][col]
#                 if tile_value != 0:
#                     # Afficher la tuile
#                     font = pygame.font.Font(None, 36)
#                     text = font.render(str(tile_value), True, (0, 0, 0))
#                     text_rect = text.get_rect(center=rect.center)
#                     self.screen.blit(text, text_rect)
#
#     def draw_current_tile(self):
#         if self.current_tile is not None:
#             rect = pygame.Rect(self.screen_width - 200, 200, 80, 80)
#             pygame.draw.rect(self.screen, (200, 200, 0), rect)
#             font = pygame.font.Font(None, 36)
#             text = font.render(str(self.current_tile), True, (0, 0, 0))
#             text_rect = text.get_rect(center=rect.center)
#             self.screen.blit(text, text_rect)
#             # Libellé
#             font = pygame.font.Font(None, 24)
#             label_text = font.render("Tuile actuelle", True, (0, 0, 0))
#             label_rect = label_text.get_rect(center=(rect.centerx, rect.top - 20))
#             self.screen.blit(label_text, label_rect)
#
#     def draw_draw_button(self):
#         # Bouton pour piocher dans la pioche
#         button_width = 150
#         button_height = 40
#         x = self.screen_width - button_width - 30  # 30 pixels de marge à droite
#         y = 50  # Position Y du premier bouton
#         button_rect = pygame.Rect(x, y, button_width, button_height)
#         pygame.draw.rect(self.screen, (0, 200, 0), button_rect)
#         font = pygame.font.Font(None, 24)
#         text = font.render("Piocher Pioche", True, (255, 255, 255))
#         text_rect = text.get_rect(center=button_rect.center)
#         self.screen.blit(text, text_rect)
#         self.draw_button_rect = button_rect
#
#     def draw_discard_current_tile_button(self):
#         # Bouton pour défausser la tuile actuelle
#         button_width = 150
#         button_height = 40
#         x = self.screen_width - button_width - 30  # 30 pixels de marge à droite
#         y = 100  # Position Y sous le premier bouton
#         button_rect = pygame.Rect(x, y, button_width, button_height)
#         pygame.draw.rect(self.screen, (200, 0, 0), button_rect)
#         font = pygame.font.Font(None, 20)
#         text = font.render("Défausser Tuile", True, (255, 255, 255))
#         text_rect = text.get_rect(center=button_rect.center)
#         self.screen.blit(text, text_rect)
#         self.discard_current_tile_button_rect = button_rect
#
#
#
#     def draw_discard_pile(self):
#         # Afficher la pile de défausse
#         start_x = 20  # Position de départ en X
#         start_y = self.screen_height - 100  # Position de départ en Y, 100 pixels au-dessus du bas de l'écran
#         tile_width = 30
#         tile_height = 45
#         spacing = 5
#         tiles_per_row = (self.screen_width - 40) // (tile_width + spacing)  # Calculer le nombre de tuiles par ligne
#
#         # Calculer le nombre de lignes nécessaires
#         num_tiles = len(self.game.tile_bag.discard_pile)
#         num_rows = (num_tiles - 1) // tiles_per_row + 1
#
#         # Dessiner un rectangle pour la zone de la défausse
#         area_height = num_rows * (tile_height + spacing) + 20
#         pygame.draw.rect(self.screen, (220, 220, 220), (start_x - 10, start_y - area_height - 10, self.screen_width - 40, area_height + 20))
#
#         # Afficher chaque tuile de la défausse
#         self.discard_tiles_rects = []  # Pour stocker les rectangles des tuiles
#         for index, tile in enumerate(self.game.tile_bag.discard_pile):
#             row = index // tiles_per_row
#             col = index % tiles_per_row
#             x = start_x + col * (tile_width + spacing)
#             y = start_y - (row + 1) * (tile_height + spacing)
#             rect = pygame.Rect(x, y, tile_width, tile_height)
#             pygame.draw.rect(self.screen, (200, 200, 200), rect)
#             font = pygame.font.Font(None, 18)
#             text = font.render(str(tile), True, (0, 0, 0))
#             text_rect = text.get_rect(center=rect.center)
#             self.screen.blit(text, text_rect)
#             self.discard_tiles_rects.append((rect, tile))  # Stocker le rectangle et la valeur de la tuile
#
#         # Afficher le libellé "Défausse"
#         font = pygame.font.Font(None, 24)
#         label_text = font.render("Défausse", True, (0, 0, 0))
#         self.screen.blit(label_text, (start_x, start_y - area_height - 30))
#
#     def draw_message(self):
#         if self.message:
#             current_time = pygame.time.get_ticks()
#             if current_time - self.message_timer < 3000:  # Afficher pendant 3 secondes
#                 font = pygame.font.Font(None, 24)
#                 text = font.render(self.message, True, (255, 0, 0))
#                 text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height - 30))
#                 self.screen.blit(text, text_rect)
#             else:
#                 self.message = ""
#
#     def handle_click(self, pos):
#         x, y = pos
#         # Vérifier si le clic est sur une tuile de la défausse
#         if hasattr(self, 'discard_tiles_rects'):
#             for rect, tile in self.discard_tiles_rects:
#                 if rect.collidepoint(pos):
#                     self.draw_tile_from_discard(tile)
#                     return
#         # Vérifier si le clic est sur le bouton de pioche
#         if self.draw_button_rect.collidepoint(pos):
#             self.draw_tile(from_discard=False)
#             return
#         # Vérifier si le clic est sur le bouton pour défausser la tuile actuelle
#         if hasattr(self, 'discard_current_tile_button_rect') and self.discard_current_tile_button_rect.collidepoint(pos):
#             self.discard_current_tile()
#             self.ai_take_turn()
#             return
#         # Vérifier si le clic est sur la grille
#         self.handle_grid_click(pos)
#
#     def handle_grid_click(self, pos):
#         x, y = pos
#         col = (x - self.grid_origin_x) // self.cell_size
#         row = (y - self.grid_origin_y) // self.cell_size
#
#         if 0 <= row < 4 and 0 <= col < 4:
#             # Traiter le clic sur la cellule (row, col)
#             self.process_player_move(int(row), int(col))
#
#     def draw_tile(self, from_discard=False):
#         if self.state == "waiting_for_draw":
#             if from_discard:
#                 tile = self.game.tile_bag.piocher('d')  # Piocher depuis la défausse
#                 if tile == -1:
#                     self.message = "La défausse est vide."
#                     self.message_timer = pygame.time.get_ticks()
#                     return
#             else:
#                 tile = self.game.tile_bag.piocher('p')  # Piocher depuis la pioche
#                 if tile == -1:
#                     self.message = self.game.determine_winner()
#                     self.state = "game_over"
#
#                     self.message_timer = pygame.time.get_ticks()
#                     return
#             self.current_tile = tile
#             self.state = "waiting_for_move"
#             print(f"Vous avez pioché la tuile {tile}.")
#
#         else:
#             self.message = "Vous ne pouvez pas piocher maintenant."
#             self.message_timer = pygame.time.get_ticks()
#
#     def draw_tile_from_discard(self, tile):
#         if self.state == "waiting_for_draw":
#             # Retirer la tuile de la défausse
#             self.game.tile_bag.discard_pile.remove(tile)
#             self.current_tile = tile
#             self.state = "waiting_for_move"
#             print(f"Vous avez pioché la tuile {tile} depuis la défausse.")
#         else:
#             self.message = "Vous ne pouvez pas piocher maintenant."
#             self.message_timer = pygame.time.get_ticks()
#
#     def discard_current_tile(self):
#         if self.current_tile is not None:
#             self.game.tile_bag.discard_tile(self.current_tile)
#             print(f"Vous avez défaussé la tuile {self.current_tile}.")
#             self.current_tile = None
#             self.state = "next_turn"
#         else:
#             self.message = "Aucune tuile à défausser."
#             self.message_timer = pygame.time.get_ticks()
#
#     def process_player_move(self, row, col):
#         if self.state == "waiting_for_move" and self.current_tile is not None:
#             board = self.game.players[0].board
#             tile = self.current_tile
#
#             # Obtenir les positions valides
#             valid_empty_positions = board.get_valid_vide_positions(tile)
#             valid_not_empty_positions = board.get_not_empty_valid_positions(tile)
#
#             if (row, col) in valid_empty_positions:
#                 board.place_tile(row, col, tile)
#                 self.current_tile = None
#                 self.state = "waiting_for_draw"
#                 # Faire jouer l'IA
#                 self.ai_take_turn()
#             elif (row, col) in valid_not_empty_positions:
#                 old_tile = board.get_tile(row, col)
#                 self.game.tile_bag.discard_tile(old_tile)
#                 board.place_tile(row, col, tile)
#                 self.current_tile = None
#                 self.state = "waiting_for_draw"
#                 # Faire jouer l'IA
#                 self.ai_take_turn()
#             elif self.state == "next_turn":
#                 self.message = "Vous avez déjà joué ce tour."
#                 self.message_timer = pygame.time.get_ticks()
#                 self.ai_take_turn()
#             else:
#                 # Position invalide
#                 self.message = "Position invalide pour cette tuile."
#                 self.message_timer = pygame.time.get_ticks()
#
#
#         else:
#             self.message = "Vous devez piocher une tuile."
#             self.message_timer = pygame.time.get_ticks()
#
#     def ai_take_turn(self):
#         ai_player = self.game.players[1]
#         turn_result = ai_player.take_turn(self.game.tile_bag)
#         if not turn_result:
#             self.message = "La pioche est vide. Fin de la partie."
#             self.message_timer = pygame.time.get_ticks()
#             self.state = "game_over"
#             return
#         if ai_player.board.is_complete():
#             self.message = "L'IA a complété sa grille ! Vous avez perdu."
#             self.message_timer = pygame.time.get_ticks()
#             self.state = "game_over"
#         elif self.game.players[0].board.is_complete():
#             self.message = "Félicitations ! Vous avez gagné."
#             self.message_timer = pygame.time.get_ticks()
#             self.state = "game_over"
#         self.state = "waiting_for_draw"
#

# game_gui.py

import pygame
from GameController import GameController

class GameGUI:
    def __init__(self, game):
        self.game = game  # Le modèle
        self.controller = GameController(game, self)  # Le contrôleur
        pygame.init()
        # Initialiser la fenêtre avec une taille fixe de 800x600 pixels
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Lucky Numbers")
        self.clock = pygame.time.Clock()
        # Définir la taille fixe des cellules
        self.cell_size = 80  # pixels
        # Calculer l'origine de la grille pour la centrer horizontalement
        grid_total_width = self.cell_size * 4
        self.grid_origin_x = (self.screen_width - grid_total_width) // 2
        self.grid_origin_y = 50  # Marge supérieure
        # Informations sur la tuile actuelle
        self.current_tile = None
        # Gestion des messages
        self.message = ""
        self.message_timer = 0
        # Rectangles des boutons
        self.draw_button_rect = None
        self.discard_current_tile_button_rect = None
        # Rectangles des tuiles de la défausse
        self.discard_tiles_rects = []

    def run(self):
        running = True
        while running:
            self.clock.tick(60)  # Limite à 60 FPS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.handle_click(pos)
            # Dessiner l'interface
            self.draw()
            pygame.display.flip()
            # Vérifier si le jeu est terminé
            if self.controller.is_game_over():
                pygame.time.wait(5000)  # Attendre 5 secondes avant de fermer
                running = False
        pygame.quit()

    def draw(self):
        # Effacer l'écran
        self.screen.fill((255, 255, 255))  # Fond blanc
        # Dessiner la grille du joueur
        self.draw_board()
        # Dessiner la tuile actuelle
        self.draw_current_tile()
        # Dessiner le bouton pour piocher
        self.draw_draw_button()
        # Dessiner la pile de défausse
        self.draw_discard_pile()
        # Dessiner le bouton pour défausser la tuile actuelle si nécessaire
        if self.controller.state == "waiting_for_move" and self.controller.current_tile is not None:
            self.draw_discard_current_tile_button()

        # Afficher les messages
        self.draw_message()

    def draw_board(self):
        board = self.game.players[0].board.grid
        for row in range(4):
            for col in range(4):
                rect = pygame.Rect(
                    self.grid_origin_x + col * self.cell_size,
                    self.grid_origin_y + row * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)  # Contour noir

                tile_value = board[row][col]
                if tile_value != 0:
                    # Afficher la tuile
                    font = pygame.font.Font(None, 36)
                    text = font.render(str(tile_value), True, (0, 0, 0))
                    text_rect = text.get_rect(center=rect.center)
                    self.screen.blit(text, text_rect)

    def draw_current_tile(self):
        if self.controller.current_tile is not None:
            rect = pygame.Rect(self.screen_width - 200, 200, 80, 80)
            pygame.draw.rect(self.screen, (200, 200, 0), rect)  # Jaune
            font = pygame.font.Font(None, 36)
            text = font.render(str(self.controller.current_tile), True, (0, 0, 0))
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)
            # Libellé
            font = pygame.font.Font(None, 24)
            label_text = font.render("Tuile actuelle", True, (0, 0, 0))
            label_rect = label_text.get_rect(center=(rect.centerx, rect.top - 20))
            self.screen.blit(label_text, label_rect)

    def draw_draw_button(self):
        # Bouton pour piocher dans la pioche
        button_width = 150
        button_height = 40
        x = self.screen_width - button_width - 30  # 30 pixels de marge à droite
        y = 50  # Position Y du premier bouton
        button_rect = pygame.Rect(x, y, button_width, button_height)
        pygame.draw.rect(self.screen, (0, 200, 0), button_rect)  # Vert
        font = pygame.font.Font(None, 24)
        text = font.render("Piocher Pioche", True, (255, 255, 255))
        text_rect = text.get_rect(center=button_rect.center)
        self.screen.blit(text, text_rect)
        self.draw_button_rect = button_rect

    def draw_discard_current_tile_button(self):
        # Bouton pour défausser la tuile actuelle
        button_width = 150
        button_height = 40
        x = self.screen_width - button_width - 30  # 30 pixels de marge à droite
        y = 100  # Position Y sous le premier bouton
        button_rect = pygame.Rect(x, y, button_width, button_height)
        pygame.draw.rect(self.screen, (200, 0, 0), button_rect)  # Rouge
        font = pygame.font.Font(None, 20)
        text = font.render("Défausser Tuile", True, (255, 255, 255))
        text_rect = text.get_rect(center=button_rect.center)
        self.screen.blit(text, text_rect)
        self.discard_current_tile_button_rect = button_rect

    def draw_discard_pile(self):
        # Afficher la pile de défausse
        start_x = 20  # Marge gauche
        start_y = self.screen_height - 100  # 100 pixels au-dessus du bas
        tile_width = 30
        tile_height = 45
        spacing = 5
        tiles_per_row = (self.screen_width - 40) // (tile_width + spacing)  # Calculer le nombre de tuiles par ligne

        # Calculer le nombre de lignes nécessaires
        num_tiles = len(self.game.tile_bag.discard_pile)
        num_rows = (num_tiles - 1) // tiles_per_row + 1

        # Dessiner un rectangle pour la zone de la défausse
        area_height = num_rows * (tile_height + spacing) + 20
        pygame.draw.rect(self.screen, (220, 220, 220), (start_x - 10, start_y - area_height - 10, self.screen_width - 40, area_height + 20))

        # Afficher chaque tuile de la défausse
        self.discard_tiles_rects = []  # Stocker les rectangles des tuiles
        for index, tile in enumerate(self.game.tile_bag.discard_pile):
            row = index // tiles_per_row
            col = index % tiles_per_row
            x = start_x + col * (tile_width + spacing)
            y = start_y - (row + 1) * (tile_height + spacing)
            rect = pygame.Rect(x, y, tile_width, tile_height)
            pygame.draw.rect(self.screen, (200, 200, 200), rect)  # Gris
            font = pygame.font.Font(None, 18)
            text = font.render(str(tile), True, (0, 0, 0))
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)
            self.discard_tiles_rects.append((rect, tile))  # Stocker le rectangle et la valeur de la tuile

        # Libellé
        font = pygame.font.Font(None, 24)
        label_text = font.render("Défausse", True, (0, 0, 0))
        self.screen.blit(label_text, (start_x, start_y - area_height - 30))

    def draw_message(self):
        if self.message:
            current_time = pygame.time.get_ticks()
            if current_time - self.message_timer < 3000:  # Afficher pendant 3 secondes
                font = pygame.font.Font(None, 24)
                text = font.render(self.message, True, (255, 0, 0))  # Rouge
                text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height - 30))
                self.screen.blit(text, text_rect)
            else:
                self.message = ""

    def handle_click(self, pos):
        x, y = pos
        # Vérifier si le clic est sur une tuile de la défausse
        if hasattr(self, 'discard_tiles_rects'):
            for rect, tile in self.discard_tiles_rects:
                if rect.collidepoint(pos):
                    self.controller.handle_draw_tile(from_discard=True, tile=tile)
                    return
        # Vérifier si le clic est sur le bouton de pioche
        if self.draw_button_rect and self.draw_button_rect.collidepoint(pos):
            self.controller.handle_draw_tile(from_discard=False)
            return
        # Vérifier si le clic est sur le bouton pour défausser la tuile actuelle
        if self.discard_current_tile_button_rect and self.discard_current_tile_button_rect.collidepoint(pos):
            self.controller.handle_discard_tile()
            return
        # Vérifier si le clic est sur la grille
        self.handle_grid_click(pos)

    def handle_grid_click(self, pos):
        x, y = pos
        col = (x - self.grid_origin_x) // self.cell_size
        row = (y - self.grid_origin_y) // self.cell_size

        if 0 <= row < 4 and 0 <= col < 4:
            self.controller.handle_place_tile(int(row), int(col))

    # Méthodes appelées par le contrôleur pour mettre à jour la vue
    def update_current_tile(self, tile):
        self.current_tile = tile
        self.draw()

    def clear_current_tile(self):
        self.current_tile = None
        self.draw()

    def update_board(self):
        self.draw()

    def display_message(self, message):
        self.message = message
        self.message_timer = pygame.time.get_ticks()
        self.draw()
