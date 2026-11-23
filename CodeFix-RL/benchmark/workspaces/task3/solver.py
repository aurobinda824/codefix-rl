def solve_maze(maze, start, goal):
    """
    Return a path from start to goal.
    maze: 0 = walkable, 1 = wall
    """

    stack = [start]
    explored = [start]

    while stack:
        current = stack.pop()

        if current == goal:
            return explored

        y, x = current

        neighbours = [
            (y + 1, x),
            (y - 1, x),
            (y, x + 1),
            (y, x - 1),
        ]

        for neighbour in neighbours:
            ny, nx = neighbour

            if maze[ny][nx] == 0 and neighbour not in explored:
                explored.append(neighbour)
                stack.append(neighbour)

    return None
