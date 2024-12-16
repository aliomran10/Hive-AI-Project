import pygame as pg
from tile import initialize_grid, draw_drag
from move_checker import is_valid_move, game_is_over, player_has_no_moves, is_queen_played
from menus import start_menu, end_menu, no_move_popup
from game_state import Game_State
from inventory_frame import Inventory_Frame
from settings import BACKGROUND, WIDTH, HEIGHT, BLACK_PIECE
from AI import minimax

def game_loop():
    pg.font.init()

    display = pg.display.set_mode((WIDTH, HEIGHT))
    backdrop = pg.Surface(display.get_size())

    pg.display.set_caption('Hive')
    icon_image = pg.image.load('images/icon.png')
    pg.display.set_icon(icon_image)

    game_state = Game_State(initialize_grid(HEIGHT - 200, WIDTH, radius=20))
    white_frame = Inventory_Frame((0, 158), 0, white=True)
    black_frame = Inventory_Frame((440, 158), 1, white=False)

    # AI Settings
    ai_piece_color = BLACK_PIECE
    AI_DIFFICULTY = 2

    while game_state.running:
        while game_state.menu_loop:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    game_state.quit()
                    break
                start_menu(display, game_state, event)

        while game_state.move_popup_loop:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    game_state.quit()
                    break
                no_move_popup(display, backdrop, game_state, event)

        while game_state.main_loop:
            mouse_pos = pg.mouse.get_pos()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    game_state.quit()
                    break
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        game_state.quit()
                        break
                if event.type == pg.MOUSEBUTTONDOWN:
                    game_state.click()
                if event.type == pg.MOUSEBUTTONUP:
                    game_state.unclick()
                    if game_state.moving_piece and game_state.is_player_turn():
                        origin_tile = next(tile for tile in game_state.board_tiles if tile.has_pieces() and tile.pieces[-1] == game_state.moving_piece)
                        destination_tile = next((tile for tile in game_state.board_tiles if tile.under_mouse(mouse_pos)), None)
                        if is_valid_move(game_state, origin_tile, destination_tile):
                            origin_tile.move_piece(destination_tile)
                            game_state.next_turn()
                            if game_state.turn == 7 or game_state.turn == 8:
                                if not is_queen_played(game_state):
                                    game_state.open_popup()
                                elif player_has_no_moves(game_state):
                                    game_state.open_popup()

                    game_state.remove_moving_piece()

            # only animate once each loop
            backdrop.fill(BACKGROUND)
            white_frame.draw(backdrop, mouse_pos)
            black_frame.draw(backdrop, mouse_pos)
            for tile in game_state.board_tiles:
                if game_state.clicked:
                    tile.draw(backdrop, mouse_pos, game_state.clicked)
                    if tile.under_mouse(mouse_pos) and game_state.moving_piece is None and tile.has_pieces():
                        game_state.add_moving_piece(tile.pieces[-1])
                else:
                    tile.draw(backdrop, mouse_pos)
            if game_state.moving_piece:
                draw_drag(backdrop, mouse_pos, game_state.moving_piece)
            game_state.turn_panel.draw(backdrop, game_state.turn)
            display.blit(backdrop, (0, 0))
            pg.display.flip()

            if game_is_over(game_state):
                game_state.end_game()

            # # AI's Turn
            # if (state.turn % 2 == 0 and ai_color == PIECE_BLACK) or (
            #         state.turn % 2 == 1 and ai_color == PIECE_WHITE):
            #     print("AI is thinking...")
            #     # Call the minimax algorithm to determine the best move
            #     _, ai_move = minimax(state, AI_DIFFICULTY_LEVEL, True if ai_color == PIECE_WHITE else False)
            #     if ai_move:  # Execute AI's move if one is found
            #         # old_tile, new_tile = ai_move
            #         # old_tile.move_piece(new_tile)
            #         # state.next_turn()
            #         print(ai_move)
            #     else:
            #         print("AI could not find a move!")

        while game_state.end_loop:
            end_menu(display, game_state, event)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    game_state.quit()
                    break
    return game_state.play_new_game


def main():
    run_game = True
    while run_game:
        run_game = game_loop()


if __name__ == '__main__':
    main()
