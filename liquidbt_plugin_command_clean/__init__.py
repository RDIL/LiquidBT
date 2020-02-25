from liquidbt.plugins import Plugin
from liquidbt_plugin_build.handlers import unsafely_clean


class CleanCommand(Plugin):
    """Plugin that adds the 'clean' command (same functionality as the build plugin)."""

    @property
    def commands(self):
        return {
            "clean": self.entrypoint
        }

    def entrypoint(self, plugins, locale):
        if self.get_build_plugin(plugins) == None:
            raise RuntimeError("Couldn't find build plugin!")

        for p in self.get_build_plugin(plugins).packages:
            unsafely_clean(p.pkgname, False)

