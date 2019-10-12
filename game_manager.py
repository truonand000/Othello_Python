# A game manager class for Othello

BLACK = 0
WHITE = 255


class GameManager:
    """A Game Manager class for Othello"""

    def __init__(self, board_logic):
        """Creates an instances of GameManager given the game grid"""
        self.player1_win = False
        self.player2_win = False
        self.total_piece_count = board_logic.piece_count()

    def winning_conditions(self, no_legal_moves, game_pieces, pieces_on_board):
        """Determines and displays the winner of the game"""
        game_over = False
        current_piece_count = pieces_on_board
        if current_piece_count == self.total_piece_count:
            game_over = True
            self.end_game_message(game_pieces, pieces_on_board)
            print("END GAME")
        elif no_legal_moves == 2:
            game_over = True
            self.end_game_message(game_pieces, pieces_on_board)
            print("END GAME")
        return game_over

    def end_game_message(self, game_pieces, pieces_on_board):
        """Displays the end game message that shows up when one of the players win
        or if the game is a tie"""
        black_count, white_count = self.count_colors(game_pieces)
        if black_count > white_count:
            self.player1_win = True
            winner = "Black"
            win_score = black_count
            lose_score = white_count
        elif white_count > black_count:
            self.player2_win = True
            winner = "White"
            win_score = white_count
            lose_score = black_count
        else:
            message = "TIE, {0} - {1}".format(black_count, white_count)
        if self.player1_win or self.player2_win:
            message = "{} Wins, {} - {}".format(winner, win_score,
                                                lose_score)
        self.display_endgame_mssg(message, black_count, white_count)

    def count_colors(self, game_pieces):
        """Returns number of black and white game pieces currently
        on the board"""
        black_count = 0
        white_count = 0
        for piece in game_pieces:
            if piece.COLOR == BLACK:
                black_count += 1
            elif piece.COLOR == WHITE:
                white_count += 1
        return black_count, white_count

    def update_piece_count(self, used_points):
        """Return the number of pieces on the board"""
        return used_points

    def display_endgame_mssg(self, message, black_count, white_count):
        """Displays the end game message"""
        textSize(32)
        tw = textWidth(message)
        ta = textAscent()
        td = textDescent()

        stroke(0)
        strokeWeight(4)
        fill(255)
        rectMode(CENTER)
        rect(320, 320, tw + 20, ta + td + 20)

        fill(50)
        textAlign(CENTER, CENTER)
        text(message, 320, 320)
