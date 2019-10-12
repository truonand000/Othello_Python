# A board logisitics class for an Othello game

BLACK = 0
WHITE = 255


class BoardLogic:
    """A class for the Othello board that controls game logistics"""

    def __init__(self, WIDTH, HEIGHT, SIZE, SPACE_SIZE):
        """Creates an instance of the BoardLogic given the width, heigh size, and
        space size of the board.
        """
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.SIZE = SIZE
        self.SPACE_SIZE = SPACE_SIZE
        self.CLICK_RADIUS = (SPACE_SIZE/2) - 10
        self.click_points = []
        self.board_position = []
        self.pieces_to_flip = []
        self.possible_directions = {"RIGHT": (1, 0),
                                    "LEFT": (-1, 0),
                                    "DOWN": (0, 1),
                                    "UP": (0, -1),
                                    "RIGHT_DOWN": (1, 1),
                                    "LEFT_UP": (-1, -1),
                                    "RIGHT_UP": (1, -1),
                                    "LEFT_DOWN": (-1, 1)}
        self.create_points()

    def create_points(self):
        """Creates clickable points and board positions matrix"""
        for y in range(self.SIZE):
            new_row = []
            for x in range(self.SIZE):
                new_row.append(((self.SPACE_SIZE/2) +
                                (self.SPACE_SIZE * x),
                                (self.SPACE_SIZE/2) +
                                (self.SPACE_SIZE * y)))
            self.click_points.append(new_row)
        # Sets up the board positions matrix to keep track of occupied
        # poistions
        # Size of matrix is larger than actual board to nullify difficulty with
        # edge cases
        for y in range(self.SIZE):
            new_position_row = []
            for x in range(self.SIZE):
                new_position_row.append(None)
            self.board_position.append(new_position_row)

    def click_points_display(self):
        """Displays the location of click points
        Meant to be used for debugging
        """
        stroke(0)
        for grid_point in self.click_points:
            point(grid_point[0], grid_point[1])

    def point_clicked(self, click_X, click_Y):
        """Returns the coordinate of the clickable point upon mouse click.
        Expands the clickable region.
        """
        for row in self.click_points:
            for coordinate in row:
                if abs(click_X - coordinate[0]) <= self.CLICK_RADIUS and \
                        abs(click_Y - coordinate[1]) <= self.CLICK_RADIUS:
                    return coordinate

    def piece_count(self):
        """Calculates a static value that acts as the maximum pieces that can
        be placed on the board"""
        total_points = 0
        for row in self.click_points:
            total_points += len(row)
        return total_points

    def matrix_indexes(self, this_point):
        """Takes the coordinates of a point and returns indexes for
        the corresponding position in the board_position matrix"""
        for y in range(len(self.click_points)):
            for x in range(len(self.click_points[0])):
                if this_point == self.click_points[y][x]:
                    return x, y

    def matrix_to_coord(self, x, y):
        """Converts matrix to coordinates on actual board"""
        return self.click_points[y][x]

    def space_available(self, this_point):
        """Checks if the space is avaiable for piece placement"""
        x, y = self.matrix_indexes(this_point)
        if self.board_position[y][x] is None:
            return True
        else:
            return False

    def occupy_space(self, this_point, COLOR):
        """Marks the position down as occupied by a ceratin color"""
        x, y = self.matrix_indexes(this_point)
        if COLOR == BLACK:
            self.board_position[y][x] = BLACK
        if COLOR == WHITE:
            self.board_position[y][x] = WHITE

    def adjacent_to_otherpiece(self, game_started, this_point, COLOR):
        """Determines if move is legal and returns how many pieces are flipped
        if a particular position is chosen for piece placement"""
        if game_started:
            # print("PIECE SEARCHING FOR OTHER OPPOSITE PIECES")
            x, y = self.matrix_indexes(this_point)
            flippable_pieces = 0
            for direction in self.possible_directions:
                x_add = self.possible_directions[direction][0]
                y_add = self.possible_directions[direction][1]
                temp_x = x + x_add
                temp_y = y + y_add
                if (temp_x > self.SIZE - 1 or temp_y > self.SIZE - 1 or
                        temp_x < 0 or temp_y < 0):
                    continue
                elif self.board_position[temp_y][temp_x] is None:
                    continue
                elif self.board_position[temp_y][temp_x] != COLOR:
                    flippable_pieces += self.sandwiches_opponent(this_point,
                                                                 direction,
                                                                 COLOR)
                    # print("Detected", key)

            return flippable_pieces
        else:
            return 1

    def sandwiches_opponent(self, this_point, direction, COLOR):
        """Determines whether or not a particular move 'sandwiches' an opponents
        pieces between the player's pieces"""
        x, y = self.matrix_indexes(this_point)
        x_add = 0
        y_add = 0
        list_of_flips = []
        while True:
            x_add += self.possible_directions[direction][0]
            y_add += self.possible_directions[direction][1]
            temp_x = x + x_add
            temp_y = y + y_add
            list_of_flips.append((temp_x, temp_y))
            if (temp_x > self.SIZE - 1 or temp_y > self.SIZE - 1 or
                    temp_x < 0 or temp_y < 0):
                return 0
            elif self.board_position[temp_y][temp_x] is None:
                # print("NONE")
                return 0
            elif self.board_position[temp_y][temp_x] == COLOR:
                self.pieces_to_flip.extend(list_of_flips[:-1])
                return len(list_of_flips[:-1])

    def target_pieces(self, COLOR):
        """Returns a list of coordinates of opponent pieces to flip"""
        coordinate_list = []
        for coordinate in self.pieces_to_flip:
            x, y = coordinate
            self.board_position[y][x] = COLOR
            x, y = self.click_points[y][x]
            coordinate_list.append((x, y))
        # print(coordinate_list)
        self.pieces_to_flip = []
        return coordinate_list

    def check_move_possible(self, game_started, COLOR):
        """Checks to see if there is any legal move that can be made at all"""
        available_moves = 0
        for y in range(len(self.board_position)):
            for x in range(len(self.board_position[0])):
                if (self.board_position[y][x] is None and
                    self.adjacent_to_otherpiece(game_started,
                                                self.matrix_to_coord(x, y),
                                                COLOR)):
                    available_moves += 1
                self.pieces_to_flip = []
        if available_moves > 0:
            return True
        else:
            return False
