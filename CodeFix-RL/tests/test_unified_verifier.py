
from codefix.grader.verify import verify_submission


TASK1_FIXED = """
def manhattan_distance(goal, pos):
    return abs(goal[0] - pos[0]) + abs(goal[1] - pos[1])
"""


TASK2_FIXED = """
def neighbour(maze, pos):
    y, x = pos
    rows = len(maze)
    cols = len(maze[0])
    result = []

    directions = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1),
    ]

    for dy, dx in directions:
        ny = y + dy
        nx = x + dx

        if 0 <= ny < rows and 0 <= nx < cols:
            if maze[ny][nx] == 0:
                result.append((ny, nx))

    return result
"""


TASK3_FIXED = """
from collections import deque


def solve_maze(maze, start, goal):
    rows = len(maze)
    cols = len(maze[0])

    if not (
        0 <= start[0] < rows
        and 0 <= start[1] < cols
        and 0 <= goal[0] < rows
        and 0 <= goal[1] < cols
    ):
        return None

    if maze[start[0]][start[1]] != 0:
        return None

    if maze[goal[0]][goal[1]] != 0:
        return None

    queue = deque([start])
    parent = {start: None}

    while queue:
        current = queue.popleft()

        if current == goal:
            path = []

            while current is not None:
                path.append(current)
                current = parent[current]

            return path[::-1]

        y, x = current

        for dy, dx in [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
        ]:
            nxt = (y + dy, x + dx)
            ny, nx = nxt

            if (
                0 <= ny < rows
                and 0 <= nx < cols
                and maze[ny][nx] == 0
                and nxt not in parent
            ):
                parent[nxt] = current
                queue.append(nxt)

    return None
"""


def test_task1_verification():
    result = verify_submission("task1", TASK1_FIXED)

    assert result["status"] == "passed"
    assert result["reward"] == 1.0


def test_task2_verification():
    result = verify_submission("task2", TASK2_FIXED)

    assert result["status"] == "passed"
    assert result["reward"] == 1.0


def test_task3_verification():
    result = verify_submission("task3", TASK3_FIXED)

    assert result["status"] == "passed"
    assert result["reward"] == 1.0


def test_unknown_task():
    import pytest

    with pytest.raises(ValueError):
        verify_submission("task99", "print('hello')")

