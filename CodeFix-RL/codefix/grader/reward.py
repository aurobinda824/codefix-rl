def calculate_reward(verification: dict) -> float:
    """
    Award binary reward based on independent verification.
    """

    if verification["status"] == "passed":
        return 1.0

    return 0.0
