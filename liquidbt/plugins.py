"""The plugin API."""

from . import RunContext


class Plugin:
    """The plugin object."""

    name: str

    def __init__(self, *args, **kwargs) -> None:
        """
        Called on initialization of the plugin class.

        Arguments:
            args: The arguments.
            kwargs: The keyword arguments.

        Returns:
            Nothing.
        """

        self.args = args
        self.kwargs = kwargs
        self.name = "Unnamed"

    def load(self, ctx: RunContext) -> None:
        """
        Called on load of the plugin from within LiquidBT.

        If you are overriding this, **you should set
        `self.ctx` to the passed argument.**

        Arguments:
            ctx: The RunContext object.

        Returns:
            Nothing.
        """
        self.ctx = ctx

    def shutdown(self) -> None:
        """
        Called on shutdown of LiquidBT.

        At this point, no new tasks can be created,
        so just run any final code here.

        Returns:
            Nothing.
        """
        pass
