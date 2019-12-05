import os
import sys
from . import plugins as PluginInterfaceShaded
import liquidbt_plugin_build
from typing import List

__all__ = [
    "main", "plugin_list_type"
]

plugin_list_type = List[PluginInterfaceShaded.Plugin]


def main(plugins: plugin_list_type = []):
    PluginInterfaceShaded.log("Loading Plugins", phase=1)
    if plugins is None:
        plugins = []

    build_plugin_present = False
    for plugin in plugins:
        if type(plugin) == liquidbt_plugin_build.Build:
            build_plugin_present = True

        if plugin.plugin_type == "transformer" and not build_plugin_present:
            raise EnvironmentError(
                """
You tried to load a transformer without the build plugin!
Ensure you define the build plugin before any transformers
in in the list.
                """)
        else:
            plugin.load()

    args = sys.argv
    command = ""
    for item in args:
        if not item.startswith("-") and not item.endswith(".py"):
            command = item.replace("-", "")

    if command == "":
        if type(plugins) == list and len(plugins) != 0 and build_plugin_present:
            # hacky way to say that most users want to not need to say
            # build when they want to build it, so if the build
            # plugin is active, default to it's command
            command = "build"
        else:
            raise ValueError("No command specified!")

    for plugin in plugins:
        for key in plugin.commands.keys():
            if command == key:
                plugin.commands[command](plugins)
        plugin.shutdown()
