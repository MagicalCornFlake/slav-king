"""Module that handles the command line arguments for the program."""

import sys

argument_names = {
    "no-update": ["-s", "--skip-update-check"],
}


def get_run_arguments():
    """Returns a list of the mapped argument names provided by the user."""
    args = [
        key
        for key, value in argument_names.items()
        if any(arg in sys.argv[1:] for arg in value)
    ]
    return args
