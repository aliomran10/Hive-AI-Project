import pygame as pg
from settings import WHITE_PIECE, BLACK_PIECE, WHITE, BLACK, PANEL, WIDTH, HEIGHT
from pieces import Queen, Grasshopper, Spider, Beetle, Ant
from tile import Inventory_Tile


class Inventory_Frame:

    def __init__(self, pos, player, white=True,):
        left = pos[0]
        top = HEIGHT - pos[1]

        inventory_width = WIDTH / 2
        inventory_height = 160

        inner_left = left + 5
        inner_top = top + 5
        inner_width = inventory_width - 10
        inner_height = inventory_height - 10

        self.back_panel = pg.Rect(left, top, inventory_width, inventory_height)
        self.inner_panel = pg.Rect(inner_left, inner_top, inner_width, inner_height)

        title_height = inner_height / 10
        stock_height = inner_height * (9 / 10)
        stock_width = inner_width / 5

        self.tile_rects = []
        self.tiles = []

        if white:
            self.color = WHITE_PIECE
        else:
            self.color = BLACK_PIECE
        for i in range(0, 5):
            self.tile_rects.append(pg.Rect(inner_left + i * stock_width + 2, inner_top + title_height + 2, stock_width - 4, stock_height - 4))

            if i == 0:
                tile_pos = (inner_left + i * stock_width + stock_width / 2, inner_top + title_height + stock_height / 2)
                self.tiles.append(Inventory_Tile(tile_pos, (99, 99),20, self.color, piece=Queen(self.color)))
            if i == 1:
                for j in range(1, 3):
                    tile_pos = (inner_left + i * stock_width + stock_width / 2, inner_top + title_height + j * stock_height / 3)
                    self.tiles.append(Inventory_Tile(tile_pos, (99, 99), 20, self.color, piece=Beetle(self.color)))
            if i == 2:
                for j in range(1, 3):
                    tile_pos = (inner_left + i * stock_width + stock_width / 2, inner_top + title_height + j * stock_height / 3)
                    self.tiles.append(Inventory_Tile(tile_pos, (99, 99), 20, self.color, piece=Spider(self.color)))
            if i == 3:
                for j in [25, 67, 109]:
                    tile_pos = (inner_left + i * stock_width + stock_width / 2, inner_top + title_height + j * stock_height / 135)
                    self.tiles.append(Inventory_Tile(tile_pos, (99, 99), 20, self.color, piece=Grasshopper(self.color)))
            if i == 4:
                for j in [25, 67, 109]:
                    tile_pos = (inner_left + i * stock_width + stock_width / 2, inner_top + title_height + j * stock_height / 135)
                    self.tiles.append(Inventory_Tile(tile_pos, (99, 99), 20, self.color, piece=Ant(self.color)))

        for tile in self.tiles:
            for piece in tile.pieces:
                piece.update_pos(tile.coords)

        FONT = pg.font.SysFont('Times New Norman', 24)
        if player == 0:
            self.font = FONT.render('Player 1 Inventory', True, WHITE)
        else:
            self.font = FONT.render('Player 2 Inventory', True, WHITE)
        self.title_rect = self.font.get_rect(center=(inner_left + inner_width / 2, inner_top + title_height / 2))

    def draw(self, background, pos):

        pg.draw.rect(background, BLACK, self.back_panel)
        pg.draw.rect(background, PANEL, self.inner_panel)
        pg.draw.rect(background, PANEL, self.title_rect)
        for i in range(0, len(self.tile_rects)):
            pg.draw.rect(background, self.color, self.tile_rects[i])

        background.blit(self.font, self.title_rect)
        pg.display.flip()

    def copy(self):
        # Create a new Inventory_Frame with the same positional arguments
        new_frame = Inventory_Frame(pos=(self.back_panel.left, HEIGHT - self.back_panel.top),
                                    player=0 if self.color == WHITE_PIECE else 1,
                                    white=(self.color == WHITE_PIECE))

        # Copy tile_rects
        new_frame.tile_rects = [pg.Rect(r.left, r.top, r.width, r.height) for r in self.tile_rects]

        # Copy tiles
        new_frame.tiles = [tile.copy() for tile in self.tiles]

        # Update piece positions
        for new_tile, old_tile in zip(new_frame.tiles, self.tiles):
            for new_piece, old_piece in zip(new_tile.pieces, old_tile.pieces):
                new_piece.update_pos(new_tile.coords)

        # Copy font and title_rect
        new_frame.font = self.font.copy()
        new_frame.title_rect = self.title_rect.copy()

        return new_frame