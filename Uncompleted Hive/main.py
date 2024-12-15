import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1500, 1000
TILE_RADIUS = 50  # Radius of each hex tile
BOARD_ROWS, BOARD_COLS = 25, 25  # Example grid size
BOARD_COLOR = (229, 227, 212)
TILE_COLOR = (0, 0, 0)
HIGHLIGHT_COLOR = (255, 200, 100)
FPS = 30

# Scrolling offsets
scroll_x, scroll_y = 0, 0  # Initial offsets
SCROLL_SPEED = 20

# Space for pieces on the right side
PIECE_DISPLAY_WIDTH = 300  # Width for the piece display area

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hive Game - Hexagonal Setup")
clock = pygame.time.Clock()

# Game board representation
board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

#classes
class Piece(pygame.sprite.Sprite):
    def __init__(self, color, num, pos, name):
        super().__init__()
        self.color = color
        self.name = name
        self.num = num
        self.pos = pos
        self.tile_pos = None
        self.image = None
        self.rect = None
        self.scale_factor = 1.0
        self.original_image = None
        self.draw_image()
    def draw_image(self):
        self.image = pygame.image.load(f"images/{self.color} {self.name}.png").convert_alpha()
        self.original_image = self.image
        self.rect = self.image.get_rect(center=(self.pos[0], self.pos[1]))
    def scale_image(self):
        if self.original_image is not None:
            width = int(self.original_image.get_width() * self.scale_factor)
            height = int(self.original_image.get_height() * self.scale_factor)
            self.image = pygame.transform.scale(self.original_image, (width, height))
            self.rect = self.original_image.get_rect(center=self.rect.center)
        else:
            print("Error: Image not loaded yet.")

    def reset_size(self):
        self.scale_factor = 1
        self.scale_image()

    def enlarge(self):
        self.scale_factor = 1.2
        self.scale_image()

    def place_on_tile(self, row, col):
        self.tile_pos = (row, col)

    def find_available_moves(self):
        pass

class Queen(Piece):
    def __init__(self, color, num, pos):
        super().__init__(color, num, pos, name="queen")
        self.draw_image()

    def find_available_moves(self):
        row, col = self.tile_pos
        neighbors = get_neighbors(row, col)
        return [(r, c) for r, c in neighbors if 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and not board[r][c]]

class Ant(Piece):
    def __init__(self, color, num, pos):
        super().__init__(color, num, pos, name="ant")
        self.draw_image()

    def find_available_moves(self):
        row, col = self.tile_pos
        neighbors = get_neighbors(row, col)
        return [(r, c) for r, c in neighbors if 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and not board[r][c]]

class Beetle(Piece):
    def __init__(self, color, num, pos):
        super().__init__(color, num, pos, name="beetle")
        self.draw_image()

    def find_available_moves(self):
        row, col = self.tile_pos
        neighbors = get_neighbors(row, col)
        return [(r, c) for r, c in neighbors if 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS]

