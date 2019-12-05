import os
import sys
from . import plugins as PluginInterfaceShaded
import liquidbt_plugin_build

__all__ = [
    "main"
]


def main(b, plugins=[]):
    PluginInterfaceShaded.log("Loading Plugins", phase=1)
    if plugins is None:
        plugins = []

    for plugin in plugins:
        plugin.load()

    args = sys.argv
    command = ""
    for item in args:
        if not item.startswith("-") and not item.endswith(".py"):
            command = item.replace("-", "")
    
    if command == "":
        if type(plugins) == list and len(plugins) != 0:
            # hacky way to say that most users want to not need to say
            # build when they want to build it, so if the distribute
            # plugin is active, default to build
            for plugin in plugins:
                if type(plugin) == ibind_plugin_build.BuildPlugin:
                    command = "build"
        else:
            raise ValueError("No command specified!")

    for plugin in plugins:
        for key in plugin.commands().keys():
            if command == key:
                plugin.commands()[command](b, plugins)
        plugin.shutdown()
