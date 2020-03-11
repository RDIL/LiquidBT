import sys


def get_named_command() -> str:
    command = "build"
    for item in sys.argv:
        if not item.startswith("-") and not item.endswith(".py"):
            command = item
    return command