class Grasshopper(Piece):
    def __init__(self, color, num, pos):
        super().__init__(color, num, pos, name="grasshopper")
        self.draw_image()

    def get_top_left_moves(self):
        valid_moves = []
        row, col = self.tile_pos
        original_row = row
        original_col = col

        while 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLS:
            # If the row is odd, top-left is (row-1, col)
            if row % 2 == 1:
                next_row, next_col = row - 1, col
            # If the row is even, top-left is (row-1, col-1)
            else:
                next_row, next_col = row - 1, col - 1

            # Check if the destination tile is empty
            if 0 <= next_row < BOARD_ROWS and 0 <= next_col < BOARD_COLS and board[next_row][next_col] is None:
                # Check the neighbors of the potential destination tile
                neighbors = get_neighbors(next_row, next_col)
                flag = False
                for r, c in neighbors:
                    if board[r][c] and (r != original_row or c != original_col):
                        # If there's a piece blocking the move, flag it
                        flag = True

                if flag:
                    valid_moves.append((next_row, next_col))  # Add valid move to list

                # Update current position to next position
                row, col = next_row, next_col

        return valid_moves

    def get_top_right_moves(self):
        valid_moves = []
        row, col = self.tile_pos
        original_row = row
        original_col = col

        while 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLS:
            # If the row is odd, top-left is (row-1, col)
            if row % 2 == 1:
                next_row, next_col = row - 1, col + 1
            # If the row is even, top-left is (row-1, col-1)
            else:
                next_row, next_col = row - 1, col

            # Check if the destination tile is empty
            if 0 <= next_row < BOARD_ROWS and 0 <= next_col < BOARD_COLS and board[next_row][next_col] is None:
                # Check the neighbors of the potential destination tile
                neighbors = get_neighbors(next_row, next_col)
                flag = False
                for r, c in neighbors:
                    if board[r][c] and (r != original_row or c != original_col):
                        # If there's a piece blocking the move, flag it
                        flag = True

                if flag:
                    valid_moves.append((next_row, next_col))  # Add valid move to list

                # Update current position to next position
                row, col = next_row, next_col

        return valid_moves

    def get_left_moves(self):
        valid_moves = []
        row, col = self.tile_pos
        original_row = row
        original_col = col

        while 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLS:
            next_row, next_col = row, col - 1

            # Check if the destination tile is empty
            if 0 <= next_row < BOARD_ROWS and 0 <= next_col < BOARD_COLS and board[next_row][next_col] is None:
                # Check the neighbors of the potential destination tile
                neighbors = get_neighbors(next_row, next_col)
                flag = False
                for r, c in neighbors:
                    if board[r][c] and (r != original_row or c != original_col):
                        # If there's a piece blocking the move, flag it
                        flag = True

                if flag:
                    valid_moves.append((next_row, next_col))  # Add valid move to list

                # Update current position to next position
                row, col = next_row, next_col

        return valid_moves

    def get_right_moves(self):
        valid_moves = []
        row, col = self.tile_pos
        original_row = row
        original_col = col

        while 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLS:
            next_row, next_col = row, col + 1

            # Check if the destination tile is empty
            if 0 <= next_row < BOARD_ROWS and 0 <= next_col < BOARD_COLS and board[next_row][next_col] is None:
                # Check the neighbors of the potential destination tile
                neighbors = get_neighbors(next_row, next_col)
                flag = False
                for r, c in neighbors:
                    if board[r][c] and (r != original_row or c != original_col):
                        # If there's a piece blocking the move, flag it
                        flag = True

                if flag:
                    valid_moves.append((next_row, next_col))  # Add valid move to list

                # Update current position to next position
                row, col = next_row, next_col

        return valid_moves

    def get_bottom_left_moves(self):
        valid_moves = []
        row, col = self.tile_pos
        original_row = row
        original_col = col

        while 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLS:
            # If the row is odd, top-left is (row-1, col)
            if row % 2 == 1:
                next_row, next_col = row + 1, col
            # If the row is even, top-left is (row-1, col-1)
            else:
                next_row, next_col = row + 1, col - 1

            # Check if the destination tile is empty
            if 0 <= next_row < BOARD_ROWS and 0 <= next_col < BOARD_COLS and board[next_row][next_col] is None:
                # Check the neighbors of the potential destination tile
                neighbors = get_neighbors(next_row, next_col)
                flag = False
                for r, c in neighbors:
                    if board[r][c] and (r != original_row or c != original_col):
                        # If there's a piece blocking the move, flag it
                        flag = True

                if flag:
                    valid_moves.append((next_row, next_col))  # Add valid move to list

                # Update current position to next position
                row, col = next_row, next_col

        return valid_moves

    def get_bottom_right_moves(self):
        valid_moves = []
        row, col = self.tile_pos
        original_row = row
        original_col = col

        while 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLS:
            # If the row is odd, top-left is (row-1, col)
            if row % 2 == 1:
                next_row, next_col = row + 1, col + 1
            # If the row is even, top-left is (row-1, col-1)
            else:
                next_row, next_col = row + 1, col

            # Check if the destination tile is empty
            if 0 <= next_row < BOARD_ROWS and 0 <= next_col < BOARD_COLS and board[next_row][next_col] is None:
                # Check the neighbors of the potential destination tile
                neighbors = get_neighbors(next_row, next_col)
                flag = False
                for r, c in neighbors:
                    if board[r][c] and (r != original_row or c != original_col):
                        # If there's a piece blocking the move, flag it
                        flag = True

                if flag:
                    valid_moves.append((next_row, next_col))  # Add valid move to list

                # Update current position to next position
                row, col = next_row, next_col

        return valid_moves

    def find_available_moves(self):
        # top_left_moves = self.get_top_left_moves()
        # top_right_moves = self.get_top_right_moves()
        # left_moves = self.get_left_moves()
        # right_moves = self.get_right_moves()
        # bottom_left_moves = self.get_bottom_left_moves()
        # bottom_right_moves = self.get_bottom_right_moves()
        #
        # all_moves = list(set(top_left_moves + top_right_moves + left_moves + right_moves + bottom_left_moves + bottom_right_moves))
        #
        # return all_moves

        row, col = self.tile_pos
        neighbors = get_neighbors(row, col)
        return [(r, c) for r, c in neighbors if 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and not board[r][c]]

