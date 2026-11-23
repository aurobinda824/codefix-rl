# CodeFix-RL — Project Scope

## 1. Objective

CodeFix-RL is a lightweight code-repair environment designed to evaluate how an agent or human can identify and repair defects in existing Python code.

The project adapts code from the MazeSolver project into three repair tasks with increasing difficulty.

The environment provides a structured observation, accepts a source-code submission, verifies the implementation, and returns a reward.

## 2. Implementation Scope

The following components have been implemented:

| Component | Description | Status |
|---|---|---|
| Benchmark tasks | Three tasks with different difficulty levels | Implemented |
| Observation interface | Provides task description and broken source code | Implemented |
| Action interface | Accepts corrected Python source code | Implemented |
| Unified verifier | Executes task-specific verification cases | Implemented |
| Reward mechanism | Binary reward based on verification success | Implemented |
| Environment | Reset and step interaction methods | Implemented |
| Anti-gaming tests | Targeted manipulation and hardcoding experiments | Implemented |
| Manual evaluation | Supports manual code submissions | Implemented |
| Result logging | Stores evaluation records in JSONL format | Implemented |

## 3. Benchmark Tasks

### Task 1 — Easy: Manhattan Distance

Repair an incorrect distance calculation that uses Euclidean distance instead of Manhattan distance.

### Task 2 — Medium: Neighbour Detection

Repair maze neighbour detection by introducing proper boundary checks and preventing invalid grid access.

### Task 3 — Hard: Maze Solver

Implement a maze-solving algorithm that returns a valid path from a starting position to a goal while avoiding walls and invalid movements.

## 4. Environment Design

The environment uses a simplified Gym-style interface.

**Observation:** Task identifier, difficulty, description, and original source code.

**Action:** A Python source-code submission.

**Reward:** Binary reward:

- `1.0` when all verification cases pass.
- `0.0` when one or more verification cases fail.

**Termination:** An evaluation episode terminates after a submission is verified.

## 5. Verification and Anti-Gaming

Candidate submissions are executed using subprocess-based verification.

The project includes targeted tests for:

- Public test manipulation attempts.
- Hardcoded outputs for known examples.
- Acceptance of legitimate implementations.

These tests provide limited protection against the specific attacks evaluated. They do not constitute a complete security sandbox.

## 6. Evaluation Scope

The initial evaluation was performed using manually prepared code submissions.

No trained reinforcement learning agent or autonomous coding agent was evaluated.

The recorded results were:

| Task | Passed | Total | Reward |
|---|---:|---:|---:|
| Task 1 | 5 | 5 | 1.0 |
| Task 2 | 2 | 3 | 0.0 |
| Task 3 | 3 | 3 | 1.0 |

See `results.md` for the detailed evaluation report.

## 7. Out of Scope

The following features were not implemented in this prototype:

- Training a reinforcement learning policy.
- Autonomous multi-step code repair.
- Docker-based execution.
- Complete isolation against malicious submissions.
- Large-scale benchmark evaluation.
- Persistent agent memory or learning across episodes.

## 8. Future Work

Potential extensions include:

1. Increasing the number and complexity of benchmark tasks.
2. Introducing partial rewards based on verification progress.
3. Integrating autonomous coding agents.
4. Improving execution isolation and resource restrictions.
5. Supporting multi-file code repair.
6. Measuring execution time and agent efficiency.

## 9. Design Philosophy

The objective was to build a small, reproducible prototype using real code rather than create an unnecessarily complex benchmark.

The implementation prioritizes task clarity, a consistent interaction interface, independent verification, and transparent reporting of experimental limitations.

