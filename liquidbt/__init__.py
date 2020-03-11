"""LiquidBT's main entrypoint."""

import liquidbt_i18n
import os
import json
from .plugins import Plugin
from .build_tools.api import handle_package, handle_single_file
from .tasks import RunContext, Task, TaskStatuses
from typing import List

__all__ = ["main", "plugin_list_type", "load_translations"]


def load_translations(identifier: str = "en_us"):
    """Loads the translations for the named language."""
    return json.load(
        open(
            "/".join(
                [
                    os.path.abspath(os.path.dirname(liquidbt_i18n.this)),
                    f"{identifier}.json",
                ]
            ),
            "r",
        )
    )


plugin_list_type = List[Plugin]


def main(
    *args, plugins: plugin_list_type = [], lang: str = "en_us", **kwargs,
):
    """
    The build system runtime.
    
    For the non-keyword arguments, pass a BuildConfiguration
        instance per each package.
    For the `plugins` argument, pass a list of plugins to use.
    For the `lang` argument, pass a language if you want to use
        it's localization (defaults to `en_US`).
    """

    files = kwargs.get("files")
    packages = args

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

    print(locale["build.loadPlugins"], emoji="load")

    for file in files:
        ctx.add_task(_create_build_task(ctx, file, False))

    for package in packages:
        ctx.add_task(_create_build_task(ctx, package, True))

    for plugin in plugins:
        plugin.load(ctx)

    while True:
        for task in ctx.get_tasks():
            if task.status is TaskStatuses.READY:
                task()
                task.status = TaskStatuses.COMPLETED
                continue
        break

    for plugin in plugins:
        plugin.shutdown()


def _create_build_task(ctx, build_item, is_package):
    """Creates a task on the fly to build a package or file."""

    t = Task()
    t.name = "Build " + build_item

    if is_package:

        def run(self):
            handle_package(ctx, build_item)

    else:

        def run(self):
            handle_single_file(ctx, build_item)

    t.run = run
    return t