class Spider(Piece):
    def __init__(self, color, num, pos):
        super().__init__(color, num, pos, name="spider")
        self.draw_image()

    def find_available_moves(self):
        row, col = self.tile_pos
        neighbors = get_neighbors(row, col)
        return [(r, c) for r, c in neighbors if 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and not board[r][c]]


# Helper functions
def draw_hexagon(surface, color, center, radius, width=0):
    """Draws a hexagon rotated so the bottom is a point."""
    points = []
    for i in range(6):
        # Add a 30-degree offset to rotate the hexagon
        angle = math.radians(60 * i + 30)
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        points.append((x, y))
    pygame.draw.polygon(surface, color, points, width)
def get_tile_position(col, row):
    # Horizontal offset for adjacent hexagons in the same row
    x_offset = col * (2 * TILE_RADIUS) + scroll_x

    # Vertical offset for adjacent rows
    y_offset = row * (math.sqrt(3) * TILE_RADIUS) + scroll_y

    # Stagger odd rows
    if row % 2 == 1:
        x_offset += 1 * TILE_RADIUS

    # Center the grid within the screen
    x = x_offset + (SCREEN_WIDTH - ((BOARD_COLS - 1) * 1.5 * TILE_RADIUS)) // 2
    y = y_offset + (SCREEN_HEIGHT - ((BOARD_ROWS - 1) * math.sqrt(3) * TILE_RADIUS)) // 2

    return x, y

def draw_board():
    """Draw the hexagonal game board."""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            x, y = get_tile_position(col, row)
            draw_hexagon(screen, TILE_COLOR, (x, y), TILE_RADIUS, 2)
def get_hex_from_mouse(pos):
    """Convert mouse position to board coordinates."""
    mouse_x, mouse_y = pos
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            x, y = get_tile_position(col, row)
            dist = math.sqrt((mouse_x - x) ** 2 + (mouse_y - y) ** 2)
            if dist <= TILE_RADIUS:
                return row, col
    return None
def handle_scrolling():
    global scroll_x, scroll_y
    keys = pygame.key.get_pressed()

    # Scroll with arrow keys
    if keys[pygame.K_UP]:
        scroll_y += SCROLL_SPEED
    if keys[pygame.K_DOWN]:
        scroll_y -= SCROLL_SPEED
    if keys[pygame.K_LEFT]:
        scroll_x += SCROLL_SPEED
    if keys[pygame.K_RIGHT]:
        scroll_x -= SCROLL_SPEED
def draw_pieces():
    for piece in all_pieces:
        if piece.tile_pos:
            row, col = piece.tile_pos
            x, y = get_tile_position(col, row)
            piece.rect.center = (x, y)
        screen.blit(piece.image, piece.rect)

def get_neighbors(row, col):
    if row%2 == 1:
        top_left = (row-1, col)
    else:
        top_left = (row - 1, col-1)

    top_right = (top_left[0], top_left[1]+1)
    left = (row, col-1)
    right = (row, col + 1)
    bottom_left = (top_left[0]+2, top_left[1])
    bottom_right = (top_right[0]+2, top_right[1])

    neighbors = [top_left, top_right, left, right, bottom_left, bottom_right]
    return [(r, c) for r, c in neighbors if 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS]

def is_valid_move(row, col, color):
    neighbors = get_neighbors(row, col)
    has_same_color_neighbor = any(
        board[r][c] and board[r][c].color == color for r, c in neighbors
    )
    touches_opponent = any(
        board[r][c] and board[r][c].color != color for r, c in neighbors
    )
    return has_same_color_neighbor and not touches_opponent


#Pieces
all_pieces = pygame.sprite.Group()

# Queens
white_queen = Queen("white", 1, [SCREEN_WIDTH - 250, 200])
black_queen = Queen("black", 1, [SCREEN_WIDTH - 250, 400])

# Ants
white_ant_1 = Ant("white", 1, [SCREEN_WIDTH - 250, 100])
white_ant_2 = Ant("white", 2, [SCREEN_WIDTH - 200, 100])
white_ant_3 = Ant("white", 3, [SCREEN_WIDTH - 150, 100])
black_ant_1 = Ant("black", 1, [SCREEN_WIDTH - 250, 300])
black_ant_2 = Ant("black", 2, [SCREEN_WIDTH - 200, 300])
black_ant_3 = Ant("black", 3, [SCREEN_WIDTH - 150, 300])

