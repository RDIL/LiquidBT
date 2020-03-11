"""The plugin API."""


class Plugin:
    """Typical plugin interface."""

    def __init__(self, *args, **kwargs):
        """Called on initialization of the plugin class."""

        self.args = args
        self.kwargs = kwargs

    def load(self, ctx):
        """
        Called on load of the plugin from within LiquidBT.

        If you are overriding this, **you should set
        `self.ctx` to the passed argument.**
        """
        self.ctx = ctx

    def shutdown(self):
        """
        Called on shutdown of LiquidBT.

        At this point, no new tasks can be created,
        so just run any final code here.
        """
        pass

    @property
    def name(self) -> str:
        """The plugin's name."""
        return "Unnamed"
