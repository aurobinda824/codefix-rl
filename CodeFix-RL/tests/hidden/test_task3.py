from solver import solve_maze


def is_valid_path(maze, start, goal, path):
    if path is None:
        return False

    if path[0] != start or path[-1] != goal:
        return False

    rows = len(maze)
    cols = len(maze[0])

    for y, x in path:
        if not (0 <= y < rows and 0 <= x < cols):
            return False

        if maze[y][x] != 0:
            return False

    for a, b in zip(path, path[1:]):
        if abs(a[0] - b[0]) + abs(a[1] - b[1]) != 1:
            return False

    return True


def test_requires_backtracking():
    maze = [
        [0, 0, 1],
        [1, 0, 1],
        [0, 0, 0],
    ]

    start = (0, 0)
    goal = (2, 2)

    path = solve_maze(maze, start, goal)

    assert is_valid_path(maze, start, goal, path)


def test_unreachable_goal():
    maze = [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0],
    ]

    assert solve_maze(maze, (0, 0), (2, 2)) is None
