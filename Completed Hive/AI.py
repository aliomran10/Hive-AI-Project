import copy, math, time
from settings import WHITE_PIECE, BLACK_PIECE
from move_checker import game_is_over, is_valid_move
import pieces


def evaluate(state):
    white_surround_count = 0
    black_surround_count = 0

    for tile in state.get_tiles_with_pieces():
        for piece in tile.pieces:
            if type(piece) is pieces.Queen:
                adjacent_tiles_with_pieces = [x for x in tile.adjacent_tiles if x.has_pieces()]
                if piece.color == WHITE_PIECE:
                    white_surround_count = len(adjacent_tiles_with_pieces)
                elif piece.color == BLACK_PIECE:
                    black_surround_count = len(adjacent_tiles_with_pieces)
                break

    # Calculate the evaluation score
    # A positive score means the current player (black) is in a favorable position
    # A negative score means the opponent (white) is in a favorable position
    score = (6 - black_surround_count) - (6 - white_surround_count)

    current_player_moves = len(generate_moves(state))
    state.turn += 1
    opponent_moves = len(generate_moves(state))
    state.turn -= 1

    score += 0.1 * (current_player_moves - opponent_moves)

    return score


def generate_moves(state):
    if state.turn % 2 == 1:
        color = WHITE_PIECE
    else:
        color = BLACK_PIECE

    moves = []
    hive_tiles = state.get_tiles_with_pieces(include_inventory=True)
    player_piece_tiles = [tile for tile in hive_tiles if tile.pieces[-1].color == color]
    open_adjacent_tiles = []

    for tile in hive_tiles:
        hive_adjacent_tiles = tile.adjacent_tiles
        for adj_tile in hive_adjacent_tiles:
            if adj_tile not in open_adjacent_tiles and not adj_tile.has_pieces():
                open_adjacent_tiles.append(adj_tile)

    for old_tile in player_piece_tiles:
        for new_tile in open_adjacent_tiles:
            state.moving_piece = old_tile.pieces[-1]
            if is_valid_move(state, old_tile, new_tile):
                moves.append((old_tile, new_tile))
            state.moving_piece = None

    return moves


def simulate_move(state, old_tile, new_tile):
    new_state = state.copy()
    old_tile_sim = next(t for t in new_state.board_tiles if t == old_tile)
    new_tile_sim = next(t for t in new_state.board_tiles if t == new_tile)
    old_tile_sim.move_piece(new_tile_sim)
    return new_state


def undo_move(state, old_tile, new_tile):
    if new_tile.has_pieces():
        piece = new_tile.pieces.pop()
        old_tile.pieces.append(piece)

        state.turn -= 1

    return state


def minimax(state, depth, maximizingPlayer):
    if depth == 0 or game_is_over(state):
        return evaluate(state), None

    best_move = None

    if maximizingPlayer:
        max_eval = float('-inf')
        for move in generate_moves(state):
            old_tile, new_tile = move
            new_state = simulate_move(state, old_tile, new_tile)

            eval_score, _ = minimax(new_state, depth - 1, False)

            undo_move(new_state, old_tile, new_tile)

            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move

        return max_eval, best_move

    else:
        min_eval = float('inf')
        for move in generate_moves(state):
            old_tile, new_tile = move
            new_state = simulate_move(state, old_tile, new_tile)

            eval_score, _ = minimax(new_state, depth - 1, True)

            undo_move(new_state, old_tile, new_tile)

            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move

        return min_eval, best_move


# def minimax(state, depth, maximizingPlayer):
#     if depth == 0 or game_is_over(state):
#         return evaluate(state), None
#
#     best_move = None
#     if maximizingPlayer:
#         max_eval = float('-inf')
#         for move in generate_moves(state):
#             old_tile, new_tile = move
#             old_tile.move_piece(new_tile)  # Apply move
#
#             eval_score, _ = minimax(state, depth - 1, False)
#
#             new_tile.move_piece(old_tile)  # Undo move
#
#             if eval_score > max_eval:
#                 max_eval = eval_score
#                 best_move = move
#         return max_eval, best_move
#     else:
#         min_eval = float('inf')
#         for move in generate_moves(state):
#             old_tile, new_tile = move
#             old_tile.move_piece(new_tile)  # Apply move
#
#             eval_score, _ = minimax(state, depth - 1, True)
#
#             new_tile.move_piece(old_tile)  # Undo move
#
#             if eval_score < min_eval:
#                 min_eval = eval_score
#                 best_move = move
#         return min_eval, best_move


