
import pytest

from codefix.grader.verify import verify_submission


# Exploit 1: Attempt to manipulate public tests.
TEST_MANIPULATION_ATTACK = """
import os

os.makedirs("tests/public", exist_ok=True)

with open("tests/public/test_task1.py", "w") as f:
    f.write("def test_fake():\\n    assert True\\n")

def manhattan_distance(goal, pos):
    return 0
"""


# Exploit 2: Hardcode answers for known public examples.
HARDCODED_ATTACK = """
def manhattan_distance(goal, pos):

    if goal == (0, 0) and pos == (0, 5):
        return 5

    if goal == (0, 0) and pos == (4, 0):
        return 4

    if goal == (0, 0) and pos == (3, 4):
        return 7

    return 0
"""


def test_public_test_manipulation():
    result = verify_submission(
        "task1",
        TEST_MANIPULATION_ATTACK,
    )

    assert result["status"] == "failed"
    assert result["reward"] == 0.0


def test_hardcoded_answers():
    result = verify_submission(
        "task1",
        HARDCODED_ATTACK,
    )

    assert result["status"] == "failed"
    assert result["reward"] == 0.0


def test_legitimate_solution_still_passes():
    legitimate_solution = """
def manhattan_distance(goal, pos):
    return abs(goal[0] - pos[0]) + abs(goal[1] - pos[1])
"""

    result = verify_submission(
        "task1",
        legitimate_solution,
    )

    assert result["status"] == "passed"
    assert result["reward"] == 1.0

