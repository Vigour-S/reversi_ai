import copy
import sys
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response

evaluation = [[99, -8, 8, 6, 6, 8, -8, 99],
              [-8, -24, -4, -3, -3, -4, -24, -8],
              [8, -4, 7, 4, 4, 7, -4, 8],
              [6, -3, 4, 0, 0, 4, -3, 6],
              [6, -3, 4, 0, 0, 4, -3, 6],
              [8, -4, 7, 4, 4, 7, -4, 8],
              [-8, -24, -4, -3, -3, -4, -24, -8],
              [99, -8, 8, 6, 6, 8, -8, 99]]


def index(request):
    return render_to_response('index.html')


@csrf_exempt
def request_util(request):
    row1 = request.GET.getlist('myArray[0][]')
    row2 = request.GET.getlist('myArray[1][]')
    row3 = request.GET.getlist('myArray[2][]')
    row4 = request.GET.getlist('myArray[3][]')
    row5 = request.GET.getlist('myArray[4][]')
    row6 = request.GET.getlist('myArray[5][]')
    row7 = request.GET.getlist('myArray[6][]')
    row8 = request.GET.getlist('myArray[7][]')
    game_board = [row1, row2, row3, row4, row5, row6, row7, row8]
    helper(game_board)
    result = 10 * next_move[0] + next_move[1]
    return HttpResponse(result)

depth = 7  # reassigned in inner function
player = 'O'

if player == 'X':
    opponent = 'O'
else:
    opponent = 'X'
next_move = ()


def alpha_beta_pruning(board, player, opponent, num, turn, alpha, beta, utility, pass_move):

    if turn == 'maximizer':
        utility = -sys.maxsize
    else:
        utility = sys.maxsize

    if num == depth or pass_move == 2:
        return evaluate(board)
    not_found = True
    for x in range(0, 8):
        for y in range(0, 8):
            if board[x][y] == '*':
                valid = False
                new_board = copy.deepcopy(board)
                for a in range(-1, 2):
                    for b in range(-1, 2):
                        _x = x + a
                        _y = y + b
                        flag = False
                        while 0 <= _x < 8 and 0 <= _y < 8 and board[_x][_y] == opponent:
                            flag = True
                            _x += a
                            _y += b
                        # find a valid piece
                        if flag and 0 <= _x < 8 and 0 <= _y < 8 and board[_x][_y] == player:
                            valid = True
                            _x -= a
                            _y -= b
                            # flip the pieces
                            while new_board[_x][_y] == opponent:
                                new_board[_x][_y] = player
                                _x -= a
                                _y -= b
                            new_board[x][y] = player

                if valid:
                    not_found = False
                    if turn == 'maximizer':
                        change = utility    # to find the best next move
                        utility = max(utility, alpha_beta_pruning(new_board, opponent, player, num + 1,
                                                                  'minimizer', alpha, beta, utility, 0))
                        if change != utility and num == 0:
                            global next_move
                            next_move = (x, y)
                        alpha = max(alpha, utility)
                        if beta <= alpha:
                            return utility
                    else:
                        utility = min(utility, alpha_beta_pruning(new_board, opponent, player, num + 1,
                                                                  'maximizer', alpha, beta, utility, 0))
                        beta = min(beta, utility)
                        if beta <= alpha:
                            return utility
    if not_found:
        if turn == 'maximizer':
            utility = max(utility, alpha_beta_pruning(board, opponent, player, num + 1,
                                                      'minimizer', alpha, beta, utility, pass_move + 1))
            alpha = max(alpha, utility)
            if beta <= alpha:
                return utility
        else:
            utility = min(utility, alpha_beta_pruning(board, opponent, player, num + 1,
                                                      'maximizer', alpha, beta, utility, pass_move + 1))
            beta = min(beta, utility)
            if beta <= alpha:
                return utility
    return utility


def evaluate(board):
    rank = 0
    for x in range(0, 8):
        for y in range(0, 8):
            if board[x][y] == player:
                rank += evaluation[x][y]
            if board[x][y] == opponent:
                rank -= evaluation[x][y]
    return rank


def helper(game_board):
    global depth
    depth = 5
    global next_move
    next_move = ()
    alpha_beta_pruning(game_board, player, opponent, 0, 'maximizer', -sys.maxsize, sys.maxsize, sys.maxsize, 0)
