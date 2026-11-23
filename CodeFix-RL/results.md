# CodeFix-RL — Experimental Results

## 1. Overview

This document summarizes the initial evaluation of CodeFix-RL, a lightweight reinforcement-learning-style environment for code repair tasks derived from the MazeSolver Python project.

The benchmark contains three code repair tasks with different difficulty levels:

- **Task 1 — Easy:** Correct the Manhattan distance calculation.
- **Task 2 — Medium:** Implement boundary-safe neighbour detection.
- **Task 3 — Hard:** Implement a valid maze-solving algorithm that returns a path.

Each task provides an initial broken implementation, a code submission interface, and an independent verification mechanism.

## 2. Evaluation Setup

| Parameter | Configuration |
|---|---|
| Environment | CodeFix-RL |
| Source project | MazeSolver |
| Programming language | Python |
| Python version | 3.14.10 |
| Test framework | pytest 9.2.0 |
| Evaluation method | Manual solution submission |
| Reward mechanism | Binary (0 or 1) |
| Execution platform | Linux |
| Docker | Not implemented |

Solutions were submitted as Python files and evaluated through the unified verification interface.

A task receives a reward of 1.0 only when all its verification cases pass. Otherwise, it receives 0.0.

## 3. Experimental Results

The following results were recorded in `results/manual_runs.jsonl`.

| Task | Difficulty | Tests Passed | Total Tests | Reward | Result |
|---|---|---:|---:|---:|---|
| Task 1 | Easy | 5 | 5 | 1.0 | Passed |
| Task 2 | Medium | 2 | 3 | 0.0 | Failed |
| Task 3 | Hard | 3 | 3 | 1.0 | Passed |
| **Total** | | **10** | **11** | **2.0 / 3.0** | |

### Task 1: Manhattan Distance

**Result: Passed (5/5)**

The original implementation calculated Euclidean distance instead of Manhattan distance.

The submitted implementation replaced the calculation with:

`abs(goal[0] - pos[0]) + abs(goal[1] - pos[1])`

All five verification cases passed.

### Task 2: Neighbour Detection

**Result: Failed (2/3)**

The original implementation did not properly handle maze boundaries. In particular, negative indices could access elements from the opposite side of a Python list.

The submitted implementation introduced explicit row and column boundary checks before accessing neighbouring cells.

Two of the three verification cases passed. One case remains unresolved.

### Task 3: Maze Solver

**Result: Passed (3/3)**

The original implementation had missing boundary checks and returned the explored cells rather than a reconstructed path.

The submitted implementation used depth-first search with a stack, a visited set, and parent tracking.

It successfully returned a valid path for all three verification cases.

## 4. Anti-Gaming Experiments

Three anti-gaming tests were executed.

| Experiment | Outcome |
|---|---|
| Attempt to manipulate public test files | Passed |
| Hardcoded answers for known examples | Passed |
| Legitimate solution acceptance | Passed |

These experiments indicate that the verifier resisted the specific manipulation and hardcoding attempts tested.

They do not establish comprehensive protection against arbitrary adversarial submissions.

## 5. Framework Test Results

The project test suite was executed using pytest.

The recorded run collected 23 tests:

- 20 tests passed.
- 3 tests failed.

The three failures were associated with the intentionally broken original Task 1 and Task 3 workspace implementations. The submitted solutions were evaluated separately through the unified verifier.

The framework tests covering environment behaviour, verification, reward calculation, and anti-gaming passed.

## 6. Limitations

The current implementation has several limitations:

1. **No autonomous RL agent:** Evaluation was performed through manual code submissions. No trained reinforcement learning policy or autonomous AI coding agent was evaluated.
2. **Limited task coverage:** The benchmark currently contains only three tasks.
3. **Binary reward:** The reward function does not distinguish partial progress between failed and successful submissions.
4. **Sandboxing:** Submissions are executed in subprocesses, but this is not a complete security sandbox against malicious code.
5. **Hidden-test limitations:** Verification cases are implemented in the project verifier and are not backed by a separate secure evaluation service.
6. **Docker:** Containerization and Docker-based execution were not implemented.

## 7. Future Improvements

Potential improvements include:

- Add more tasks from real-world Python repositories.
- Introduce partial rewards based on test coverage.
- Evaluate autonomous coding agents.
- Improve submission isolation and execution security.
- Expand adversarial testing.
- Add execution time and resource limits.
- Introduce more difficult tasks involving multiple files and dependencies.

## 8. Conclusion

The initial implementation demonstrates a working code-repair environment with three tasks of increasing difficulty, a unified submission interface, automated verification, and a binary reward mechanism.

Two tasks passed all verification cases, while one achieved partial success. The anti-gaming experiments also passed their targeted checks.

The current version should be considered a functional prototype rather than a production-ready RL benchmark. Further work is needed to expand task coverage, improve execution isolation, and evaluate autonomous agents.

