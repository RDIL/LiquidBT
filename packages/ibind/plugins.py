class Plugin:
    def __init__(self):
        """Called on initialization of the plugin class."""
        pass

    def load(self):
        """Called on load of the plugin from within ibind."""
        pass

    def shutdown(self):
        """Called on shutdown of ibind."""
        pass
    
    def commands(self):
        """
        Entrypoint to add custom commands.
        
        Format:
        {
            "my-command-name": someFunctionOrLambda
        }

        The function must accept the argument b,
        which will be whatever configuration the
        user passed, as well as plugins, which will be
        None or a list of Plugin objects.
        You may need to validate the types.

        If you don't want to add additional commands, just
        return None for this function.
        """
        return {}
    
    @property
    def plugin_type(self):
        return "typical"


def log(message, phase=2, max=6):
    """
    Log a message.

    Use the params phase and max to generate
    a category number for the message, e.g.:
    
    [2/6] Doing stuff...
    """
    print(f"[{phase}/{max}] {message}")


class TransformerPlugin(Plugin):
    """A Plugin that can transform code."""
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
                    # some boolean:
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

    @property
    def plugin_type(self):
        return "transformer"
