from liquidbt.plugins import Plugin


class Deploy(Plugin):
    def __init__(self, *config):
        self.config = config

    @property
    def commands(self):
        return {
            "deploy": self.deploy,
            "publish": self.deploy,
        }

    def deploy(self, plugins):
        self.entrypoint(self.config, plugins)

    @staticmethod
    def entrypoint(config, plugins):
        raise NotImplementedError("This plugin is coming soon!")
