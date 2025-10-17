"""
Interactive Othello game with a minimax-based AI opponent.
"""

import sys
from typing import List, Optional, Sequence, Tuple, Union

import pygame

INITIAL_STATE = ('........',) * 3 + ('...XO...', '...OX...') + ('........',) * 3

DIRECTIONS = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))


def flips(board, player, location):
    """
    :param board: A sequence of strings
    :param player: 'X' or 'O'
    :param location: A pair (r, c) with 0 <= r < 8 and 0 <= c < 8
    :return: A collection of pairs of locations of opponent's pieces that would be flipped by this move
    """
    def f(r, c, dr, dc):  # Find flips starting at (r, c) and looking in direction (dr, dc)
        line = []
        while True:
            r, c = (r + dr, c + dc)
            if not (0 <= r < 8 and 0 <= c < 8):
                return []  # Edge of board -- no capture
            if board[r][c] == '.':
                return []  # Empty space -- no capture
            if board[r][c] == player:
                return line  # Friendly piece -- capture all opposing pieces seen so far
            line.append((r, c))
    result = []
    for d in DIRECTIONS:
        result.extend(f(*location, *d))
    return result



def successor(board, player, move):
    """
    :param board: A sequence of strings
    :param player: 'X' or 'O'
    :param move: Either 'pass' or a pair (r, c) with 0 <= r < 8 and 0 <= c < 8
    :return: The board that would result if player played move
    """
    if move == 'pass':
        return board

    r, c = move
    result = [list(row) for row in board] #tuple to list of list
    result[r][c] = player
    for row, col in flips(board, player, move):
        result[row][col] = player

    return tuple(map("".join, result)) #found that on stackoverflow and it seems to work



def legal_moves(board, player):
    """
    :param board: A sequence of strings
    :param player: 'X' or 'O'
    :return: A collection of legal moves for player from board; each is (r, c). Returns an empty collection if neither
    player has a legal move or ['pass'] if player cannot make a capturing move.
    """
    result = []
    game_over = True
    for r in range(8):
        for c in range(8):
            if board[r][c] == '.':
                here = (r, c)
                if flips(board, player, here):
                    game_over = False
                    result.append(here)
                # The inclusion of game_over in the condition below is for efficiency:
                # If it has already been determined that the game is not over, there's no need to check
                # for opposing legal moves
                elif game_over and flips(board, opposite(player), here):
                    game_over = False
    if result or game_over:
        return result
    return ['pass']


def score(board):
    """
    :param board: A sequence of strings
    :return: The difference between the number of pieces 'X' has and the number 'O' has. This is therefore positive if
    'X' is winning, negative if 'O' is winning, and 0 if the score is tied.
    """
    count_x = 0
    count_o = 0
    x = 'X'
    o = 'O'
    for r in range(8):
        for c in range(8):
            if board[r][c] != '.':
                here = board[r][c]
                if here == x:
                    count_x+=1
                elif here == o:
                    count_o+=1
    return count_x - count_o


def opposite(player):
    if player == 'X':
        return 'O'
    return 'X'


Board = Sequence[str]
Player = str
Move = Tuple[int, int]
MoveResult = Union[str, Move, None]


def value(board: Board, player: Player, depth: int) -> int:
    """
    :param board: A sequence of strings
    :param player: 'X' or 'O'
    :param depth: At least 1; greater depth is slower but smarter
    :return: The value of board if it is player's turn
    """
    #Returns value of total flips for your best move and then other players best move. Positive value is net gain for you: negative value is net loss for you

    if depth == 0:
        return score(board)

    moves = legal_moves(board, player)
    if not moves:
        return score(board)
    if moves == ['pass']:
        return value(board, opposite(player), max(depth - 1, 0))

    if player == 'X':
        best_value = -float('inf')
        for move in moves:
            test_board = successor(board, player, move)
            val = value(test_board, opposite(player), depth - 1)
            if best_value < val:
                best_value = val
        return best_value

    # player == 'O'
    best_value = float('inf')
    for move in moves:
        test_board = successor(board, player, move)
        val = value(test_board, opposite(player), depth - 1)
        if best_value > val:
            best_value = val
    return best_value


def less(x, y):
    return x < y


def greater(x, y):
    return x > y


