from codefix.grader.verify import verify_submission
from codefix.grader.reward import calculate_reward


BROKEN_CODE = """
def manhattan_distance(goal, pos):
    dist = (
        (goal[0] - pos[0]) ** 2
        + (goal[1] - pos[1]) ** 2
    ) ** 0.5
    return round(dist, 2)
"""


FIXED_CODE = """
def manhattan_distance(goal, pos):
    return abs(goal[0] - pos[0]) + abs(goal[1] - pos[1])
"""


def test_broken_submission():
    result = verify_submission("task1", BROKEN_CODE)

    assert result["status"] == "failed"
    assert result["reward"] == 0.0


def test_fixed_submission():
    result = verify_submission("task1", FIXED_CODE)

    assert result["status"] == "passed"
    assert result["reward"] == 1.0


def test_reward_calculation():
    result = verify_submission("task1", FIXED_CODE)

    assert calculate_reward(result) == 1.0
