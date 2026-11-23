
def solve_maze(maze, start, goal):
    rows = len(maze)
    cols = len(maze[0])

    if not (0 <= start[0] < rows and 0 <= start[1] < cols):
        return None

    if not (0 <= goal[0] < rows and 0 <= goal[1] < cols):
        return None

    if maze[start[0]][start[1]] != 0:
        return None

    if maze[goal[0]][goal[1]] != 0:
        return None

    stack = [start]
    visited = {start}
    parent = {start: None}

    directions = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1),
    ]

    while stack:
        current = stack.pop()

        if current == goal:
            path = []
            node = goal

            while node is not None:
                path.append(node)
                node = parent[node]

            return path[::-1]

        y, x = current

        for dy, dx in directions:
            ny = y + dy
            nx = x + dx
            neighbour = (ny, nx)

            if not (0 <= ny < rows and 0 <= nx < cols):
                continue

            if maze[ny][nx] != 0:
                continue

            if neighbour in visited:
                continue

            visited.add(neighbour)
            parent[neighbour] = current
            stack.append(neighbour)

    return None

