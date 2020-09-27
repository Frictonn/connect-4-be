from django.conf import settings

from connect4.games.models import Move, Game, RED, YELLOW


def get_all_moves(game_obj):
    return game_obj.moves.all()


def check_if_four_connected(current_board, current_row, current_column, coin):
    # vertical check
    if current_row < 3:
        return False

    if current_board[current_row - 1][current_column] == coin and current_board[current_row - 2][current_column] == coin and current_board[current_row - 3][current_column] == coin:
        return True

    # TODO: horizontal check

    # TODO: diagonal check
    return False


def is_winning_move(game_obj, moves, row, column, coin):
    rows, cols = (settings.ROW_MAX_VALUE, settings.COLUMN_MAX_VALUE)
    current_board = [['' for i in range(cols)] for j in range(rows)]

    for move in moves:
        current_board[move.row][move.column] = move.coin

    current_board[row][column] = coin

    if check_if_four_connected(current_board, row, column, coin):
        game_obj.status = Game.FINISHED
        game_obj.winner = coin
    else:
        game_obj.status = Game.INITIALIZED
    game_obj.save()


def is_valid_column(moves, column):
    topmost_move_obj = moves.filter(column=column).order_by('-row').first()
    if not topmost_move_obj:
        return True, 0
    if topmost_move_obj == settings.ROW_MAX_VALUE:
        return False, -1
    return True, topmost_move_obj.row + 1


def is_valid_move(game_id, column, coin):
    game_obj = Game.objects.filter(id=game_id).first()
    moves = get_all_moves(game_obj)
    current_moves_count = moves.count()

    if current_moves_count % 2 == 0 and coin == RED:
        return False, -1, "This is Yellow Player's Turn"
    elif current_moves_count % 2 != 0 and coin == YELLOW:
        return False, -1, "This is Red Player's Turn"

    is_valid_col, row = is_valid_column(moves, column)

    if not is_valid_col:
        return False, -1, "This column is already filled"

    is_winning_move(game_obj, moves, row, column, coin)
    return True, row, ""
