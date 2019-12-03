class Plugin:
    def __init__(self):
        """Called on initialization of the plugin class."""
        pass

    def load(self):
        """Called on load of the plugin from within ibind."""
        pass

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
            class MyPlugin(Plugin):
                def process_code(
                    self,
                    code: str
                ) -> str:
                    # boolean:
                    needs_transform = True
                    if needs_transform:
                        return code.replace(
                            "PLACE HOLDER",
                            "secret123"
                        )
                    else:
                        return code
        """
        return code

    def shutdown(self):
        """Called on shutdown of ibind."""
        pass
