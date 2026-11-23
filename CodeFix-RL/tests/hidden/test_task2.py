from ai import neighbour


def test_top_boundary():
    maze = [
        [0, 1, 1],
        [0, 0, 1],
        [1, 1, 1],
    ]

    assert neighbour(maze, (0, 1)) == []


def test_left_boundary():
    maze = [
        [1, 1, 1],
        [0, 1, 1],
        [1, 1, 1],
    ]

    assert neighbour(maze, (1, 0)) == []


def test_all_directions():
    maze = [
        [1, 0, 1],
        [0, 0, 0],
        [1, 0, 1],
    ]

    assert set(neighbour(maze, (1, 1))) == {
        (0, 1), (2, 1), (1, 0), (1, 2)
    }