def best_move(board: Board, player: Player, depth: int) -> MoveResult:
    """
    :param board: A seq of strings
    :param player: 'X' or 'O'
    :param depth: At least 1; greater depth is slower but smarter
    :return: The best move (index) for player
    """

    moves = legal_moves(board, player)
    if not moves:
        return None
    if moves == ['pass']:
        return 'pass'

    if player == 'X':
        best_play = None
        best_value = -float('inf')
        for move in moves:
            val = value(successor(board, player, move), opposite(player), depth - 1)
            if best_value < val:
                best_value = val
                best_play = move
        return best_play

    best_play = None
    best_value = float('inf')
    for move in moves:
        val = value(successor(board, player, move), opposite(player), depth - 1)
        if best_value > val:
            best_value = val
            best_play = move
    return best_play


def print_board(board):
    print(' 01234567')
    for i in range(8):
        print(str(i) + board[i] + str(i))
    print(' 01234567')
    print()


def console_main():
    board = INITIAL_STATE
    player = 'X'
    depth = 5
    print("Starting console Othello. Press Ctrl+C to exit.")
    while True:
        moves = legal_moves(board, player)
        if not moves:
            break
        if moves == ['pass']:
            move = 'pass'
        elif player == 'X':
            move = best_move(board, player, depth)
        else:
            print('Your move.')
            r = int(input('Row: '))
            c = int(input('Column: '))
            move = (r, c)
        board = successor(board, player, move)
        print_board(board)
        player = opposite(player)
    w = score(board)
    if w > 0:
        print('X wins!')
    elif w < 0:
        print('O wins!')
    else:
        print('Tie.')


WINDOW_WIDTH = 960
WINDOW_HEIGHT = 720
BOARD_SIZE = 640
BOARD_LEFT = 80
BOARD_TOP = 60
SQUARE_SIZE = BOARD_SIZE // 8

BACKGROUND_COLOR = (15, 18, 32)
GRADIENT_TOP = (27, 31, 51)
GRADIENT_BOTTOM = (12, 13, 22)
BOARD_FRAME_OUTER = (32, 52, 41)
BOARD_FRAME_INNER = (19, 92, 52)
BOARD_COLOR = (31, 115, 64)
GRID_COLOR = (20, 88, 46)
HINT_COLOR = (255, 215, 0, 120)
LAST_MOVE_COLOR = (255, 235, 130)
LAST_MOVE_DOT_COLOR = (220, 60, 70)
BLACK_DISC = (25, 25, 25)
BLACK_DISC_HILITE = (70, 70, 70)
WHITE_DISC = (235, 235, 235)
WHITE_DISC_SHADOW = (180, 180, 180)
PANEL_BG = (28, 32, 50)
PANEL_BORDER = (70, 80, 110)
TEXT_PRIMARY = (240, 244, 255)
TEXT_SECONDARY = (164, 174, 193)
STATUS_BG = (22, 25, 41)

DIFFICULTIES = [
    ("Easy", 1, "Depth 1 · Quick replies"),
    ("Medium", 2, "Depth 2 · Casual play"),
    ("Hard", 5, "Depth 5 · Strong opponent"),
]

HUMAN_PLAYER: Player = 'X'
AI_PLAYER: Player = 'O'


def count_pieces(board: Board) -> Tuple[int, int]:
    x_count = sum(row.count('X') for row in board)
    o_count = sum(row.count('O') for row in board)
    return x_count, o_count


def determine_winner(board: Board) -> str:
    x_score, o_score = count_pieces(board)
    if x_score > o_score:
        return "human"
    if o_score > x_score:
        return "ai"
    return "draw"


def player_label(player: Player) -> str:
    if player == 'X':
        return "You (Black)"
    if player == 'O':
        return "AI (White)"
    return player


def board_position_from_mouse(pos: Tuple[int, int]) -> Optional[Move]:
    x, y = pos
    if not (BOARD_LEFT <= x < BOARD_LEFT + BOARD_SIZE and BOARD_TOP <= y < BOARD_TOP + BOARD_SIZE):
        return None
    col = (x - BOARD_LEFT) // SQUARE_SIZE
    row = (y - BOARD_TOP) // SQUARE_SIZE
    return int(row), int(col)