# Beetles
white_beetle_1 = Beetle("white", 1, [SCREEN_WIDTH - 100, 100])
white_beetle_2 = Beetle("white", 2, [SCREEN_WIDTH - 250, 150])
black_beetle_1 = Beetle("black", 1, [SCREEN_WIDTH - 100, 300])
black_beetle_2 = Beetle("black", 2, [SCREEN_WIDTH - 250, 350])

# Grasshoppers
white_grasshopper_1 = Grasshopper("white", 1, [SCREEN_WIDTH - 200, 150])
white_grasshopper_2 = Grasshopper("white", 2, [SCREEN_WIDTH - 150, 150])
white_grasshopper_3 = Grasshopper("white", 3, [SCREEN_WIDTH - 100, 150])
black_grasshopper_1 = Grasshopper("black", 1, [SCREEN_WIDTH - 200, 350])
black_grasshopper_2 = Grasshopper("black", 2, [SCREEN_WIDTH - 150, 350])
black_grasshopper_3 = Grasshopper("black", 3, [SCREEN_WIDTH - 100, 350])

# Spiders
white_spider_1 = Spider("white", 1, [SCREEN_WIDTH - 200, 200])
white_spider_2 = Spider("white", 2, [SCREEN_WIDTH - 150, 200])
black_spider_1 = Spider("black", 1, [SCREEN_WIDTH - 200, 400])
black_spider_2 = Spider("black", 2, [SCREEN_WIDTH - 150, 400])

# Add all pieces to the group
all_pieces.add(
    white_queen, black_queen,
    white_ant_1, white_ant_2, white_ant_3,
    black_ant_1, black_ant_2, black_ant_3,
    white_beetle_1, white_beetle_2,
    black_beetle_1, black_beetle_2,
    white_grasshopper_1, white_grasshopper_2, white_grasshopper_3,
    black_grasshopper_1, black_grasshopper_2, black_grasshopper_3,
    white_spider_1, white_spider_2,
    black_spider_1, black_spider_2
)


# Main game loop
selected_tile = None  # Tile currently selected
selected_piece = None
running = True
current_turn = "white"  # First turn is white
placed_pieces = []      # List of placed pieces
highlighted_tiles = []  # List of tiles to highlight

