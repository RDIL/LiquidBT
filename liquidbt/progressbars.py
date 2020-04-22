from progress.bar import IncrementalBar


class CustomProgressBar(IncrementalBar):
    """Our custom progress bar."""

    def set_ctx(self, ctx):
        """Sets the build context."""

        self.ctx = ctx

    def before_task(self, task):
        """Runs before a task."""

        self.max = self.ctx.task_count()
        self.message = task.name

    def after_task(self):
        """Runs after a task."""

        self.next()
