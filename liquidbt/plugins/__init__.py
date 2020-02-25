import os
import typing


class Plugin:
    """Typical plugin interface."""

    def __init__(self, *args, **kwargs):
        """Called on initialization of the plugin class."""
        self.args = args
        self.kwargs = kwargs

    def load(self):
        """Called on load of the plugin from within LiquidBT."""
        pass

    def shutdown(self):
        """Called on shutdown of LiquidBT."""
        pass

    @property
    def name(self) -> str:
        return "Unnamed"

    @property
    def commands(self) -> typing.Dict[str, typing.Callable]:
        """
        Entrypoint to add custom commands.

        Example:
            class CustomCommand(Plugin):
                @property
                def commands(self):
                    return {
                        "my-command-name": someFunctionOrLambda
                    }

        The function must accept the argument
        plugins, which will be
        None or a list of Plugin objects.
        You may need to validate the types.

        If you don't want to add additional commands,
        don't override this function.
        """
        return {}

    @property
    def plugin_type(self):
        return "typical"

    def get_build_plugin(self, plugins: list):
        """Finds the build plugin in the list of plugins."""

        from liquidbt_plugin_build import Build
    
        for plugin in plugins:
            if type(plugin) == Build:
                return plugin
        return None


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


def log(message, phase=2, max=7, emoji=""):
    """
    Log a message.

    Use the params phase and max to generate
    a category number for the message, e.g.:

    [2/7] Doing stuff...
    """
    if os.getenv("CI") is not None:
        print(f"[{phase}/{max}] {message}")
    else:
        print(f"{emotes[emoji]} [{phase}/{max}] {message}")


emotes = {
    "": "",
    "load": "📥",
    "build": "🛠",
    "write": "📝",
    "transform": "⛓",
    "launch": "📡",
    "clean": "🧽",
    "done": "🎉"
}
