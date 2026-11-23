def neighbour(maze, pos):
    y, x = pos
    re = []

    if maze[y + 1][x] == 0:
        re.append((y + 1, x))

    if maze[y - 1][x] == 0:
        re.append((y - 1, x))

    if maze[y][x + 1] == 0:
        re.append((y, x + 1))

    if maze[y][x - 1] == 0:
        re.append((y, x - 1))

    return re
