from board import Board
from game_grid import GameGrid
from ai import AI

WIDTH = 640
HEIGHT = 640
SIZE = 8
GREEN = 153
WHITE = 255
BLACK = 0
CHECK_X = 360
CHECK_Y = 280

game_board = Board(WIDTH, HEIGHT, SIZE)
computer_player = AI(game_board.board_logic.click_points, SIZE)


def setup():
    """Board setup"""
    size(WIDTH, HEIGHT)
    background(0, GREEN, 0)
    game_board.display()
    print "Please Enter Your Name"
    answer = input('enter your name')
    game_board.name = answer


def draw():
    """Contains constantly updating variables of the game, including the game's AI mechanism"""
    if game_board.display_turn and not game_board.game_over:
        color = ""
        if game_board.current_color == BLACK:
            color = "BLACK"
        else:
            color = "WHITE"
        print "CURRENT TURN:", color
        game_board.display_turn = False

    if (game_board.current_color == BLACK and
            game_board.needs_check):
        game_board.update_click(CHECK_X, CHECK_Y)
        game_board.needs_check = False

    if game_board.current_color == WHITE:
        game_board.update_click(CHECK_X, CHECK_Y)
        delay(500)
        x, y = computer_player.play_turn(game_board.board_logic)
        game_board.update_click(x, y)

    if game_board.game_over and game_board.file_handle_needed:
        game_board.file_handling(game_board.game_pieces)
        game_board.file_handle_needed = False


def mouseClicked():
    """Mouse clicked updater"""
    if game_board.current_color == BLACK:
        game_board.update_click(mouseX, mouseY)


def input(self, message=''):
    """Custom input function"""
    from javax.swing import JOptionPane
    return JOptionPane.showInputDialog(frame, message)