def light_gradient(surface: pygame.Surface) -> None:
    """Draw a subtle vertical gradient as the background."""
    top_color = GRADIENT_TOP
    bottom_color = GRADIENT_BOTTOM
    for y in range(WINDOW_HEIGHT):
        ratio = y / WINDOW_HEIGHT
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (WINDOW_WIDTH, y))


def draw_disc(surface: pygame.Surface, center: Tuple[int, int], color: Tuple[int, int, int], accent: Tuple[int, int, int], radius: int) -> None:
    pygame.draw.circle(surface, color, center, radius)
    pygame.draw.circle(surface, accent, center, radius - max(2, radius // 6))


def draw_board(surface: pygame.Surface, board: Board, highlight_moves: List[Move], last_move: Optional[Move],
               current_player: Player, difficulty_label: str, status_message: str, fonts: dict) -> None:
    light_gradient(surface)

    frame_rect = pygame.Rect(BOARD_LEFT - 14, BOARD_TOP - 14, BOARD_SIZE + 28, BOARD_SIZE + 28)
    inner_frame_rect = frame_rect.inflate(-10, -10)
    board_rect = pygame.Rect(BOARD_LEFT, BOARD_TOP, BOARD_SIZE, BOARD_SIZE)

    pygame.draw.rect(surface, BOARD_FRAME_OUTER, frame_rect, border_radius=24)
    pygame.draw.rect(surface, BOARD_FRAME_INNER, inner_frame_rect, border_radius=20)
    pygame.draw.rect(surface, BOARD_COLOR, board_rect, border_radius=16)

    # Grid lines
    for i in range(1, 8):
        y = BOARD_TOP + i * SQUARE_SIZE
        x = BOARD_LEFT + i * SQUARE_SIZE
        pygame.draw.line(surface, GRID_COLOR, (BOARD_LEFT, y), (BOARD_LEFT + BOARD_SIZE, y), 2)
        pygame.draw.line(surface, GRID_COLOR, (x, BOARD_TOP), (x, BOARD_TOP + BOARD_SIZE), 2)

    # Highlight last move
    if last_move:
        r, c = last_move
        move_rect = pygame.Rect(
            BOARD_LEFT + c * SQUARE_SIZE,
            BOARD_TOP + r * SQUARE_SIZE,
            SQUARE_SIZE,
            SQUARE_SIZE
        )
        pygame.draw.rect(surface, LAST_MOVE_COLOR, move_rect.inflate(-SQUARE_SIZE // 3, -SQUARE_SIZE // 3), width=3, border_radius=8)

    # Hint markers
    hint_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
    pygame.draw.circle(hint_surface, HINT_COLOR, (SQUARE_SIZE // 2, SQUARE_SIZE // 2), SQUARE_SIZE // 6)
    for r, c in highlight_moves:
        surface.blit(hint_surface, (BOARD_LEFT + c * SQUARE_SIZE, BOARD_TOP + r * SQUARE_SIZE))

    # Pieces
    radius = SQUARE_SIZE // 2 - 6
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece == '.':
                continue
            center = (BOARD_LEFT + c * SQUARE_SIZE + SQUARE_SIZE // 2,
                      BOARD_TOP + r * SQUARE_SIZE + SQUARE_SIZE // 2)
            if piece == 'X':
                draw_disc(surface, center, BLACK_DISC, BLACK_DISC_HILITE, radius)
            else:
                draw_disc(surface, center, WHITE_DISC, WHITE_DISC_SHADOW, radius)

    if last_move:
        r, c = last_move
        center = (BOARD_LEFT + c * SQUARE_SIZE + SQUARE_SIZE // 2,
                  BOARD_TOP + r * SQUARE_SIZE + SQUARE_SIZE // 2)
        dot_radius = max(4, SQUARE_SIZE // 10)
        pygame.draw.circle(surface, LAST_MOVE_DOT_COLOR, center, dot_radius)

    # Info panel
    panel_rect = pygame.Rect(BOARD_LEFT + BOARD_SIZE + 32, BOARD_TOP, 220, 320)
    pygame.draw.rect(surface, PANEL_BG, panel_rect, border_radius=20)
    pygame.draw.rect(surface, PANEL_BORDER, panel_rect, width=2, border_radius=20)

    title = fonts["panel_title"].render("Match Info", True, TEXT_PRIMARY)
    surface.blit(title, (panel_rect.x + 20, panel_rect.y + 20))

    difficulty_text = fonts["body"].render(f"Difficulty: {difficulty_label}", True, TEXT_SECONDARY)
    surface.blit(difficulty_text, (panel_rect.x + 20, panel_rect.y + 70))

    current_text = fonts["body"].render(f"Turn: {player_label(current_player)}", True, TEXT_SECONDARY)
    surface.blit(current_text, (panel_rect.x + 20, panel_rect.y + 110))

    # Scores
    x_score, o_score = count_pieces(board)
    score_title = fonts["panel_title"].render("Score", True, TEXT_PRIMARY)
    surface.blit(score_title, (panel_rect.x + 20, panel_rect.y + 160))

    disc_radius = 18
    score_rows = [
        (panel_rect.y + 210, BLACK_DISC, BLACK_DISC_HILITE, x_score, "You"),
        (panel_rect.y + 266, WHITE_DISC, WHITE_DISC_SHADOW, o_score, "AI"),
    ]
    for row_y, fill, accent, tally, label in score_rows:
        center = (panel_rect.x + 38, row_y)
        draw_disc(surface, center, fill, accent, disc_radius)
        text_surface = fonts["body"].render(f"{tally:>2} · {label}", True, TEXT_SECONDARY)
        text_pos = (panel_rect.x + 80, row_y - text_surface.get_height() // 2 - 2)
        surface.blit(text_surface, text_pos)

    hint_text = fonts["small"].render("Click a highlighted square to play.", True, TEXT_SECONDARY)
    hint_rect = hint_text.get_rect()
    hint_rect.left = panel_rect.x + 20
    hint_rect.bottom = panel_rect.bottom - 16
    surface.blit(hint_text, hint_rect)

    # Status bar
    status_rect = pygame.Rect(BOARD_LEFT - 14, BOARD_TOP + BOARD_SIZE + 24, BOARD_SIZE + 28, 64)
    pygame.draw.rect(surface, STATUS_BG, status_rect, border_radius=16)
    pygame.draw.rect(surface, PANEL_BORDER, status_rect, width=2, border_radius=16)

    status_surface = fonts["status"].render(status_message, True, TEXT_PRIMARY)
    status_pos = status_surface.get_rect(center=status_rect.center)
    surface.blit(status_surface, status_pos)


def show_start_screen(screen: pygame.Surface, clock: pygame.time.Clock, fonts: dict) -> Tuple[int, str]:
    button_width = 320
    button_height = 72
    button_margin = 20
    card_width = 460
    card_height = 440
    card_rect = pygame.Rect(
        (WINDOW_WIDTH - card_width) // 2,
        (WINDOW_HEIGHT - card_height) // 2,
        card_width,
        card_height
    )
    button_top = card_rect.y + 180

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                for index, (label, depth, description) in enumerate(DIFFICULTIES):
                    rect = pygame.Rect(
                        card_rect.x + (card_width - button_width) // 2,
                        button_top + index * (button_height + button_margin),
                        button_width,
                        button_height
                    )
                    if rect.collidepoint(mouse_pos):
                        return depth, label

        light_gradient(screen)

        #Card background
        pygame.draw.rect(screen, PANEL_BG, card_rect, border_radius=26)
        pygame.draw.rect(screen, PANEL_BORDER, card_rect, width=2, border_radius=26)

        title_surface = fonts["title"].render("Othello AI", True, TEXT_PRIMARY)
        subtitle_surface = fonts["subtitle"].render("Choose your challenge level", True, TEXT_SECONDARY)
        screen.blit(title_surface, title_surface.get_rect(center=(WINDOW_WIDTH // 2, card_rect.y + 60)))
        screen.blit(subtitle_surface, subtitle_surface.get_rect(center=(WINDOW_WIDTH // 2, card_rect.y + 110)))
        turn_surface = fonts["small"].render("You play as black and make the first move.", True, TEXT_SECONDARY)
        screen.blit(turn_surface, turn_surface.get_rect(center=(WINDOW_WIDTH // 2, card_rect.y + 140)))

        mouse_pos = pygame.mouse.get_pos()
        for index, (label, depth, description) in enumerate(DIFFICULTIES):
            rect = pygame.Rect(
                card_rect.x + (card_width - button_width) // 2,
                button_top + index * (button_height + button_margin),
                button_width,
                button_height
            )
            hovered = rect.collidepoint(mouse_pos)
            color = (64, 140, 96) if hovered else (47, 108, 74)
            pygame.draw.rect(screen, color, rect, border_radius=18)
            pygame.draw.rect(screen, PANEL_BORDER, rect, width=2, border_radius=18)

            label_surface = fonts["button"].render(label, True, TEXT_PRIMARY)
            desc_surface = fonts["small"].render(description, True, TEXT_SECONDARY)
            screen.blit(label_surface, label_surface.get_rect(center=(rect.centerx, rect.y + 24)))
            screen.blit(desc_surface, desc_surface.get_rect(center=(rect.centerx, rect.y + 50)))

        esc_surface = fonts["tiny"].render("Press Esc to exit", True, TEXT_SECONDARY)
        screen.blit(esc_surface, esc_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 60)))

        credit_surface = fonts["tiny"].render("Inspired by https://www.eothello.com/ - Created by Panagiotis", True, TEXT_SECONDARY)
        screen.blit(credit_surface, credit_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 24)))

        pygame.display.flip()


def play_match(screen: pygame.Surface, clock: pygame.time.Clock, depth: int, difficulty_label: str, fonts: dict) -> dict:
    board = INITIAL_STATE
    current_player: Player = HUMAN_PLAYER
    last_move: Optional[Move] = None
    passes_in_a_row = 0
    ai_pending_move: Optional[Move] = None
    ai_execute_at = 0
    status_message = "You have the first move."
    message_expires = pygame.time.get_ticks() + 1500

    while True:
        clock.tick(60)
        current_time = pygame.time.get_ticks()

        if current_time > message_expires:
            status_message = "Your turn" if current_player == HUMAN_PLAYER else "AI thinking..."

        valid_moves = legal_moves(board, current_player)
        if not valid_moves:
            passes_in_a_row += 1
            if passes_in_a_row >= 2:
                x_score, o_score = count_pieces(board)
                outcome = determine_winner(board)
                return {
                    "board": board,
                    "scores": (x_score, o_score),
                    "winner": outcome,
                    "last_move": last_move,
                    "difficulty": difficulty_label,
                }
            status_message = f"{player_label(current_player)} has no moves and passes."
            message_expires = current_time + 2000
            current_player = opposite(current_player)
            ai_pending_move = None
            ai_execute_at = current_time + 350 if current_player == AI_PLAYER else 0
            continue

        if valid_moves == ['pass']:
            passes_in_a_row += 1
            status_message = f"{player_label(current_player)} passes."
            message_expires = current_time + 2000
            current_player = opposite(current_player)
            ai_pending_move = None
            ai_execute_at = current_time + 350 if current_player == AI_PLAYER else 0
            continue

        passes_in_a_row = 0
        human_turn = current_player == HUMAN_PLAYER

        move_made = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if human_turn and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                candidate = board_position_from_mouse(event.pos)
                if candidate and candidate in valid_moves:
                    board = successor(board, current_player, candidate)
                    last_move = candidate
                    current_player = opposite(current_player)
                    status_message = "AI thinking..."
                    message_expires = current_time + 1500
                    ai_pending_move = None
                    ai_execute_at = current_time + 350
                    move_made = True
                    break
        if move_made:
            continue

        if current_player == AI_PLAYER:
            if ai_pending_move is None:
                ai_pending_move = best_move(board, current_player, depth)
                if ai_pending_move is None or ai_pending_move == 'pass':
                    passes_in_a_row += 1
                    status_message = "AI passes."
                    message_expires = current_time + 2000
                    current_player = HUMAN_PLAYER
                    ai_pending_move = None
                    continue
                ai_execute_at = current_time + 400
                status_message = "AI thinking..."
                message_expires = current_time + 1500
            elif current_time >= ai_execute_at:
                board = successor(board, current_player, ai_pending_move)
                last_move = ai_pending_move
                current_player = opposite(current_player)
                ai_pending_move = None
                status_message = "Your turn"
                message_expires = current_time + 1200
                continue

        #Draw frame
        highlight_moves = valid_moves if human_turn else []
        draw_board(
            screen,
            board,
            highlight_moves,
            last_move,
            current_player,
            difficulty_label,
            status_message,
            fonts
        )
        pygame.display.flip()


def show_game_over(screen: pygame.Surface, clock: pygame.time.Clock, result: dict, fonts: dict) -> str:
    board = result["board"]
    x_score, o_score = result["scores"]
    winner = result["winner"]
    last_move = result.get("last_move")
    difficulty_label = result.get("difficulty", "Unknown")

    if winner == "human":
        title_text = "You win!"
        detail_text = "Great job controlling the board."
    elif winner == "ai":
        title_text = "AI wins!"
        detail_text = "Try a new strategy or drop the difficulty."
    else:
        title_text = "It's a tie."
        detail_text = "Balanced play from both sides."

    buttons = [
        ("Play Again", "again"),
        ("Change Difficulty", "difficulty"),
        ("Quit", "quit"),
    ]

    button_width = 260
    button_height = 58
    spacing = 20
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))

    card_width = 520
    card_height = 400
    card_rect = pygame.Rect(
        (WINDOW_WIDTH - card_width) // 2,
        (WINDOW_HEIGHT - card_height) // 2,
        card_width,
        card_height
    )

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for idx, (_, action) in enumerate(buttons):
                    rect = pygame.Rect(
                        card_rect.x + (card_width - button_width) // 2,
                        card_rect.y + 200 + idx * (button_height + spacing),
                        button_width,
                        button_height
                    )
                    if rect.collidepoint(event.pos):
                        return action

        #Redraw board as background state
        draw_board(screen, board, [], last_move, "Game Over", difficulty_label, "Game over", fonts)
        screen.blit(overlay, (0, 0))

        pygame.draw.rect(screen, PANEL_BG, card_rect, border_radius=30)
        pygame.draw.rect(screen, PANEL_BORDER, card_rect, width=2, border_radius=30)

        title_surface = fonts["title"].render(title_text, True, TEXT_PRIMARY)
        detail_surface = fonts["subtitle"].render(detail_text, True, TEXT_SECONDARY)
        score_surface = fonts["body"].render(f"Final score — You: {x_score}  AI: {o_score}", True, TEXT_PRIMARY)

        screen.blit(title_surface, title_surface.get_rect(center=(WINDOW_WIDTH // 2, card_rect.y + 80)))
        screen.blit(detail_surface, detail_surface.get_rect(center=(WINDOW_WIDTH // 2, card_rect.y + 120)))
        screen.blit(score_surface, score_surface.get_rect(center=(WINDOW_WIDTH // 2, card_rect.y + 160)))

        mouse_pos = pygame.mouse.get_pos()
        for idx, (label, _) in enumerate(buttons):
            rect = pygame.Rect(
                card_rect.x + (card_width - button_width) // 2,
                card_rect.y + 200 + idx * (button_height + spacing),
                button_width,
                button_height
            )
            hovered = rect.collidepoint(mouse_pos)
            color = (70, 140, 100) if hovered else (52, 112, 80)
            pygame.draw.rect(screen, color, rect, border_radius=18)
            pygame.draw.rect(screen, PANEL_BORDER, rect, width=2, border_radius=18)

            label_surface = fonts["button"].render(label, True, TEXT_PRIMARY)
            screen.blit(label_surface, label_surface.get_rect(center=rect.center))

        pygame.display.flip()


def run_game():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Othello AI — Minimax Agent")
    clock = pygame.time.Clock()

    fonts = {
        "title": pygame.font.SysFont("Poppins", 60, bold=True),
        "subtitle": pygame.font.SysFont("Poppins", 26),
        "panel_title": pygame.font.SysFont("Poppins", 24, bold=True),
        "body": pygame.font.SysFont("Poppins", 20),
        "button": pygame.font.SysFont("Poppins", 24, bold=True),
        "small": pygame.font.SysFont("Poppins", 18),
        "status": pygame.font.SysFont("Poppins", 24),
        "tiny": pygame.font.SysFont("Poppins", 16),
    }

    while True:
        depth, difficulty_label = show_start_screen(screen, clock, fonts)
        while True:
            result = play_match(screen, clock, depth, difficulty_label, fonts)
            action = show_game_over(screen, clock, result, fonts)
            if action == "again":
                continue
            if action == "difficulty":
                break
            if action == "quit":
                pygame.quit()
                sys.exit()


if __name__ == '__main__':
    run_game()
