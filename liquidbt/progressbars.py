"""A class that holds our progress bar configurations."""

from progress.bar import IncrementalBar
from sys import stdout
from typing import Any


class CustomProgressBar(IncrementalBar):
    """Our custom progress bar."""

    def post_init(self) -> IncrementalBar:
        """
        Reconfigure the bar if this isn't an interactive terminal.

        Returns:
            The CustomProgressBar object.
        """

        self.interactive = stdout.isatty()
        if not self.interactive:
            self.update = self.noop

        return self

    def do_output(self, output: Any) -> None:
        """
        Logs `output` if the shell is not interactive, or sets the
        title of the progress bar to the value of `output` if it is.

        Arguments:
            output: What to output.

        Returns:
            Nothing.
        """

        if self.interactive:
            self.message = output
        else:
            print("log " + output)

    def noop(self):
        """Does nothing."""

    def set_ctx(self, ctx):
        """Sets the build context."""

        self.ctx = ctx

    def before_task(self, task):
        """Runs before a task."""

        self.max = self.ctx.task_count()
        self.do_output(task.name)

    def after_task(self):
        """Runs after a task."""

        self.next()
