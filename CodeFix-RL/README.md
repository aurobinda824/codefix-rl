# CodeFix-RL

A lightweight code-repair environment inspired by the OpenAI Gym interface, built using real-world Python code from the MazeSolver project.

CodeFix-RL presents broken code to an agent or human, accepts a corrected implementation, verifies the submission, and returns a reward.

## Features

- Three code-repair tasks with different difficulty levels.
- Structured observation and action interface.
- Automated submission verification.
- Binary reward mechanism.
- Subprocess-based execution of candidate code.
- Anti-gaming experiments.
- Manual evaluation support.
- JSONL-based experiment result logging.

## Project Structure

```text
CodeFix-RL/
├── benchmark/
│   ├── reference/
│   └── workspaces/
│       ├── task1/
│       ├── task2/
│       └── task3/
├── codefix/
│   ├── agent/
│   ├── grader/
│   ├── tasks/
│   └── env.py
├── scripts/
│   ├── run.py
│   ├── grade.py
│   ├── run_agent.py
│   └── manual_agent.py
├── submissions/
├── tests/
│   ├── public/
│   ├── hidden/
│   ├── test_environment.py
│   ├── test_grader.py
│   ├── test_unified_verifier.py
│   └── test_anti_gaming.py
├── results/
├── requirements.txt
├── pytest.ini
├── scope.md
└── results.md
```

## Tasks

| Task | Difficulty | Description |
|---|---|---|
| Task 1 | Easy | Correct the Manhattan distance calculation. |
| Task 2 | Medium | Implement boundary-safe maze neighbour detection. |
| Task 3 | Hard | Implement a maze solver that returns a valid path. |

The tasks are based on the original MazeSolver project. Each workspace contains an intentionally broken implementation that serves as the starting point for code repair.

## Installation

Clone the repository:

```bash
git clone https://github.com/aurobinda824/Projects.git
cd Projects/CodeFix-RL
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Tests

Run the project test suite:

```bash
python -m pytest -v
```

The original broken workspace implementations are intentionally retained. Their known failing public tests are expected baseline failures, not failures of the submitted solutions.

## Manual Evaluation

The environment supports manual solution submissions.

Create a submission file inside `submissions/`.

For example, Task 1:

```python
def manhattan_distance(goal, pos):
    return abs(goal[0] - pos[0]) + abs(goal[1] - pos[1])
```

Run the evaluation:

```bash
python -m scripts.manual_agent \
    --task task1 \
    --submission submissions/task1_attempt1.py \
    --attempt 1 \
    --method manual
```

Supported task identifiers:

- `task1`
- `task2`
- `task3`

The evaluation runner displays the task description, original source code, submitted code, verification result, and reward.

Results are appended to:

```text
results/manual_runs.jsonl
```

Each record includes the task identifier, difficulty, attempt number, evaluation method, number of passed tests, reward, and verification status.

## Environment Interface

The environment follows a simplified Gym-style interaction pattern.

### Reset

```python
observation, info = env.reset("task1")
```

The observation provides information about the selected task, including its description, difficulty, and source code.

### Step

```python
observation, reward, terminated, truncated, info = env.step(
    {"code": submitted_source}
)
```

The environment submits the candidate implementation to the verifier and returns the reward and termination information.

### Reward

The current reward function is binary:

| Verification result | Reward |
|---|---:|
| All test cases pass | 1.0 |
| One or more test cases fail | 0.0 |

## Anti-Gaming Experiments

The project includes targeted tests for:

1. Attempts to manipulate public test files.
2. Hardcoded answers for known examples.
3. Acceptance of legitimate solutions.

These experiments test specific attack scenarios and should not be interpreted as comprehensive security validation.

## Experimental Results

The initial manual evaluation produced the following results:

| Task | Passed | Total | Reward |
|---|---:|---:|---:|
| Task 1 | 5 | 5 | 1.0 |
| Task 2 | 2 | 3 | 0.0 |
| Task 3 | 3 | 3 | 1.0 |

See [results.md](results.md) for the detailed experimental report and limitations.

## Scope and Limitations

This is a functional prototype rather than a production-ready reinforcement learning benchmark.

Current limitations include:

- Only three benchmark tasks.
- No trained reinforcement learning policy.
- Initial evaluation performed through manual submissions.
- Binary reward rather than partial-credit scoring.
- Subprocess execution without complete security sandboxing.
- No Docker-based execution.

See [scope.md](scope.md) for additional implementation details and design decisions.

## Technologies

- Python
- pytest
- subprocess-based verification
- Git

## Acknowledgements

The benchmark tasks are derived from the MazeSolver Python project and adapted for code-repair evaluation.

