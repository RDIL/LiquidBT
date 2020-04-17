from liquidbt.plugins import Plugin
from liquidbt.build_tools.handlers import unsafely_clean
from liquidbt.tasks import RunContext, create_task


class CleanCommand(Plugin):
    """A plugin that adds the 'clean' command."""

    def load(self, ctx: RunContext):
        self.ctx = ctx
        if self.ctx.command == "clean":
            self.ctx.add_task(create_task("Clean up", self.entrypoint))

    def entrypoint(self):
        for p in self.ctx.packages:
            unsafely_clean(p.pkgname, False)
