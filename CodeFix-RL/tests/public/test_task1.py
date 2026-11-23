from benchmark.workspaces.task1.ai import manhattan_distance


def test_horizontal_distance():
    assert manhattan_distance((0, 0), (0, 5)) == 5


def test_vertical_distance():
    assert manhattan_distance((0, 0), (4, 0)) == 4

def test_diagonal_distance():
    assert manhattan_distance((0, 0), (3, 4)) == 7
