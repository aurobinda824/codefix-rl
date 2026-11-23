
from codefix.env import CodeFixEnv
from codefix.grader.verify import verify_submission
from codefix.agent.baseline import solve_task


def main():
    env = CodeFixEnv(verify_submission)

    for task_id in ("task1", "task2", "task3"):
        observation, info = env.reset(task_id)

        print(f"\nRunning {task_id}")
        print(f"Difficulty: {observation['difficulty']}")

        solution = solve_task(task_id, observation)

        action = {"code": solution}

        observation, reward, terminated, truncated, info = (
            env.step(action)
        )

        verification = info["verification"]

        print(f"Status: {verification['status']}")
        print(f"Tests passed: {verification['passed']}/{verification['total']}")
        print(f"Reward: {reward}")


if __name__ == "__main__":
    main()

