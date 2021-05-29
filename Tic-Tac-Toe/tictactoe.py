"""
Tic Tac Toe Player by Kiron Deb
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count = 0
    for row in board:
        for item in row:
            if item:
                count += 1
    if count % 2 == 0:
        return X
    return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for c in range(3):
        for i in range(3):
            if not board[c][i]:
                actions.add((c, i))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new = copy.deepcopy(board)
    if new[action[0]][action[1]]:
        raise Exception
    new[action[0]][action[1]] = player(board)
    return new


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    X_win = [X, X, X]
    O_win = [O, O, O]
    col1 = []
    col2 = []
    col3 = []
    dg1 = []
    dg2 = []

    # Check rows
    for row in board:
        if row == X_win:
            return X
        elif row == O_win:
            return O
        col1.append(row[0])
        col2.append(row[1])
        col3.append(row[2])

    # Check columns
    if col1 == X_win or col2 == X_win or col3 == X_win:
        return X
    elif col1 == O_win or col2 == O_win or col3 == O_win:
        return O

    # Check diagonals
    for c in range(3):
        dg1.append(board[c][c])
        dg2.append(board[c][2 - c])
    if dg1 == X_win or dg2 == X_win:
        return X
    elif dg1 == O_win or dg2 == O_win:
        return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    for row in board:
        for item in row:
            if not item:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    victor = winner(board)
    if victor == X:
        return 1
    elif victor == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    if player(board) == X:
        max_util = -1000
        for action in actions(board):
            util = min_value(-2, 2, result(board, action))
            if util == 1:
                best_action = action
                break
            elif util > max_util:
                max_util = util
                best_action = action
    else:
        min_util = 1000
        for action in actions(board):
            util = max_value(-2, 2, result(board, action))
            if util == -1:
                best_action = action
                break
            elif util < min_util:
                min_util = util
                best_action = action
    return best_action


def max_value(alpha, beta, board):
    """"
    Returns the maximum possible utility for the current board
    """
    if terminal(board):
        return utility(board)

    value = -2
    for action in actions(board):
        value = max(value, min_value(-2, 2, result(board, action)))
        if value == 1:
            break
        alpha = max(alpha, value)
        if beta <= alpha:
            break
    return value


def min_value(alpha, beta, board):
    """"
    Returns the minimum possible utility for the current board
    """
    if terminal(board):
        return utility(board)

    value = 2
    for action in actions(board):
        value = min(value, max_value(-2, 2, result(board, action)))
        if value == -1:
            break
        beta = min(beta, value)
        if beta <= alpha:
            break
    return value
