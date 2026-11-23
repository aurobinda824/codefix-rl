def manhattan_distance(goal, pos):
    dist = (
        (goal[0] - pos[0]) ** 2
        + (goal[1] - pos[1]) ** 2
    ) ** 0.5

    return round(dist, 2)
