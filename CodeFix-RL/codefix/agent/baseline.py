
def solve_task(task_id, observation):
    """
    Deterministic baseline for validating environment mechanics.
    These solutions are test fixtures, not an AI agent.
    """

    if task_id == "task1":
        return """
def manhattan_distance(goal, pos):
    return abs(goal[0] - pos[0]) + abs(goal[1] - pos[1])
"""

    if task_id == "task2":
        return """
def neighbour(maze, pos):
    y, x = pos
    rows = len(maze)
    cols = len(maze[0])
    result = []

    for dy, dx in [
        (1, 0), (-1, 0), (0, 1), (0, -1)
    ]:
        ny, nx = y + dy, x + dx

        if 0 <= ny < rows and 0 <= nx < cols:
            if maze[ny][nx] == 0:
                result.append((ny, nx))

    return result
"""

    if task_id == "task3":
        return """
from collections import deque

def solve_maze(maze, start, goal):
    rows, cols = len(maze), len(maze[0])

    if not (0 <= start[0] < rows and 0 <= start[1] < cols):
        return None

    if not (0 <= goal[0] < rows and 0 <= goal[1] < cols):
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

        for dy, dx in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nxt = (y + dy, x + dx)
            ny, nx = nxt

            if (0 <= ny < rows and 0 <= nx < cols
                    and maze[ny][nx] == 0
                    and nxt not in parent):
                parent[nxt] = current
                queue.append(nxt)

    return None
"""

    raise ValueError(f"Unknown task: {task_id}")

