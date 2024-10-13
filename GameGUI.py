
import pygame
from GameController import GameController

# class GameGUI:
#     def __init__(self, game):
#         self.game = game  # Le modèle
#         self.controller = GameController(game, self)  # Le contrôleur
#         pygame.init()
#         # Initialiser la fenêtre avec une taille fixe de 800x600 pixels
#         self.screen_width = 800
#         self.screen_height = 600
#         self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
#         pygame.display.set_caption("Lucky Numbers")
#         self.clock = pygame.time.Clock()
#         # Définir la taille fixe des cellules
#         self.cell_size = 80  # pixels
#         # Calculer l'origine de la grille pour la centrer horizontalement
#         grid_total_width = self.cell_size * 4
#         self.grid_origin_x = (self.screen_width - grid_total_width) // 2
#         self.grid_origin_y = 50  # Marge supérieure
#         # Informations sur la tuile actuelle
#         self.current_tile = None
#         # Gestion des messages
#         self.message = ""
#         self.message_timer = 0
#         # Rectangles des boutons
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
#             # Dessiner l'interface
#             self.draw()
#             pygame.display.flip()
#             # Vérifier si le jeu est terminé
#             if self.controller.is_game_over():
#                 pygame.time.wait(5000)  # Attendre 5 secondes avant de fermer
#                 running = False
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
#         if self.controller.state == "waiting_for_move" and self.controller.current_tile is not None:
#             self.draw_discard_current_tile_button()
#
#         # Afficher les messages
#         self.draw_message()
#
#     def draw_board(self):
#         board = self.game.players[0].board.grid
#         for row in range(4):
#             for col in range(4):
#                 rect = pygame.Rect(
#                     self.grid_origin_x + col * self.cell_size,
#                     self.grid_origin_y + row * self.cell_size,
#                     self.cell_size,
#                     self.cell_size
#                 )
#                 pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)  # Contour noir
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
#         """
#         Dessine la tuile actuelle sur l'écran
#         :return:
#         """
#         if self.controller.current_tile is not None:
#             rect = pygame.Rect(self.screen_width - 200, 200, 80, 80)
#             pygame.draw.rect(self.screen, (200, 200, 0), rect)  # Jaune
#             font = pygame.font.Font(None, 36)
#             text = font.render(str(self.controller.current_tile), True, (0, 0, 0))
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
#         pygame.draw.rect(self.screen, (0, 200, 0), button_rect)  # Vert
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
#         pygame.draw.rect(self.screen, (200, 0, 0), button_rect)  # Rouge
#         font = pygame.font.Font(None, 20)
#         text = font.render("Défausser Tuile", True, (255, 255, 255))
#         text_rect = text.get_rect(center=button_rect.center)
#         self.screen.blit(text, text_rect)
#         self.discard_current_tile_button_rect = button_rect
#
#     def draw_discard_pile(self):
#         # Afficher la pile de défausse
#         start_x = 20  # Marge gauche
#         start_y = self.screen_height - 100  # 100 pixels au-dessus du bas
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
#         self.discard_tiles_rects = []  # Stocker les rectangles des tuiles
#         for index, tile in enumerate(self.game.tile_bag.discard_pile):
#             row = index // tiles_per_row
#             col = index % tiles_per_row
#             x = start_x + col * (tile_width + spacing)
#             y = start_y - (row + 1) * (tile_height + spacing)
#             rect = pygame.Rect(x, y, tile_width, tile_height)
#             pygame.draw.rect(self.screen, (200, 200, 200), rect)  # Gris
#             font = pygame.font.Font(None, 18)
#             text = font.render(str(tile), True, (0, 0, 0))
#             text_rect = text.get_rect(center=rect.center)
#             self.screen.blit(text, text_rect)
#             self.discard_tiles_rects.append((rect, tile))  # Stocker le rectangle et la valeur de la tuile
#
#         # Libellé
#         font = pygame.font.Font(None, 24)
#         label_text = font.render("Défausse", True, (0, 0, 0))
#         self.screen.blit(label_text, (start_x, start_y - area_height - 30))
#
#     def draw_message(self):
#         if self.message:
#             current_time = pygame.time.get_ticks()
#             if current_time - self.message_timer < 3000:  # Afficher pendant 3 secondes
#                 font = pygame.font.Font(None, 24)
#                 text = font.render(self.message, True, (255, 0, 0))  # Rouge
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
#                     self.controller.handle_draw_tile(from_discard=True, tile=tile)
#                     return
#         # Vérifier si le clic est sur le bouton de pioche
#         if self.draw_button_rect and self.draw_button_rect.collidepoint(pos):
#             self.controller.handle_draw_tile(from_discard=False)
#             return
#         # Vérifier si le clic est sur le bouton pour défausser la tuile actuelle
#         if self.discard_current_tile_button_rect and self.discard_current_tile_button_rect.collidepoint(pos):
#             self.controller.handle_discard_tile()
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
#             self.controller.handle_place_tile(int(row), int(col))
#
#     # Méthodes appelées par le contrôleur pour mettre à jour la vue
#     def update_current_tile(self, tile):
#         self.current_tile = tile
#         self.draw()
#
#     def clear_current_tile(self):
#         self.current_tile = None
#         self.draw()
#
#     def update_board(self):
#         self.draw()
#
#     def display_message(self, message):
#         self.message = message
#         self.message_timer = pygame.time.get_ticks()
#         self.draw()



