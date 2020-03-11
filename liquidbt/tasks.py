"""The tasks API."""

import os
from typing import List, Optional, Callable
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

    def __init__(self):
        """Create the class."""
        self.status = TaskStatuses.READY

    def __repr__(self):
        return "<Task status={}>".format(str(self.status))

    def run(self):
        """Run the task. (Do NOT manually call this anywhere in your plugin)."""
        pass

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

    # Global data
    locale: List[str]
    _plugins: List[Plugin]
    _transformers: List[Callable]

    def __init__(self, locale):
        """Create the class. THIS IS DONE INTERNALLY, DO NOT RUN!"""
        self.locale = locale

    def add_task(self, task: Task):
        """Adds a task to the task list."""
        self._tasks.append(task)

    def task_count(self) -> int:
        """Get the number of tasks registered total."""
        return len(self._tasks)

    def get_tasks(self) -> List[Task]:
        """Gets the list of tasks registered."""
        return self._tasks

    def log(self, message):
        print(f"    {message}")

    def add_transformer(self, transformer: Callable):
        """Adds a transformer to the end of the list."""
        self._transformers.append(transformer)

    def get_build_transformers(self):
        """Get a list of transformers in the order they were registered in."""
        return self._transformers