while running:
    screen.fill(BOARD_COLOR)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_pos = pygame.mouse.get_pos()
                for piece in all_pieces:
                    if piece.rect.collidepoint(mouse_pos):
                        if piece.color == current_turn and selected_piece is None:
                            selected_piece = piece
                        elif selected_piece:
                            selected_piece.reset_size()
                            selected_piece = None

                if selected_piece:
                    selected_piece.enlarge()
                    if selected_piece not in placed_pieces:
                        # Highlight valid moves
                        if not placed_pieces:  # First piece
                            highlighted_tiles = [(BOARD_ROWS // 2, BOARD_COLS // 2)]
                        elif len(placed_pieces) == 1:  # Second piece
                            first_piece = placed_pieces[0]
                            first_row, first_col = first_piece.tile_pos
                            highlighted_tiles = get_neighbors(first_row, first_col)
                        else:  # Subsequent pieces
                            highlighted_tiles = [
                                (r, c) for r in range(BOARD_ROWS) for c in range(BOARD_COLS)
                                if not board[r][c] and is_valid_move(r, c, current_turn)
                            ]
                    else:
                        highlighted_tiles = selected_piece.find_available_moves()
                else:
                    highlighted_tiles = []

                # Check if a highlighted tile is clicked
                clicked_tile = get_hex_from_mouse(mouse_pos)
                if clicked_tile and selected_piece and clicked_tile in highlighted_tiles:
                    if selected_piece in placed_pieces:
                        r, c = selected_piece.tile_pos
                        board[r][c] = None
                        placed_pieces.remove(selected_piece)


                    # Place the piece on the board
                    row, col = clicked_tile
                    board[row][col] = (selected_piece)
                    selected_piece.place_on_tile(row, col)
                    placed_pieces.append(selected_piece)

                    # Switch turn
                    current_turn = "black" if current_turn == "white" else "white"
                    selected_piece = None
                    highlighted_tiles = []

    # Draw the board and pieces
    handle_scrolling()
    draw_board()
    # Highlight available moves
    for row, col in highlighted_tiles:
        x, y = get_tile_position(col, row)
        draw_hexagon(screen, HIGHLIGHT_COLOR, (x, y), TILE_RADIUS, 4)

    # Display the piece area on the right side
    pygame.draw.rect(screen, (229, 227, 212), (SCREEN_WIDTH - PIECE_DISPLAY_WIDTH, 0, PIECE_DISPLAY_WIDTH, SCREEN_HEIGHT))
    draw_pieces()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1500, 1000
TILE_RADIUS = 50  # Radius of each hex tile
BOARD_ROWS, BOARD_COLS = 25, 25  # Example grid size
BOARD_COLOR = (229, 227, 212)
TILE_COLOR = (0, 0, 0)
HIGHLIGHT_COLOR = (255, 200, 100)
FPS = 30

# Scrolling offsets
scroll_x, scroll_y = 0, 0  # Initial offsets
SCROLL_SPEED = 20

# Space for pieces on the right side
PIECE_DISPLAY_WIDTH = 300  # Width for the piece display area

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hive Game - Hexagonal Setup")
clock = pygame.time.Clock()

# Game board representation
board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

#classes
class Piece(pygame.sprite.Sprite):
    def __init__(self, color, num, pos, name):
        super().__init__()
        self.color = color
        self.name = name
        self.num = num
        self.pos = pos
        self.tile_pos = None
        self.image = None
        self.rect = None
        self.scale_factor = 1.0
        self.original_image = None
        self.draw_image()
    def draw_image(self):
        self.image = pygame.image.load(f"images/{self.color} {self.name}.png").convert_alpha()
        self.original_image = self.image
        self.rect = self.image.get_rect(center=(self.pos[0], self.pos[1]))
    def scale_image(self):
        if self.original_image is not None:
            width = int(self.original_image.get_width() * self.scale_factor)
            height = int(self.original_image.get_height() * self.scale_factor)
            self.image = pygame.transform.scale(self.original_image, (width, height))
            self.rect = self.original_image.get_rect(center=self.rect.center)
        else:
            print("Error: Image not loaded yet.")

    def reset_size(self):
        self.scale_factor = 1
        self.scale_image()

    def enlarge(self):
        self.scale_factor = 1.2
        self.scale_image()

    def place_on_tile(self, row, col):
        self.tile_pos = (row, col)

    def find_available_moves(self):
        pass

class Queen(Piece):
    def __init__(self, color, num, pos):
        super().__init__(color, num, pos, name="queen")
        self.draw_image()

    def find_available_moves(self):
        row, col = self.tile_pos
        neighbors = get_neighbors(row, col)
        return [(r, c) for r, c in neighbors if 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and not board[r][c]]

class Ant(Piece):
    def __init__(self, color, num, pos):
        super().__init__(color, num, pos, name="ant")
        self.draw_image()

    def find_available_moves(self):
        row, col = self.tile_pos
        neighbors = get_neighbors(row, col)
        return [(r, c) for r, c in neighbors if 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and not board[r][c]]

class Beetle(Piece):
    def __init__(self, color, num, pos):
        super().__init__(color, num, pos, name="beetle")
        self.draw_image()

    def find_available_moves(self):
        row, col = self.tile_pos
        neighbors = get_neighbors(row, col)
        return [(r, c) for r, c in neighbors if 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS]

class Grasshopper(Piece):
    def __init__(self, color, num, pos):
        super().__init__(color, num, pos, name="grasshopper")
        self.draw_image()

    def get_top_left_moves(self):
        valid_moves = []
        row, col = self.tile_pos
        original_row = row
        original_col = col

        while 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLS:
            # If the row is odd, top-left is (row-1, col)
            if row % 2 == 1:
                next_row, next_col = row - 1, col
            # If the row is even, top-left is (row-1, col-1)
            else:
                next_row, next_col = row - 1, col - 1

            # Check if the destination tile is empty
            if 0 <= next_row < BOARD_ROWS and 0 <= next_col < BOARD_COLS and board[next_row][next_col] is None:
                # Check the neighbors of the potential destination tile
                neighbors = get_neighbors(next_row, next_col)
                flag = False
                for r, c in neighbors:
                    if board[r][c] and (r != original_row or c != original_col):
                        # If there's a piece blocking the move, flag it
                        flag = True

                if flag:
                    valid_moves.append((next_row, next_col))  # Add valid move to list

                # Update current position to next position
                row, col = next_row, next_col

        return valid_moves

    def get_top_right_moves(self):
        valid_moves = []
        row, col = self.tile_pos
        original_row = row
        original_col = col

        while 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLS:
            # If the row is odd, top-left is (row-1, col)
            if row % 2 == 1:
                next_row, next_col = row - 1, col + 1
            # If the row is even, top-left is (row-1, col-1)
            else:
                next_row, next_col = row - 1, col

            # Check if the destination tile is empty
            if 0 <= next_row < BOARD_ROWS and 0 <= next_col < BOARD_COLS and board[next_row][next_col] is None:
                # Check the neighbors of the potential destination tile
                neighbors = get_neighbors(next_row, next_col)
                flag = False
                for r, c in neighbors:
                    if board[r][c] and (r != original_row or c != original_col):
                        # If there's a piece blocking the move, flag it
                        flag = True

                if flag:
                    valid_moves.append((next_row, next_col))  # Add valid move to list

                # Update current position to next position
                row, col = next_row, next_col

        return valid_moves

    def get_left_moves(self):
        valid_moves = []
        row, col = self.tile_pos
        original_row = row
        original_col = col

        while 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLS:
            next_row, next_col = row, col - 1

            # Check if the destination tile is empty
            if 0 <= next_row < BOARD_ROWS and 0 <= next_col < BOARD_COLS and board[next_row][next_col] is None:
                # Check the neighbors of the potential destination tile
                neighbors = get_neighbors(next_row, next_col)
                flag = False
                for r, c in neighbors:
                    if board[r][c] and (r != original_row or c != original_col):
                        # If there's a piece blocking the move, flag it
                        flag = True

                if flag:
                    valid_moves.append((next_row, next_col))  # Add valid move to list

                # Update current position to next position
                row, col = next_row, next_col

        return valid_moves

    def get_right_moves(self):
        valid_moves = []
        row, col = self.tile_pos
        original_row = row
        original_col = col

        while 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLS:
            next_row, next_col = row, col + 1

            # Check if the destination tile is empty
            if 0 <= next_row < BOARD_ROWS and 0 <= next_col < BOARD_COLS and board[next_row][next_col] is None:
                # Check the neighbors of the potential destination tile
                neighbors = get_neighbors(next_row, next_col)
                flag = False
                for r, c in neighbors:
                    if board[r][c] and (r != original_row or c != original_col):
                        # If there's a piece blocking the move, flag it
                        flag = True

                if flag:
                    valid_moves.append((next_row, next_col))  # Add valid move to list

                # Update current position to next position
                row, col = next_row, next_col

        return valid_moves

    def get_bottom_left_moves(self):
        valid_moves = []
        row, col = self.tile_pos
        original_row = row
        original_col = col

        while 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLS:
            # If the row is odd, top-left is (row-1, col)
            if row % 2 == 1:
                next_row, next_col = row + 1, col
            # If the row is even, top-left is (row-1, col-1)
            else:
                next_row, next_col = row + 1, col - 1

            # Check if the destination tile is empty
            if 0 <= next_row < BOARD_ROWS and 0 <= next_col < BOARD_COLS and board[next_row][next_col] is None:
                # Check the neighbors of the potential destination tile
                neighbors = get_neighbors(next_row, next_col)
                flag = False
                for r, c in neighbors:
                    if board[r][c] and (r != original_row or c != original_col):
                        # If there's a piece blocking the move, flag it
                        flag = True

                if flag:
                    valid_moves.append((next_row, next_col))  # Add valid move to list

                # Update current position to next position
                row, col = next_row, next_col

        return valid_moves

    def get_bottom_right_moves(self):
        valid_moves = []
        row, col = self.tile_pos
        original_row = row
        original_col = col

        while 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLS:
            # If the row is odd, top-left is (row-1, col)
            if row % 2 == 1:
                next_row, next_col = row + 1, col + 1
            # If the row is even, top-left is (row-1, col-1)
            else:
                next_row, next_col = row + 1, col

            # Check if the destination tile is empty
            if 0 <= next_row < BOARD_ROWS and 0 <= next_col < BOARD_COLS and board[next_row][next_col] is None:
                # Check the neighbors of the potential destination tile
                neighbors = get_neighbors(next_row, next_col)
                flag = False
                for r, c in neighbors:
                    if board[r][c] and (r != original_row or c != original_col):
                        # If there's a piece blocking the move, flag it
                        flag = True

                if flag:
                    valid_moves.append((next_row, next_col))  # Add valid move to list

                # Update current position to next position
                row, col = next_row, next_col

        return valid_moves

    def find_available_moves(self):
        # top_left_moves = self.get_top_left_moves()
        # top_right_moves = self.get_top_right_moves()
        # left_moves = self.get_left_moves()
        # right_moves = self.get_right_moves()
        # bottom_left_moves = self.get_bottom_left_moves()
        # bottom_right_moves = self.get_bottom_right_moves()
        #
        # all_moves = list(set(top_left_moves + top_right_moves + left_moves + right_moves + bottom_left_moves + bottom_right_moves))
        #
        # return all_moves

        row, col = self.tile_pos
        neighbors = get_neighbors(row, col)
        return [(r, c) for r, c in neighbors if 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and not board[r][c]]

class Spider(Piece):
    def __init__(self, color, num, pos):
        super().__init__(color, num, pos, name="spider")
        self.draw_image()

    def find_available_moves(self):
        row, col = self.tile_pos
        neighbors = get_neighbors(row, col)
        return [(r, c) for r, c in neighbors if 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and not board[r][c]]


# Helper functions
def draw_hexagon(surface, color, center, radius, width=0):
    """Draws a hexagon rotated so the bottom is a point."""
    points = []
    for i in range(6):
        # Add a 30-degree offset to rotate the hexagon
        angle = math.radians(60 * i + 30)
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        points.append((x, y))
    pygame.draw.polygon(surface, color, points, width)
def get_tile_position(col, row):
    # Horizontal offset for adjacent hexagons in the same row
    x_offset = col * (2 * TILE_RADIUS) + scroll_x

    # Vertical offset for adjacent rows
    y_offset = row * (math.sqrt(3) * TILE_RADIUS) + scroll_y

    # Stagger odd rows
    if row % 2 == 1:
        x_offset += 1 * TILE_RADIUS

    # Center the grid within the screen
    x = x_offset + (SCREEN_WIDTH - ((BOARD_COLS - 1) * 1.5 * TILE_RADIUS)) // 2
    y = y_offset + (SCREEN_HEIGHT - ((BOARD_ROWS - 1) * math.sqrt(3) * TILE_RADIUS)) // 2

    return x, y

def draw_board():
    """Draw the hexagonal game board."""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            x, y = get_tile_position(col, row)
            draw_hexagon(screen, TILE_COLOR, (x, y), TILE_RADIUS, 2)
def get_hex_from_mouse(pos):
    """Convert mouse position to board coordinates."""
    mouse_x, mouse_y = pos
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            x, y = get_tile_position(col, row)
            dist = math.sqrt((mouse_x - x) ** 2 + (mouse_y - y) ** 2)
            if dist <= TILE_RADIUS:
                return row, col
    return None
def handle_scrolling():
    global scroll_x, scroll_y
    keys = pygame.key.get_pressed()

    # Scroll with arrow keys
    if keys[pygame.K_UP]:
        scroll_y += SCROLL_SPEED
    if keys[pygame.K_DOWN]:
        scroll_y -= SCROLL_SPEED
    if keys[pygame.K_LEFT]:
        scroll_x += SCROLL_SPEED
    if keys[pygame.K_RIGHT]:
        scroll_x -= SCROLL_SPEED
def draw_pieces():
    for piece in all_pieces:
        if piece.tile_pos:
            row, col = piece.tile_pos
            x, y = get_tile_position(col, row)
            piece.rect.center = (x, y)
        screen.blit(piece.image, piece.rect)

def get_neighbors(row, col):
    if row%2 == 1:
        top_left = (row-1, col)
    else:
        top_left = (row - 1, col-1)

    top_right = (top_left[0], top_left[1]+1)
    left = (row, col-1)
    right = (row, col + 1)
    bottom_left = (top_left[0]+2, top_left[1])
    bottom_right = (top_right[0]+2, top_right[1])

    neighbors = [top_left, top_right, left, right, bottom_left, bottom_right]
    return [(r, c) for r, c in neighbors if 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS]

def is_valid_move(row, col, color):
    neighbors = get_neighbors(row, col)
    has_same_color_neighbor = any(
        board[r][c] and board[r][c].color == color for r, c in neighbors
    )
    touches_opponent = any(
        board[r][c] and board[r][c].color != color for r, c in neighbors
    )
    return has_same_color_neighbor and not touches_opponent


#Pieces
all_pieces = pygame.sprite.Group()

# Queens
white_queen = Queen("white", 1, [SCREEN_WIDTH - 250, 200])
black_queen = Queen("black", 1, [SCREEN_WIDTH - 250, 400])

# Ants
white_ant_1 = Ant("white", 1, [SCREEN_WIDTH - 250, 100])
white_ant_2 = Ant("white", 2, [SCREEN_WIDTH - 200, 100])
white_ant_3 = Ant("white", 3, [SCREEN_WIDTH - 150, 100])
black_ant_1 = Ant("black", 1, [SCREEN_WIDTH - 250, 300])
black_ant_2 = Ant("black", 2, [SCREEN_WIDTH - 200, 300])
black_ant_3 = Ant("black", 3, [SCREEN_WIDTH - 150, 300])

# Beetles
white_beetle_1 = Beetle("white", 1, [SCREEN_WIDTH - 100, 100])
white_beetle_2 = Beetle("white", 2, [SCREEN_WIDTH - 250, 150])
black_beetle_1 = Beetle("black", 1, [SCREEN_WIDTH - 100, 300])
black_beetle_2 = Beetle("black", 2, [SCREEN_WIDTH - 250, 350])

# Grasshoppers
white_grasshopper_1 = Grasshopper("white", 1, [SCREEN_WIDTH - 200, 150])
white_grasshopper_2 = Grasshopper("white", 2, [SCREEN_WIDTH - 150, 150])
white_grasshopper_3 = Grasshopper("white", 3, [SCREEN_WIDTH - 100, 150])
black_grasshopper_1 = Grasshopper("black", 1, [SCREEN_WIDTH - 200, 350])
black_grasshopper_2 = Grasshopper("black", 2, [SCREEN_WIDTH - 150, 350])
black_grasshopper_3 = Grasshopper("black", 3, [SCREEN_WIDTH - 100, 350])

# Spiders
white_spider_1 = Spider("white", 1, [SCREEN_WIDTH - 200, 200])
white_spider_2 = Spider("white", 2, [SCREEN_WIDTH - 150, 200])
black_spider_1 = Spider("black", 1, [SCREEN_WIDTH - 200, 400])
black_spider_2 = Spider("black", 2, [SCREEN_WIDTH - 150, 400])

# Add all pieces to the group
all_pieces.add(
    white_queen, black_queen,
    white_ant_1, white_ant_2, white_ant_3,
    black_ant_1, black_ant_2, black_ant_3,
    white_beetle_1, white_beetle_2,
    black_beetle_1, black_beetle_2,
    white_grasshopper_1, white_grasshopper_2, white_grasshopper_3,
    black_grasshopper_1, black_grasshopper_2, black_grasshopper_3,
    white_spider_1, white_spider_2,
    black_spider_1, black_spider_2
)


# Main game loop
selected_tile = None  # Tile currently selected
selected_piece = None
running = True
current_turn = "white"  # First turn is white
placed_pieces = []      # List of placed pieces
highlighted_tiles = []  # List of tiles to highlight

while running:
    screen.fill(BOARD_COLOR)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_pos = pygame.mouse.get_pos()
                for piece in all_pieces:
                    if piece.rect.collidepoint(mouse_pos):
                        if piece.color == current_turn and selected_piece is None:
                            selected_piece = piece
                        elif selected_piece:
                            selected_piece.reset_size()
                            selected_piece = None

                if selected_piece:
                    selected_piece.enlarge()
                    if selected_piece not in placed_pieces:
                        # Highlight valid moves
                        if not placed_pieces:  # First piece
                            highlighted_tiles = [(BOARD_ROWS // 2, BOARD_COLS // 2)]
                        elif len(placed_pieces) == 1:  # Second piece
                            first_piece = placed_pieces[0]
                            first_row, first_col = first_piece.tile_pos
                            highlighted_tiles = get_neighbors(first_row, first_col)
                        else:  # Subsequent pieces
                            highlighted_tiles = [
                                (r, c) for r in range(BOARD_ROWS) for c in range(BOARD_COLS)
                                if not board[r][c] and is_valid_move(r, c, current_turn)
                            ]
                    else:
                        highlighted_tiles = selected_piece.find_available_moves()
                else:
                    highlighted_tiles = []

                # Check if a highlighted tile is clicked
                clicked_tile = get_hex_from_mouse(mouse_pos)
                if clicked_tile and selected_piece and clicked_tile in highlighted_tiles:
                    if selected_piece in placed_pieces:
                        r, c = selected_piece.tile_pos
                        board[r][c] = None
                        placed_pieces.remove(selected_piece)


                    # Place the piece on the board
                    row, col = clicked_tile
                    board[row][col] = (selected_piece)
                    selected_piece.place_on_tile(row, col)
                    placed_pieces.append(selected_piece)

                    # Switch turn
                    current_turn = "black" if current_turn == "white" else "white"
                    selected_piece = None
                    highlighted_tiles = []

    # Draw the board and pieces
    handle_scrolling()
    draw_board()
    # Highlight available moves
    for row, col in highlighted_tiles:
        x, y = get_tile_position(col, row)
        draw_hexagon(screen, HIGHLIGHT_COLOR, (x, y), TILE_RADIUS, 4)

    # Display the piece area on the right side
    pygame.draw.rect(screen, (229, 227, 212), (SCREEN_WIDTH - PIECE_DISPLAY_WIDTH, 0, PIECE_DISPLAY_WIDTH, SCREEN_HEIGHT))
    draw_pieces()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
