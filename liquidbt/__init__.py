"""LiquidBT entrypoint."""

import liquidbt_plugin_build
import liquidbt_i18n
import os
import json
import functools
from .plugins import Plugin
from .tasks import RunContext
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


def main(packages=None, files=None, plugins: plugin_list_type = [], lang: str = "en_us"):
    """Runtime."""

    if files is None:
        files = []
    if packages is None:
        packages = []

    if packages == [] and files == [] and plugins == []:
        raise RuntimeError(
            "You need to add build config(s), or plugins to the liquidbt.main arguments!"
        )

    locale = load_translations(lang)
    ctx = RunContext(locale)

    ctx.log(locale["build.loadPlugins"], emoji="load")

    for plugin in plugins:
        if type(plugin) == liquidbt_plugin_build.Build:
            ctx.build_plugin = plugin
        plugin.load(ctx)

    for plugin in plugins:
        plugin.shutdown()
