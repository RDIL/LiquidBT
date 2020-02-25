"""LiquidBT entrypoint."""

import sys
import liquidbt_plugin_build
import liquidbt_i18n
import os
import json
import functools
from .plugins import log, Plugin
from typing import List

__all__ = [
    "main", "plugin_list_type", "load_translations"
]


@functools.lru_cache(maxsize=None)
def load_translations(identifier: str = "en_us"):
    return json.load(
        open(
            "/".join([
                os.path.abspath(
                    os.path.dirname(
                        liquidbt_i18n.this
                    )
                ),
                f"{identifier}.json"
            ]), "r"
        )
    )


plugin_list_type = List[Plugin]


def main(plugins: plugin_list_type = [], lang: str = "en_us"):
    """Runtime."""

    locale = load_translations(lang)
    log(locale["build.loadPlugins"], phase=1, emoji="load")

    build_plugin_present = False
    for plugin in plugins:
        if type(plugin) == liquidbt_plugin_build.Build:
            build_plugin_present = True

        if plugin.plugin_type == "transformer" and not build_plugin_present:
            raise EnvironmentError(locale[
                "errors.transformerLoadWithoutBuildPlugin"
            ])
        else:
            plugin.load()

    command = ""
    for item in sys.argv:
        if not item.startswith("-") and not item.endswith(".py"):
            command = item.replace("-", "")

    if command == "":
        if type(plugins) == list and len(plugins) != 0 \
                                and build_plugin_present:
            # hacky way to say that most users want to not need to say
            # build when they want to build it, so if the build
            # plugin is active, default to it's command
            command = "build"
        else:
            raise ValueError(locale["errors.noCommand"])

    for plugin in plugins:
        for key in plugin.commands.keys():
            if command == key:
                plugin.commands[command](plugins, locale)
        plugin.shutdown()
