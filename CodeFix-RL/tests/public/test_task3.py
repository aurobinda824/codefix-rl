from benchmark.workspaces.task3.solver import solve_maze


def test_simple_path():
    maze = [
        [0, 0, 1],
        [1, 0, 1],
        [1, 0, 0],
    ]

    path = solve_maze(maze, (0, 0), (2, 2))

    assert path is not None
    assert path[0] == (0, 0)
    assert path[-1] == (2, 2)


def test_path_avoids_walls():
    maze = [
        [0, 0, 0],
        [1, 1, 0],
        [0, 0, 0],
    ]

    path = solve_maze(maze, (0, 0), (2, 2))

    assert path is not None

    for y, x in path:
        assert maze[y][x] == 0