class GameGUI:
    def __init__(self, game):
        self.game = game  # Le modèle
        self.controller = GameController(game, self)  # Le contrôleur
        pygame.init()
        # Augmenter la largeur de la fenêtre pour accueillir les deux plateaux
        self.screen_width = 1200  # Anciennement 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Lucky Numbers")
        self.clock = pygame.time.Clock()
        # Définir la taille fixe des cellules
        self.cell_size = 60  # Réduire la taille des cellules pour tout faire tenir
        # Calculer la largeur totale de la grille
        grid_total_width = self.cell_size * 4
        # Calculer les origines des grilles pour les centrer horizontalement
        self.grid_origin_x = (self.screen_width // 4) - (grid_total_width // 2)
        self.grid_origin_y = 50  # Marge supérieure
        self.opponent_grid_origin_x = (3 * self.screen_width // 4) - (grid_total_width // 2)
        self.opponent_grid_origin_y = 50  # Marge supérieure
        # Point d'origine pour les éléments UI
        self.ui_origin_x = self.screen_width // 2
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
        # Dessiner votre plateau
        self.draw_player_board(0, self.grid_origin_x, self.grid_origin_y, show_tiles=True)
        # Dessiner le plateau de l'adversaire
        self.draw_player_board(1, self.opponent_grid_origin_x, self.opponent_grid_origin_y, show_tiles=True)
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

    def draw_player_board(self, player_index, origin_x, origin_y, show_tiles=True):
        board = self.game.players[player_index].board.grid
        # Dessiner le nom du joueur
        font = pygame.font.Font(None, 24)
        player_name = self.game.players[player_index].name
        text = font.render(player_name, True, (0, 0, 0))
        text_rect = text.get_rect(center=(origin_x + 2 * self.cell_size, origin_y - 20))
        self.screen.blit(text, text_rect)
        # Dessiner la grille
        for row in range(4):
            for col in range(4):
                rect = pygame.Rect(
                    origin_x + col * self.cell_size,
                    origin_y + row * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)  # Contour noir

                tile_value = board[row][col]
                if tile_value != 0:
                    if show_tiles:
                        # Afficher la tuile
                        font = pygame.font.Font(None, 36)
                        text = font.render(str(tile_value), True, (0, 0, 0))
                        text_rect = text.get_rect(center=rect.center)
                        self.screen.blit(text, text_rect)
                    else:
                        # Afficher une tuile cachée (par exemple, un rectangle gris)
                        pygame.draw.rect(self.screen, (150, 150, 150), rect)  # Rectangle gris

    def draw_current_tile(self):
        if self.controller.current_tile is not None:
            rect = pygame.Rect(self.ui_origin_x - 40, 200, 80, 80)
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
        x = self.ui_origin_x - button_width // 2  # Centré horizontalement
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
        x = self.ui_origin_x - button_width // 2  # Centré horizontalement
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
        # Vérifier si le clic est sur votre grille
        if self.is_click_on_player_board(pos):
            self.handle_grid_click(pos)

    def is_click_on_player_board(self, pos):
        x, y = pos
        board_rect = pygame.Rect(
            self.grid_origin_x,
            self.grid_origin_y,
            self.cell_size * 4,
            self.cell_size * 4
        )
        return board_rect.collidepoint(pos)

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
