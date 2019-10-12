# A game piece for Othello

SIZE_FROM_BORDER = 20


class GamePiece:
    """A class for a game piece in Othello"""
    def __init__(self, x, y, COLOR, SIZE):
        """Creates an instance of the Othello game piece given the x and y coordinate,
        color, and size
        """
        self.x = x
        self.y = y
        self.SIZE = SIZE - SIZE_FROM_BORDER
        self.COLOR = COLOR

    def display(self):
        """Displays the game piece"""
        fill(self.COLOR)
        stroke(0)
        strokeWeight(3)
        ellipse(self.x, self.y, (self.SIZE), (self.SIZE))
