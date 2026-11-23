
from pathlib import Path


class CodeFixEnv:
    """
    A minimal code-repair environment.

    The agent receives broken source code and submits a
    repaired implementation. An independent verifier
    determines the reward.
    """

    TASKS = {
        "task1": {
            "difficulty": "easy",
            "description": (
                "Fix manhattan_distance so that it calculates "
                "the Manhattan distance between two coordinates."
            ),
            "file": "task1/ai.py",
        },
        "task2": {
            "difficulty": "medium",
            "description": (
                "Fix neighbour so that it returns only valid "
                "accessible adjacent cells without crossing "
                "grid boundaries."
            ),
            "file": "task2/ai.py",
        },
        "task3": {
            "difficulty": "hard",
            "description": (
                "Fix solve_maze so that it returns a valid path "
                "from start to goal without crossing walls. "
                "Return None if no path exists."
            ),
            "file": "task3/solver.py",
        },
    }

    def __init__(self, verifier, workspace=None):
        self.verifier = verifier

        project_root = Path(__file__).resolve().parents[1]

        self.workspace = (
            Path(workspace)
            if workspace is not None
            else project_root / "benchmark" / "workspaces"
        )

        self.task_id = None
        self.done = False

    def reset(self, task_id: str):
        """Start a new task and return its observation."""

        if task_id not in self.TASKS:
            raise ValueError(f"Unknown task: {task_id}")

        task = self.TASKS[task_id]
        source_path = self.workspace / task["file"]

        if not source_path.is_file():
            raise FileNotFoundError(source_path)

        self.task_id = task_id
        self.done = False

        observation = {
            "task_id": task_id,
            "difficulty": task["difficulty"],
            "description": task["description"],
            "source_code": source_path.read_text(
                encoding="utf-8"
            ),
        }

        info = {
            "status": "initialized",
        }

        return observation, info

    def step(self, action):
        """
        Submit a repaired source file.

        Action format:
            {"code": "<complete Python source code>"}
        """

        if self.task_id is None:
            raise RuntimeError("Call reset() before step().")

        if self.done:
            raise RuntimeError(
                "Episode finished. Call reset() before stepping again."
            )

        if not isinstance(action, dict):
            raise TypeError("Action must be a dictionary.")

        submission = action.get("code")

        if not isinstance(submission, str) or not submission.strip():
            raise ValueError("Action must contain non-empty source code.")

        verification = self.verifier(
            self.task_id,
            submission,
        )

        reward = float(verification["reward"])

        self.done = True

        observation = {
            "task_id": self.task_id,
            "status": "submitted",
        }

        terminated = True
        truncated = False

        info = {
            "verification": verification,
        }

        return observation, reward, terminated, truncated, info

