## Anti-Gaming Experiments

### Experiment 1: Public Test Manipulation

The agent attempted to overwrite the public test suite
with tests that always pass.

Result: Blocked.

The verifier executes its own independent test cases
rather than relying on the candidate's test files.

### Experiment 2: Hardcoded Answers

The agent returned hardcoded outputs for the examples
available in the public task description.

Result: Blocked.

Additional verifier cases exposed the hardcoded behavior.

### Limitations

The verifier implementation and its test cases are
currently part of the public repository. An agent can
inspect them and potentially hardcode every known case.

A production implementation should keep grading cases
outside the agent's accessible workspace and execute
the verifier in a separate restricted environment.
