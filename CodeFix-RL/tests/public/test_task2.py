from benchmark.workspaces.task2.ai import neighbour


def test_four_accessible_neighbours():
    maze = [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
    ]

    assert neighbour(maze, (1, 1)) == []


def test_accessible_right_neighbour():
    maze = [
        [1, 1, 1],
        [1, 0, 0],
        [1, 1, 1],
    ]

    assert neighbour(maze, (1, 1)) == [(1, 2)]
