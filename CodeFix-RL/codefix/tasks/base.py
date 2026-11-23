from abc import ABC, abstractmethod


class BaseTask(ABC):
    """Interface for all code repair tasks."""

    task_id: str
    description: str
    initial_code: str

    @abstractmethod
    def get_observation(self) -> dict:
        pass

    @abstractmethod
    def evaluate(self, submission: str) -> dict:
        pass
