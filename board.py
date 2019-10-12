from board_logic import BoardLogic
from game_manager import GameManager
from game_piece import GamePiece
import re

# A board game for Othello
BLACK = 0
WHITE = 255


class Board:
    """A class for the Othello board"""

    def __init__(self, WIDTH, HEIGHT, SIZE):
        """Creates an instance of a board for Othello given the width, height,
        and size of the board.
        """
        self.name = ""
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.SIZE = SIZE
        self.SPACE_SIZE = WIDTH//SIZE
        self.HOR_LINES = []
        self.VERT_LINES = []
        self.game_pieces = []
        self.board_logic = BoardLogic(WIDTH, HEIGHT, SIZE, self.SPACE_SIZE)
        self.click_count = 0
        self.pieces_on_board = 0
        self.game_manager = GameManager(self.board_logic)
        self.current_color = BLACK
        self.needs_check = True
        self.game_started = False
        self.no_legal_moves = 0
        self.display_turn = True
        self.game_over = False
        self.file_handle_needed = True

    def start_game(self):
        """Displays the first four pieces of the game"""
        x_mid = self.WIDTH // 2
        y_mid = self.HEIGHT // 2
        mid_space = self.SPACE_SIZE / 2
        top_right_space_x = x_mid + mid_space
        top_right_space_y = y_mid - mid_space
        top_left_space_x = x_mid + mid_space
        top_left_space_y = y_mid + mid_space
        bottom_right_space_x = x_mid - mid_space
        bottom_right_space_y = y_mid - mid_space
        bottom_left_space_x = x_mid - mid_space
        bottom_left_space_y = y_mid + mid_space
        self.place_piece(top_right_space_x, top_right_space_y)
        self.place_piece(top_left_space_x, top_left_space_y)
        self.place_piece(bottom_left_space_x, bottom_left_space_y)
        self.place_piece(bottom_right_space_x, bottom_right_space_y)
        self.game_started = True
        for piece in self.game_pieces:
            piece.display()

    def create_lines(self):
        """Draws the game board lines according to the size of the game"""
        for i in range(1, self.SIZE):
            self.VERT_LINES.append((self.WIDTH//self.SIZE)*i)
        for j in range(1, self.SIZE):
            self.HOR_LINES.append((self.HEIGHT//self.SIZE)*j)

    def display(self):
        """Displays the game lines of the board"""
        stroke(0, 0, 10)
        strokeWeight(5)
        self.create_lines()
        for x in self.VERT_LINES:
            line(x, 0, x, self.HEIGHT)
        for y in self.HOR_LINES:
            line(0, y, self.WIDTH, y)
        self.start_game()

    def update_click(self, x, y):
        """Places a new piece on the board if a legal empty space is clicked"""
        if self.game_over:
            return
        self.place_piece(x, y)
        for piece in self.game_pieces:
            piece.display()
        self.game_over = self.game_manager.winning_conditions(
                         self.no_legal_moves,
                         self.game_pieces,
                         self.pieces_on_board)

    def place_piece(self, clicked_x, clicked_y):
        """Places a game piece at the given x and y coordinates"""
        if self.board_logic.point_clicked(clicked_x, clicked_y) is not None:
            x, y = self.board_logic.point_clicked(clicked_x, clicked_y)
            this_point = (x, y)
            self.legal_move(this_point, self.current_color)

    def legal_move(self, this_point, COLOR):
        """Determines whether or a not a clicked upon space is a legal move"""
        if (self.board_logic.space_available(this_point) and
            self.board_logic.adjacent_to_otherpiece(self.game_started,
                                                    this_point, COLOR)):
                self.no_legal_moves = 0
                self.game_pieces.append(GamePiece(this_point[0], this_point[1],
                                                  COLOR, self.SPACE_SIZE))
                self.board_logic.occupy_space(this_point, COLOR)
                self.pieces_on_board += 1
                pieces_to_flip = self.board_logic.target_pieces(COLOR)
                self.flip_pieces(pieces_to_flip, COLOR)
                self.display_turn = True
                if self.current_color == BLACK:
                    self.current_color = WHITE
                else:
                    self.current_color = BLACK
                    self.needs_check = True

        elif not self.board_logic.check_move_possible(self.game_started,
                                                      self.current_color):
            if not self.game_over:
                self.no_legal_moves += 1
                if self.current_color == BLACK:
                    self.current_color = WHITE
                    print("BLACK HAS NO MORE MOVES, WHITE'S TURN")
                else:
                    self.current_color = BLACK
                    print("WHITE HAS NO MORE MOVES, BLACK'S TURN")

    def flip_pieces(self, pieces_to_flip, COLOR):
        """Flips the opponents pieces if a legal move is made"""
        for coordinate in pieces_to_flip:
            for piece in self.game_pieces:
                if (piece.x == coordinate[0] and piece.y == coordinate[1]):
                    piece.COLOR = COLOR

    def file_handling(self, game_pieces):
        """Prints the player's score at the end of the game onto the 'scores.txt' document
        allow with other past scores from previously played games"""
        score = self.game_manager.count_colors(game_pieces)[0]
        my_pair = (str(self.name) + " " + str(score), score)
        pair_score_list = []
        pair_score_list.append(my_pair)
        score_file = open("scores.txt", "r+")
        score_file.readline()
        for line in score_file:
            parse_results = re.findall("\w+", line)
            if len(parse_results) == 0:
                continue
            else:
                pair_score_list.append((line.strip(), int(parse_results[-1])))
        sorted_pairs = sorted(pair_score_list, key=lambda x: x[1],
                              reverse=True)
        score_file.truncate(0)
        score_file.seek(0)
        score_file.write("===== HIGH SCORES =====\n")
        for pair in sorted_pairs:
            score_file.write(pair[0] + "\n")
        score_file.close()
