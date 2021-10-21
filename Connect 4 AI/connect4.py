from vars import *

ROWS = 6
COLS = 7


def init():
    return [[0 for i in range(COLS)] for i in range(ROWS)]


def show_text(board):
    text = ""
    for row in board:
        for spot in row:
            if spot == 0:
                text += "|   "
            elif spot == 1:
                text += "| O "
            elif spot == 2:
                text += "| X "
        text += "|\n"
    return text


def show(board):
    try:
        for x in range(7):
            for y in range(6):
                if board[y][x] == 1:
                    col = (255, 0, 0)
                elif board[y][x] == 2:
                    col = (0, 0, 255)
                else:
                    col = background_color
                pygame.draw.rect(screen, col, ((x * 100, y * 100), (100, 100)))
    except TypeError:
        print("wtf")


def get_available_moves(board):
    possible = []
    for col in range(COLS - 1, -1, -1):
        if board[0][col] == 0:
            possible.append(col)
    return possible


def place_piece(board, col, player):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == 0:
            board[row][col] = player
            return board
    return board


def remove_piece(board, col):
    for row in range(ROWS):
        if board[row][col] != 0:
            board[row][col] = 0
            return board


def has_won(board, player):
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLS - 3):
            if board[row][col] == player and board[row][col + 1] == player and board[row][col + 2] == player and board[row][col + 3] == player:
                return True, [(row, col) for i in range(4)]
    # Vertical check
    for row in range(ROWS - 3):
        for col in range(COLS):
            if board[row][col] == player and board[row + 1][col] == player and board[row + 2][col] == player and board[row + 3][col] == player:
                return True, [(row, col) for i in range(4)]
    # Diagonal check down left, up right
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if board[row][col] == player and board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and board[row + 3][col + 3] == player:
                return True, [(row, col) for i in range(4)]
    # Diagonal check down right, up left
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if board[row][col] == player and board[row + 1][col - 1] == player and board[row + 2][col - 2] == player and board[row + 3][col - 3] == player:
                return True, [(row, col) for i in range(4)]
    return False


def evaluate_selection(selection, player):
    score = 0
    if selection.count(player) == 4:
        score += 100
    elif selection.count(player) == 3 and selection.count(0) == 1:
        score += 5
    elif selection.count(player) == 2 and selection.count(0) == 2:
        score += 2
    if selection.count(player % 2 + 1) == 3 and selection.count(0) == 1:
        score -= 4
    return score


def get_score(board):
    if has_won(board, 1):
        return -1000
    elif has_won(board, 2):
        return 1000
    else:
        score = 0

        # Score center column
        center_column = [board[row][int(COLS // 2)] for row in range(ROWS)]
        score += center_column.count(2) * 3

        # Score Horizontal
        for row in range(ROWS):
            for col in range(COLS - 3):
                score += evaluate_selection(board[row][col:col + 4], 2)

        # Score Vertical
        for row in range(ROWS - 3):
            for col in range(COLS):
                score += evaluate_selection([board[row][col], board[row + 1][col], board[row + 2][col], board[row + 3][col]], 2)

        # Score diagonal to top right
        for row in range(ROWS - 3):
            for col in range(COLS - 3):
                score += evaluate_selection([board[row + i][col + i] for i in range(4)], 2)

        # Score diagonal to top left
        for row in range(ROWS - 3):
            for col in range(4, COLS):
                score += evaluate_selection([board[row + i][col - i] for i in range(4)], 2)

        return score


def find_best_move(board, depth):
    best_move = 0
    best_score = -1000000000
    for move in get_available_moves(board):
        board = place_piece(board, move, 2)
        score = minimax(board, depth, -1000000000, 1000000000, False)
        board = remove_piece(board, move)
        if score > best_score:
            best_score = score
            best_move = move
    return best_move


def minimax(board, depth, alpha, beta, maximizing):
    if depth == 0 or len(get_available_moves(board)) == 0:
        return get_score(board)

    if maximizing:
        maxEval = -1000000000
        for move in get_available_moves(board):
            board = place_piece(board, move, 2)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board = remove_piece(board, move)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, maxEval)
            if beta <= alpha:
                break
        return maxEval

    else:
        minEval = 1000000000
        for move in get_available_moves(board):
            board = place_piece(board, move, 1)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board = remove_piece(board, move)
            minEval = min(minEval, eval)
            beta = min(beta, minEval)
            if beta <= alpha:
                break
        return minEval


def events():
    global run, click
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            click = True


def wait():
    global run
    pygame.display.flip()
    while run:
        events()
        clock.tick(30)


if __name__ == "__main__":
    global run, click
    board = init()
    turn = True
    while run:
        events()

        show(board)

        if has_won(board, 1):
            print("Red won")
            wait()
        if has_won(board, 2):
            print("Blue won")
            wait()

        if pygame.mouse.get_pressed()[0] and turn:
            x = int(pygame.mouse.get_pos()[0] / 100)
            if x in get_available_moves(board):
                board = place_piece(board, x, 1)
                turn = False

        else:
            if not turn:
                board = place_piece(board, find_best_move(board, 5), 2)
                turn = True

        screen.blit(grid, (0, 0))
        pygame.display.flip()
        clock.tick(30)
