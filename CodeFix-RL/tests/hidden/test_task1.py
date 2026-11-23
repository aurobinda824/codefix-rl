from ai import manhattan_distance


def test_diagonal_distance():
    assert manhattan_distance((0, 0), (3, 4)) == 7


def test_negative_coordinates():
    assert manhattan_distance((-2, 3), (2, -1)) == 8


def test_same_position():
    assert manhattan_distance((5, 5), (5, 5)) == 0
