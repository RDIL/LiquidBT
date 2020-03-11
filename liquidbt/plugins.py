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


class TransformerPlugin(Plugin):
    """A Plugin that can transform code."""

    def on_build_begin(self):
        """Run when the build starts."""
        return

    def process_code(self, code: str) -> str:
        """
        Called for every file of code.

        This method is built for transformer
        plugins, meaning plugins that
        change the source just before
        setuptools does it's thing.

        The method is called with the arg
        'code' passed to it, which will
        be the code's raw file as a multiline
        string, and this method must return
        the new code. If you don't need
        to transform the source, just return
        the code arg.

        Transformer example:
            class MySecretInjectionPlugin(Plugin):
                def process_code(
                    self,
                    code: str
                ) -> str:
                    return code.replace(
                        "PLACE HOLDER",
                        "secret123"
                    )
        """
        return code

    @property
    def plugin_type(self):
        return "transformer"
