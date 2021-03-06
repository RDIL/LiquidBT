"""The tasks API."""

from .progressbars import CustomProgressBar
from typing import Callable, List
from .plugins import Plugin
from enum import IntEnum


class TaskStatuses(IntEnum):
    """An enum for the task statuses."""

    """The task is ready to be executed."""
    READY = 0
    """The task has already finished."""
    COMPLETED = 1
    """The task was skipped."""
    SKIPPED = 2


class Task:
    """A task that can be run."""

    status: int
    name: str

    def __init__(self) -> None:
        """
        Create the class.

        Returns:
            Nothing.
        """
        self.status = TaskStatuses.READY

    def __repr__(self) -> str:
        """
        Get the repr value of this class.

        Returns:
            The repr value.
        """
        return "<Task status={}>".format(str(self.status))

    def run(self) -> None:
        """
        Run the task.

        Add the code that your task should execute here, but
        DO NOT manually call this function anywhere in your plugin.

        Returns:
            Nothing.
        """

    def skip(self):
        """Set the task to skipped, preventing it from being run."""

        self.status = TaskStatuses.SKIPPED

    def __call__(self):
        """Run the task."""

        if self.status is not TaskStatuses.READY:
            return
        self.run()


class RunContext:
    """A mechanism used to manage and store data during runtime."""

    # Task related items
    _tasks: List[Task]
    _progress_bar: CustomProgressBar

    # Global data
    command: str
    _plugins: List[Plugin]
    _transformers: List[Callable]

    def __init__(self, command: str, bar: CustomProgressBar):
        """Create the class. THIS IS DONE INTERNALLY, DO NOT USE!"""

        self._tasks = []
        self._plugins = []
        self._transformers = []
        self.command = command
        self._progress_bar = bar
        self._progress_bar.set_ctx(self)

    def add_task(self, task: Task):
        """Adds a task to the task list."""

        self._tasks.append(task)

    def task_count(self) -> int:
        """Get the number of tasks registered total."""

        return len(self._tasks)

    def get_tasks(self) -> List[Task]:
        """Gets the list of tasks registered."""

        return self._tasks

    def add_transformer(self, transformer: Callable):
        """Adds a transformer to the end of the list."""

        self._transformers.append(transformer)

    def get_build_transformers(self):
        """Get a list of transformers in the order they were registered in."""

        return self._transformers


def create_task(name: str, runnable: Callable) -> Task:
    """
    Creates a task named the value of the `name` argument,
    which calls the `runnable` argument.
    """

    class VirtualTask(Task):
        name: str = name

        def run(self):
            runnable()

    return VirtualTask()
