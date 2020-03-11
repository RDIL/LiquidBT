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
        """Called on shutdown of LiquidBT."""
        pass

    @property
    def name(self) -> str:
        """The plugin's name."""
        return "Unnamed"

    @property
    def plugin_type(self):
        """The plugin type - primarily used by build module."""
        return "typical"
