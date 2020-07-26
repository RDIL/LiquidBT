"""LiquidBT's main entrypoint."""

from .plugins import Plugin
from .build_tools import handle_package, handle_single_file
from .tasks import RunContext, Task, TaskStatuses
from .build_tools.typeClasses import (
    SourceDist,
    WheelBinaryDist,
    DistFormat,
    PackageConfig,
)
from typing import List, Union
from .progressbars import CustomProgressBar
import argparse

__all__ = [
    "main",
    "SourceDist",
    "WheelBinaryDist",
    "DistFormat",
    "PackageConfig",
    "RunContext",
    "Task",
]


def main(
    *args, plugins: List[Plugin] = [], **kwargs,
) -> None:
    """
    The build system runtime.

    For the keyword arguments,
    pass either packages (a list of PackageConfig objects),
    and/or files (a list of paths to individual files to build).

    Arguments:
        args: This isn't actually used, just ignore it.
        plugins: The list of plugins that you want to use.
        kwargs: The keyword arguments.

    Returns:
        Nothing.
    """

    parser = argparse.ArgumentParser(
        description="The CLI for your build system."
    )
    parser.add_argument(
        "command", type=str, nargs="?", help="the command you want to run."
    )

    bar = CustomProgressBar().post_init()

    command = parser.parse_args().command
    if command is None:
        command = "build"

    files = kwargs.get("files", [])
    packages = kwargs.get("packages", [])

    if packages == [] and files == [] and plugins == []:
        raise RuntimeError(
            "You need to add build configs or plugins to the main() arguments!"
        )

    ctx = RunContext(command, bar)

    print("\n")

    if command == "build":
        for f in files:
            ctx.add_task(_create_build_task(ctx, f, False))

        for package in packages:
            ctx.add_task(_create_build_task(ctx, package, True))

    for plugin in plugins:
        plugin.load(ctx)

    while True:
        for task in ctx.get_tasks():
            if task.status is TaskStatuses.READY:
                ctx._progress_bar.before_task(task)
                task()
                ctx._progress_bar.after_task()
                task.status = TaskStatuses.COMPLETED
                continue
        break

    for plugin in plugins:
        plugin.shutdown()

    bar.do_output("✓ Done!")
    bar.update()

    bar.finish()


def _create_build_task(
    ctx: RunContext, build_item: Union[str, PackageConfig], is_package: bool
) -> Task:
    """
    Creates a task on the fly to build a package or file.

    Arguments:
        ctx: The `RunContext` object.
        build_item: The PackageConfig object or path to the file.
        is_package: If this is a package instead of a file.

    Returns:
        A `Task` object.
    """

    class VirtualBuildTask(Task):
        name: str = "Build " + (  # type: ignore
            build_item.pkgname if is_package else build_item  # type: ignore
        )

        def run(self):
            if is_package:
                handle_package(ctx, build_item)
            else:
                handle_single_file(ctx, build_item)

    return VirtualBuildTask()
