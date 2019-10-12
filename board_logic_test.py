from board import Board
from board_logic import BoardLogic


def test_constructor():
    game_board = Board(640, 640, 8)
    board_logic = game_board.board_logic
    assert board_logic.WIDTH == 640
    assert board_logic.HEIGHT == 640
    assert board_logic.SIZE == 8
    game_board = Board(640, 640, 4)
    board_logic = game_board.board_logic
    assert board_logic.WIDTH == 640
    assert board_logic.HEIGHT == 640
    assert board_logic.SIZE == 4
    game_board = Board(1000, 640, 8)
    board_logic = game_board.board_logic
    assert board_logic.WIDTH == 1000
    assert board_logic.HEIGHT == 640
    assert board_logic.SIZE == 8
    game_board = Board(640, 1000, 8)
    board_logic = game_board.board_logic
    assert board_logic.WIDTH == 640
    assert board_logic.HEIGHT == 1000
    assert board_logic.SIZE == 8


def test_create_points():
    game_board = Board(640, 640, 8)
    board_logic = game_board.board_logic
    clickable_points = 0
    for row in board_logic.click_points:
        for item in row:
            clickable_points += 1
    assert clickable_points == 64
    board_positions = 0
    for row in board_logic.board_position:
        for item in row:
            board_positions += 1
    assert board_positions == 64

    game_board = Board(640, 640, 4)
    board_logic = game_board.board_logic
    clickable_points = 0
    for row in board_logic.click_points:
        for item in row:
            clickable_points += 1
    assert clickable_points == 16
    board_positions = 0
    for row in board_logic.board_position:
        for item in row:
            board_positions += 1
    assert board_positions == 16


def test_point_clicked():
    game_board = Board(640, 640, 8)
    board_logic = game_board.board_logic
    a = board_logic.point_clicked(38, 42)
    b = (40, 40)
    assert a == b

    a = board_logic.point_clicked(0, 0)
    b = None
    assert a == b

    a = board_logic.point_clicked(640, 640)
    b = None
    assert a == b


def test_piece_count():
    game_board = Board(640, 640, 8)
    board_logic = game_board.board_logic
    assert board_logic.piece_count() == 64

    game_board = Board(640, 640, 4)
    board_logic = game_board.board_logic
    assert board_logic.piece_count() == 16

    game_board = Board(640, 640, 10)
    board_logic = game_board.board_logic
    assert board_logic.piece_count() == 100

    game_board = Board(640, 640, 20)
    board_logic = game_board.board_logic
    assert board_logic.piece_count() == 400


def test_matrix_indexes():
    game_board = Board(640, 640, 8)
    board_logic = game_board.board_logic
    a = board_logic.matrix_indexes((40, 40))
    b = (0, 0)
    assert a == b

    a = board_logic.matrix_indexes((120, 40))
    b = (1, 0)
    assert a == b

    a = board_logic.matrix_indexes((40, 120))
    b = (0, 1)
    assert a == b

    a = board_logic.matrix_indexes((600, 600))
    b = (7, 7)
    assert a == b


def test_space_available():
    game_board = Board(640, 640, 8)
    board_logic = game_board.board_logic
    a = board_logic.space_available((40, 40))
    b = True
    assert a == b
    game_board.place_piece(40, 40)
    a = board_logic.space_available((40, 40))
    b = False
    assert a == b

    a = board_logic.space_available((120, 40))
    b = True
    assert a == b
    game_board.place_piece(120, 40)
    a = board_logic.space_available((120, 40))
    b = False
    assert a == b

    a = board_logic.space_available((40, 120))
    b = True
    assert a == b
    game_board.place_piece(40, 120)
    a = board_logic.space_available((40, 120))
    b = False
    assert a == b