def neighbour(maze, pos):
    y, x = pos
    height = len(maze)
    width = len(maze[0])

    result = []

    directions = [
        (0, 1),
        (0, -1),
        (1, 0),
        (-1, 0),
    ]

    for dy, dx in directions:
        ny = y + dy
        nx = x + dx

        if 0 <= ny < height and 0 <= nx < width:
            if maze[ny][nx] == 0:
                result.append((ny, nx))

    return result