def ai_turn(state):
    best_score = float('-inf') if state.ai_color == BLACK_PIECE else float('inf')
    best_move = None

    valid_moves = generate_moves(state)

    for old_tile, new_tile in valid_moves:
        simulated_state = simulate_move(state, old_tile, new_tile)
        score = evaluate(simulated_state)

        if (state.ai_color == BLACK_PIECE and score > best_score) or \
                (state.ai_color == WHITE_PIECE and score < best_score):
            best_score = score
            best_move = (old_tile, new_tile)

    if best_move:
        old_tile, new_tile = best_move
        moving_piece = old_tile.pieces.pop()
        new_tile.add_piece(moving_piece)
        state.turn += 1

    return best_move


"""-------------------Alpha-Beta Pruning-------------------"""


def alpha_beta_pruning_without_time(state, depth, alpha, beta, maximizing_player):
    if depth == 0 or game_is_over(state):
        return evaluate(state), None

    best_move = None

    possible_moves = generate_moves(state)

    if maximizing_player:
        best_value = -math.inf
        for old_tile, new_tile in possible_moves:
            simulated_state = simulate_move(state, old_tile, new_tile)

            value, _ = alpha_beta_pruning(simulated_state, depth - 1, alpha, beta, False)

            if value > best_value:
                best_value = value
                best_move = (old_tile, new_tile)

            alpha = max(alpha, value)
            if beta <= alpha:
                break

        return best_value, best_move
    else:
        best_value = math.inf
        for old_tile, new_tile in possible_moves:
            simulated_state = simulate_move(state, old_tile, new_tile)

            value, _ = alpha_beta_pruning(simulated_state, depth - 1, alpha, beta, True)

            if value < best_value:
                best_value = value
                best_move = (old_tile, new_tile)

            beta = min(beta, value)
            if beta <= alpha:
                break

        return best_value, best_move


"""-------------------Alpha-Beta Pruning with iterative deepening-------------------"""


def alpha_beta_iterative_deepening(state, max_time, max_depth):
    start_time = time.time()
    best_move = None

    for depth in range(1, max_depth + 1):
        time_elapsed = time.time() - start_time
        if time_elapsed >= max_time:
            break

        best_value, move = alpha_beta_pruning(state, depth, -math.inf, math.inf, True, start_time, max_time)
        if move is not None:
            best_move = move

    return best_move


def alpha_beta_pruning(state, depth, alpha, beta, maximizing_player, start_time, max_time):
    if depth == 0 or game_is_over(state) or (time.time() - start_time >= max_time):
        return evaluate(state), None

    best_move = None

    possible_moves = generate_moves(state)

    if maximizing_player:
        best_value = -math.inf
        for old_tile, new_tile in possible_moves:
            simulated_state = simulate_move(state, old_tile, new_tile)
            value, _ = alpha_beta_pruning(simulated_state, depth - 1, alpha, beta, False, start_time, max_time)

            if value > best_value:
                best_value = value
                best_move = (old_tile, new_tile)

            alpha = max(alpha, value)
            if beta <= alpha:
                break

        return best_value, best_move
    else:
        best_value = math.inf
        for old_tile, new_tile in possible_moves:
            simulated_state = simulate_move(state, old_tile, new_tile)
            value, _ = alpha_beta_pruning(simulated_state, depth - 1, alpha, beta, True, start_time, max_time)

            if value < best_value:
                best_value = value
                best_move = (old_tile, new_tile)

            beta = min(beta, value)
            if beta <= alpha:
                break

        return best_value, best_move
