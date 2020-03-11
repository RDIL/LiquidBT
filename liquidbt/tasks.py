"""The tasks API."""

import os
from typing import List, Optional
from .plugins import Plugin


class Task:
    """A task that can be run."""

    skipped: bool
    name: str
    subtasks: List[any]

    def __init__(self):
        """Create the class."""
        self.skipped = False
        self.subtasks = []

    def run(self):
        """Run the task. (Do NOT manually call this, use __call__)."""
        pass

    def skip(self):
        """Set the task to skipped, preventing it from being run."""
        self.skipped = True

    def __call__(self):
        """Run the task."""
        if self.skipped:
            return
        self.run()

    def run_subtask(self, subtask_name, *subtask_args):
        """Triggers the running of a subtask with the matching name."""
        for subtask in self.subtasks:
            if subtask.name == subtask_name:
                subtask(*subtask_args)

    def add_subtask(self, subtask):
        """Adds the passed subtask to the list."""
        self.subtasks.append(subtask)


class RunContext:
    """A mechanism used internally to manage and store data during runtime."""

    # Task related items
    _all_tasks: List[Task]
    _completed_tasks: List[Task]

    # Global data
    translations: List[str]
    plugins: List[Plugin]
    build_plugin: Plugin  # circular import prevents static typing this

    def __init__(self, locale):
        """Create the class. THIS IS DONE INTERNALLY, DO NOT RUN!"""
        self.translations = locale

    def add_task(self, task: Task):
        """Adds a task to the task list."""
        self._all_tasks.append(task)

    def task_count(self):
        """Get the number of tasks registered total."""
        return len(self._all_tasks)

    def completed_task_count(self):
        """Get the number of tasks that have completed."""
        return len(self._completed_tasks)

    def __call__(self):
        """Run the next task."""
        if self.task_count() - self.completed_task_count() > 0:
            for task in self._all_tasks:
                if task not in self._completed_tasks:
                    task()
                    self._completed_tasks.append(task)
    
    def log(self, message, emoji: Optional[str] = ""):
        """
        Log a message.

        Example:
            [2/7] Doing stuff...
        """
        phase = str(self.task_count() + 1) + "/" + str(self.task_count() - self.completed_task_count())
        if os.getenv("CI") is not None:
            print(f"[{phase}]  {message}")
        else:
            print(f"[{phase}/{max}] {emoji}  {message}")

    def log_continued_message(self, message):
        """Log a continued message from the previous message (just a style thing)."""
        print(f"         {message}")
