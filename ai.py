WHITE = 255
BLACK = 0
CHECK_X = 360
CHECK_Y = 280


class AI:

    def __init__(self, click_points, SIZE):
        self.possible_moves = []
        self.click_points = click_points
        self.board_size = SIZE
        self.COLOR = WHITE

    def play_turn(self, board_logic):
        self.find_move(board_logic)
        coordinate = self.play_best_move(board_logic)
        board_logic.pieces_to_flip = []
        self.possible_moves = []
        return coordinate

    def find_move(self, board_logic):
        available_moves = 0
        for y in range(self.board_size):
            for x in range(self.board_size):
                if (board_logic.space_available(self.click_points[y][x]) and
                        board_logic.adjacent_to_otherpiece(True,
                                                           self.click_points[y][x],
                                                           self.COLOR)):
                    available_moves += 1
                    piece_count = board_logic.adjacent_to_otherpiece(True,
                                  self.click_points[y][x],
                                  self.COLOR)
                    corner = False
                    if (y == self.board_size - 1 or
                            x == self.board_size - 1 or
                            y == 0 or
                            x == 0):
                        corner = True
                    self.possible_moves.append((piece_count,
                                                corner,
                                                self.click_points[y][x]))

    def play_best_move(self, board_logic):
        most_flips = (10, False, (CHECK_X, CHECK_Y))
        for item in self.possible_moves:
            if item[1]:
                return item[2]
            elif item[0] < most_flips[0]:
                most_flips = item
        return most_flips[2]
