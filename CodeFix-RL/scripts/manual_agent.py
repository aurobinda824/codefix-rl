
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from codefix.env import CodeFixEnv
from codefix.grader.verify import verify_submission


def main():
    parser = argparse.ArgumentParser(
        description="Manually evaluate a code repair submission."
    )

    parser.add_argument(
        "--task",
        required=True,
        choices=["task1", "task2", "task3"],
    )

    parser.add_argument(
        "--submission",
        required=True,
        help="Path to the submitted Python file.",
    )

    parser.add_argument("--attempt", type=int, default=1)

    parser.add_argument(
        "--method",
        default="manual",
        choices=["manual", "ai_agent"],
    )

    args = parser.parse_args()

    submission_path = Path(args.submission).resolve()

    if not submission_path.is_file():
        raise FileNotFoundError(
            f"Submission file not found: {submission_path}"
        )

    submission = submission_path.read_text(encoding="utf-8")

    env = CodeFixEnv(verifier=verify_submission)

    initial_observation, _ = env.reset(args.task)

    # Preserve task information before calling env.step().
    task_id = initial_observation["task_id"]
    difficulty = initial_observation["difficulty"]

    print("\n" + "=" * 60)
    print("CODEFIX-RL EVALUATION")
    print("=" * 60)

    print(f"\nTask: {task_id}")
    print(f"Difficulty: {difficulty}")
    print(f"Method: {args.method}")
    print(f"Attempt: {args.attempt}")

    print("\nTASK DESCRIPTION")
    print(initial_observation["description"])

    print("\nBROKEN SOURCE CODE")
    print("-" * 60)
    print(initial_observation["source_code"])
    print("-" * 60)

    print("\nSUBMITTED SOURCE CODE")
    print("-" * 60)
    print(submission)
    print("-" * 60)

    _, reward, terminated, truncated, info = env.step(
        {"code": submission}
    )

    verification = info["verification"]

    result = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "task_id": task_id,
        "difficulty": difficulty,
        "attempt": args.attempt,
        "method": args.method,
        "submission": str(submission_path),
        "passed": verification["passed"],
        "total": verification["total"],
        "reward": reward,
        "status": verification["status"],
    }

    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)

    results_file = results_dir / "manual_runs.jsonl"

    with results_file.open("a", encoding="utf-8") as file:
        file.write(json.dumps(result) + "\n")

    print("\nEVALUATION RESULT")
    print("-" * 60)
    print(f"Status: {verification['status']}")
    print(
        f"Tests passed: "
        f"{verification['passed']}/{verification['total']}"
    )
    print(f"Reward: {reward}")
    print(f"Episode terminated: {terminated}")
    print(f"Episode truncated: {truncated}")
    print(f"\nRecorded in: {results_file}")


if __name__ == "__main__":
    main()

