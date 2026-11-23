
import pytest

from codefix.env import CodeFixEnv


def fake_verifier(task_id, submission):
    """Temporary verifier for testing environment mechanics."""

    return {
        "status": "passed",
        "reward": 1.0,
        "task_id": task_id,
    }


def test_reset_task1():
    env = CodeFixEnv(fake_verifier)

    observation, info = env.reset("task1")

    assert observation["task_id"] == "task1"
    assert observation["difficulty"] == "easy"
    assert "manhattan_distance" in observation["source_code"]


def test_reset_all_tasks():
    env = CodeFixEnv(fake_verifier)

    for task_id in ("task1", "task2", "task3"):
        observation, _ = env.reset(task_id)
        assert observation["task_id"] == task_id


def test_step():
    env = CodeFixEnv(fake_verifier)
    env.reset("task1")

    action = {
        "code": """
def manhattan_distance(goal, pos):
    return abs(goal[0] - pos[0]) + abs(goal[1] - pos[1])
"""
    }

    observation, reward, terminated, truncated, info = env.step(action)

    assert reward == 1.0
    assert terminated is True
    assert truncated is False
    assert observation["status"] == "submitted"
    assert info["verification"]["status"] == "passed"


def test_invalid_task():
    env = CodeFixEnv(fake_verifier)

    with pytest.raises(ValueError):
        env.reset("task99")


def test_step_without_reset():
    env = CodeFixEnv(fake_verifier)

    with pytest.raises(RuntimeError):
        env.step({"code": "print('hello')"})


def test_no_second_submission():
    env = CodeFixEnv(fake_verifier)
    env.reset("task1")

    env.step({"code": "def manhattan_distance(a, b): return 0"})

    with pytest.raises(RuntimeError):
        env.step({"code": "print('second attempt')"})

