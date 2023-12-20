"""Settings loading, multi-instance program handling"""

import configparser
import os
import sys

import tkinter
import tkinter.messagebox

from modules import variables


tkinter.Tk().wm_withdraw()  # Hides root window


# Define custom message box called 'abort/retry/ignore' using Tkinter's template
def ask_abort_retry_ignore(
    title: str = None,
    message: str = None,
    _icon: str = tkinter.messagebox.WARNING,
    _type: str = tkinter.messagebox.ABORTRETRYIGNORE,
    **options,
) -> str:
    """Create an ABORT/RETRY/IGNORE message box.

    Args:
        title (str, optional): the dialog box title. Defaults to None.
        message (str, optional): the dialog box message. Defaults to None.
        _icon (str, optional): the dialog box icon. Defaults to tkinter.messagebox.WARNING.
        _type (str, optional): the dialog box type. Defaults to tkinter.messagebox.ABORTRETRYIGNORE.

    Returns:
        str: the user response ("yes"/"no" etc.).
    """
    if _icon:
        options.setdefault("icon", _icon)
    if _type:
        options.setdefault("type", _type)
    if title:
        options["title"] = title
    if message:
        options["message"] = message
    message_box = tkinter.messagebox.Message(**options)
    res = message_box.show()
    # In some Tcl installations, yes/no is converted into a boolean.
    if isinstance(res, bool):
        return "yes" if res else "no"
    # In others we get a Tcl_Obj.
    return str(res)


def read_settings() -> configparser.ConfigParser:
    """Reads the user settings and returns them as a dictionary."""
    config = configparser.ConfigParser()

    # Default settings options
    config["General"] = {
        "volume": 100,
        "muted": False,
    }
    config["Keybindings"] = {
        "left": "a",
        "right": "d",
        "jump": "w",
        "attack": "space",
        "pause": "escape",
        "back": "escape",
        "open_shop": "p",
    }
    config["Cheats"] = {
        "highscore": 0,
        "start_money": 120,
    }
    config["Developer Options"] = {
        "show_player_hitbox": False,
        "show_cop_hitboxes": False,
        "draw_experimental_player_weapon": False,
    }
    config.read("data/settings.ini")
    variables.settings = config
    write_settings()


def ensure_singleton():
    """Checks if temporary file has already been made by previous instances."""
    if os.path.exists("data/temp.lock"):
        msg = (
            "Either Slav King didn't close properly last time, or it is already running. Click "
            "'abort' or close any other instances of the game, then try again.\n Choosing 'ign"
            "ore' and running multiple instances of Slav King may cause performance issues."
        )
        dialog_reply = ask_abort_retry_ignore("Already running", msg)
        if dialog_reply == "retry":
            # Restarts the program
            os.execl(sys.executable, f'"{sys.executable}"', *sys.argv)
        elif dialog_reply == "abort":
            # Kills current instance
            sys.exit()
        elif dialog_reply == "ignore":
            os.remove("data/temp.lock")
    # Creates temporary file to indicate the program is already running to future instances
    with open("data/temp.lock", "w+", encoding="UTF-8") as file:
        file.write("Slav King is running...\n")


def write_settings():
    """Writes the game settings to disk."""
    with open("data/settings.ini", "w", encoding="UTF-8") as data_file:
        variables.settings.write(data_file)


def cleanup():
    """Removes the temporary lockfile."""
    try:
        os.remove("data/temp.lock")
    except FileNotFoundError:
        pass
