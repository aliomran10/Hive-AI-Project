import pygame as pg
from settings import WHITE_PIECE
from move_checker import axial_distance, move_is_not_blocked_or_jump, path_exists, is_straight_line



class Piece:

    def __init__(self, color=WHITE_PIECE):
        self.old_pos = None
        self.color = color

    def update_pos(self, pos):
        self.old_pos = pos

    def move_is_valid(self, state, old_tile, new_tile):
        pass

    def copy(self):
        copied_piece = type(self)(color=self.color)  # Create a new instance of the same type
        copied_piece.old_pos = self.old_pos  # Copy old_pos
        return copied_piece

class Queen(Piece):

    def __init__(self, color=WHITE_PIECE):
        super().__init__(color)

    def draw(self, surface, hex_pos):
        image = pg.image.load('images/{}.png'.format(type(self).__name__))
        (x, y) = hex_pos
        pos = (x - 16, y - 14)
        surface.blit(image, pos)

    def move_is_valid(self, state, old_tile, new_tile):
        dist = axial_distance(old_tile.axial_coords,new_tile.axial_coords)
        if dist == 1 and move_is_not_blocked_or_jump(state, old_tile,new_tile):
            return True
        else:
            return False

    def copy(self):
        return super().copy()

class Ant(Piece):

    def __init__(self, color=WHITE_PIECE):
        super().__init__(color)

    def draw(self, surface, hex_pos):
        image = pg.image.load('images/{}.png'.format(type(self).__name__))
        (x, y) = hex_pos
        pos = (x - 16, y - 17)
        surface.blit(image, pos)

    def move_is_valid(self, state, old_tile, new_tile):
        if path_exists(state, old_tile, new_tile):
            return True
        else:
            return False

    def copy(self):
        return super().copy()

class Spider(Piece):

    def __init__(self, color=WHITE_PIECE):
        super().__init__(color)

    def draw(self, surface, hex_pos):
        image = pg.image.load('images/{}.png'.format(type(self).__name__))
        (x, y) = hex_pos
        pos = (x - 16, y - 17)
        surface.blit(image, pos)

    def move_is_valid(self, state, old_tile, new_tile):
        if path_exists(state, old_tile, new_tile, spider=True) and move_is_not_blocked_or_jump(state, old_tile, new_tile):
            return True
        else:
            return False

    def copy(self):
        return super().copy()

class Beetle(Piece):

    def __init__(self, color=WHITE_PIECE):
        super().__init__(color)

    def draw(self, surface, hex_pos):
        image = pg.image.load('images/{}.png'.format(type(self).__name__))
        (x, y) = hex_pos
        pos = (x - 16, y - 16)
        surface.blit(image, pos)

    def move_is_valid(self, state, old_tile, new_tile):
        dist = axial_distance(old_tile.axial_coords,new_tile.axial_coords)
        if dist == 1 and (move_is_not_blocked_or_jump(state, old_tile, new_tile) or new_tile.has_pieces() or len(old_tile.pieces) > 1):
            return True
        else:
            return False

    def copy(self):
        return super().copy()
class Grasshopper(Piece):

    def __init__(self, color=WHITE_PIECE):
        super().__init__(color)

    def draw(self, surface, hex_pos):
        image = pg.image.load('images/{}.png'.format(type(self).__name__))
        (x, y) = hex_pos
        pos = (x - 12, y - 14)
        surface.blit(image, pos)

    def move_is_valid(self, state, old_tile, new_tile):
        dist = axial_distance(old_tile.axial_coords,new_tile.axial_coords)

        if dist > 1:
            visited = [old_tile]
            queue = [old_tile]
            while queue and new_tile not in visited:
                current_tile = queue.pop(0)
                for neighbor_tile in [x for x in
                        current_tile.adjacent_tiles if x.has_pieces()
                        and is_straight_line(old_tile.axial_coords,
                        x.axial_coords)]:
                    if neighbor_tile not in visited:
                        visited.append(neighbor_tile)
                        queue.append(neighbor_tile)

            for penultimate_tile in [x for x in new_tile.adjacent_tiles
                    if x.has_pieces()]:
                if penultimate_tile in visited and is_straight_line(old_tile.axial_coords,new_tile.axial_coords):
                    return True
        else:
            return False

    def copy(self):
        return super().copy()