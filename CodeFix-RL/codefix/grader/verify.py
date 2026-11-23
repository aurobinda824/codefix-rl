
import json
import subprocess
import sys
import tempfile
from pathlib import Path


TASK_TOTALS = {
    "task1": 5,
    "task2": 3,
    "task3": 3,
}


RUNNER_CODE = r'''
import importlib.util
import json
import sys

candidate_path = sys.argv[1]
task_id = sys.argv[2]
cases = []
spec = importlib.util.spec_from_file_location(
    "candidate", candidate_path
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

passed = 0
errors = []


def record(condition, description):
    global passed

    if condition:
        passed += 1
    else:
        errors.append(description)


if task_id == "task1":

    cases = [
        ((0, 0), (3, 4), 7),
        ((-2, 3), (2, -1), 8),
        ((5, 5), (5, 5), 0),
        ((1, 2), (4, 6), 7),
        ((-3, -4), (2, 1), 10),
    ]

    function = getattr(module, "manhattan_distance", None)

    if not callable(function):
        errors.append("Missing manhattan_distance function")

    else:
        for goal, pos, expected in cases:
            try:
                actual = function(goal, pos)
                record(
                    actual == expected,
                    f"Expected {expected}, got {actual}"
                )
            except Exception as exc:
                errors.append(str(exc))


elif task_id == "task2":

    cases = [
        (
            [
                [1, 0, 1],
                [1, 0, 1],
                [1, 0, 1],
            ],
            (0, 1),
            [(1, 1)],
        ),
        (
            [
                [1, 1, 1],
                [0, 0, 0],
                [1, 1, 1],
            ],
            (1, 0),
            [(1, 1)],
        ),
        (
            [
                [1, 0, 1],
                [0, 0, 0],
                [1, 0, 1],
            ],
            (1, 1),
            [(2, 1), (0, 1), (1, 2), (1, 0)],
        ),
    ]

    function = getattr(module, "neighbour", None)

    if not callable(function):
        errors.append("Missing neighbour function")

    else:
        for maze, pos, expected in cases:
            try:
                actual = function(maze, pos)

                if actual is not None:
                    actual = [tuple(p) for p in actual]

                record(
                    actual == expected,
                    f"Expected {expected}, got {actual}"
                )

            except Exception as exc:
                errors.append(str(exc))


elif task_id == "task3":

    cases = [
        (
            [
                [0, 0, 1],
                [1, 0, 1],
                [1, 0, 0],
            ],
            (0, 0),
            (2, 2),
            True,
        ),
        (
            [
                [0, 0, 1],
                [1, 0, 1],
                [0, 0, 0],
            ],
            (0, 0),
            (2, 2),
            True,
        ),
        (
            [
                [0, 1, 0],
                [1, 1, 1],
                [0, 1, 0],
            ],
            (0, 0),
            (2, 2),
            False,
        ),
    ]

    function = getattr(module, "solve_maze", None)

    if not callable(function):
        errors.append("Missing solve_maze function")

    else:
        for maze, start, goal, reachable in cases:
            try:
                path = function(maze, start, goal)

                if not reachable:
                    record(
                        path is None,
                        "Expected None for unreachable goal"
                    )
                    continue

                valid = (
                    isinstance(path, (list, tuple))
                    and len(path) > 0
                )

                if valid:
                    try:
                        path = [tuple(p) for p in path]

                        valid = (
                            path[0] == start
                            and path[-1] == goal
                        )

                        rows = len(maze)
                        cols = len(maze[0])

                        for y, x in path:
                            if not (
                                0 <= y < rows
                                and 0 <= x < cols
                                and maze[y][x] == 0
                            ):
                                valid = False
                                break

                        for a, b in zip(path, path[1:]):
                            if (
                                abs(a[0] - b[0])
                                + abs(a[1] - b[1])
                                != 1
                            ):
                                valid = False
                                break

                    except (TypeError, IndexError):
                        valid = False

                record(valid, "Invalid maze path")

            except Exception as exc:
                errors.append(str(exc))


else:
    errors.append("Unknown task ID")


print(json.dumps({
    "passed": passed,
    "total": len(cases),
    "errors": errors,
}))
'''


def verify_submission(
    task_id: str,
    submission: str,
    timeout: int = 3,
) -> dict:
    """Verify a submission against task-specific test cases."""

    if task_id not in TASK_TOTALS:
        raise ValueError(f"Unknown task: {task_id}")

    total = TASK_TOTALS[task_id]

    if not isinstance(submission, str) or not submission.strip():
        return {
            "task_id": task_id,
            "passed": 0,
            "total": total,
            "reward": 0.0,
            "status": "invalid_submission",
            "details": "Empty or invalid source code",
        }

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        candidate_file = temp_path / "candidate.py"
        runner_file = temp_path / "runner.py"

        candidate_file.write_text(
            submission,
            encoding="utf-8",
        )

        runner_file.write_text(
            RUNNER_CODE,
            encoding="utf-8",
        )

        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "-I",
                    str(runner_file),
                    str(candidate_file),
                    task_id,
                ],
                cwd=temp_dir,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )

            if result.returncode != 0:
                return {
                    "task_id": task_id,
                    "passed": 0,
                    "total": total,
                    "reward": 0.0,
                    "status": "execution_error",
                    "details": result.stderr[-1000:],
                }

            output = json.loads(
                result.stdout.strip().splitlines()[-1]
            )

            passed = output["passed"]

            return {
                "task_id": task_id,
                "passed": passed,
                "total": total,
                "reward": 1.0 if passed == total else 0.0,
                "status": (
                    "passed" if passed == total else "failed"
                ),
                "details": output["errors"],
            }

        except subprocess.TimeoutExpired:
            return {
                "task_id": task_id,
                "passed": 0,
                "total": total,
                "reward": 0.0,
                "status": "timeout",
                "details": "Execution time limit exceeded",
            }

        except (ValueError, IndexError, KeyError) as exc:
            return {
                "task_id": task_id,
                "passed": 0,
                "total": total,
                "reward": 0.0,
                "status": "verifier_error",
                "details": str(exc),
            }

