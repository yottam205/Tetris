import pytest
import copy
import layout
from main import check_lines, convert_shape_format, Tetromino, is_collision, spawn_new_tetromino, lock_tetromino


test_board = [[0 for _ in range(10)] for _ in range(20)]
test_tetromino = Tetromino(shape_index=0, color=layout.COLORS[1]) 

def test_check_lines_no_clear():
    board = copy.deepcopy(test_board)
    lines_cleared, new_board = check_lines(board)
    assert lines_cleared == 0
    assert new_board == board

def test_check_lines_clear():
    board = copy.deepcopy(test_board)
    board[19] = [1 for _ in range(10)]  
    lines_cleared, new_board = check_lines(board)
    assert lines_cleared == 1
    assert new_board[-1] == [0 for _ in range(10)]


def test_convert_shape_format():
    test_tetromino.shape = [[0, 1, 0], [1, 1, 1]]
    test_tetromino.x = 4
    test_tetromino.y = 1
    expected_positions = [(5, 1), (4, 2), (5, 2), (6, 2)]  
    assert convert_shape_format(test_tetromino) == expected_positions

def test_spawn_new_tetromino():
    new_tetromino = spawn_new_tetromino()
    assert isinstance(new_tetromino, Tetromino)
    assert 0 <= new_tetromino.shape_index < len(layout.SHAPES)
    assert new_tetromino.color in layout.COLORS

def test_is_collision_false():
    test_tetromino.x, test_tetromino.y = 5, 0
    assert not is_collision(test_tetromino, test_board)

def test_is_collision_true():
    test_tetromino.x, test_tetromino.y = 5, 0
    test_tetromino.shape = [[1]] 
    test_board[0][5] = 1  
    assert is_collision(test_tetromino, test_board)

def test_lock_tetromino():
    test_tetromino.x, test_tetromino.y = 5, 0
    test_tetromino.shape = [[1]]
    lock_tetromino(test_tetromino, test_board)
    color_index = layout.COLORS.index(test_tetromino.color)
    assert test_board[0][5] == color_index

