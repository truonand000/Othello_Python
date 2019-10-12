from board import Board


def test_constructor():
    game_board = Board(640, 640, 8)
    assert game_board.WIDTH == 640
    assert game_board.HEIGHT == 640
    assert game_board.SIZE == 8


def test_create_lines():
    game_board = Board(640, 640, 8)
    game_board.create_lines()
    assert game_board.VERT_LINES == [80, 160, 240, 320, 400, 480, 560]
    assert game_board.HOR_LINES == [80, 160, 240, 320, 400, 480, 560]


def test_place_piece():
    # Test that place piece adds game pieces to board
    game_board = Board(640, 640, 8)
    assert len(game_board.game_pieces) == 0
    game_board.place_piece(40, 40)
    assert len(game_board.game_pieces) == 1
    game_board.place_piece(120, 40)
    assert len(game_board.game_pieces) == 2
    game_board.place_piece(200, 40)
    assert len(game_board.game_pieces) == 3

    # Test that board won't place a new piece in the same place
    game_board.place_piece(40, 40)
    assert len(game_board.game_pieces) == 3
    game_board.place_piece(120, 40)
    assert len(game_board.game_pieces) == 3
    game_board.place_piece(200, 40)
    assert len(game_board.game_pieces) == 3

    # Test that off-board clicks won't place a new piece
    game_board.place_piece(-40, -40)
    game_board.place_piece(-1, -1)
    game_board.place_piece(650, 650)
    game_board.place_piece(40, 650)
    game_board.place_piece(650, 40)
    assert len(game_board.game_pieces) == 3

    # Test that placing a piece at every possible spot should
    # fill up all 64 spots on an 8x8 board.
    game_board = Board(640, 640, 8)
    for y in range(40, 640, 80):
        for x in range(40, 640, 80):
            game_board.place_piece(x, y)
    assert len(game_board.game_pieces) == 64
