import pytest


EXPECTED_BASELINE_FAILURES = {
    "tests/public/test_task1.py::test_diagonal_distance":
        "Original Task 1 implementation uses Euclidean distance.",

    "tests/public/test_task3.py::test_simple_path":
        "Original Task 3 implementation has missing boundary checks.",

    "tests/public/test_task3.py::test_path_avoids_walls":
        "Original Task 3 implementation has missing boundary checks.",
}


def pytest_collection_modifyitems(items):
    for item in items:
        reason = EXPECTED_BASELINE_FAILURES.get(item.nodeid)

        if reason:
            item.add_marker(
                pytest.mark.xfail(reason=reason, strict=True)
            )
