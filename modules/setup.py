"""Code relating to setting up the game, """

import os
import subprocess
import sys
import tkinter
import tkinter.messagebox

tkinter.Tk().wm_withdraw()  # Hides root window

key_index = {
    "escape": 27,
    "space": 32,
    "left_shift": 1073742049,
    "right_shift": 1073742053,
    "left_control": 1073742048,
    "right_control": 1073742052,
    "left_alt": 1073742050,
    "right_alt": 1073742054,
}
key_index.update({char: ord(char) for char in "abcdefghijklmnopqrstuvwxyz"})


# Define custom message box called 'abort/retry/ignore' using Tknter's template
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
    res = tkinter.messagebox.Message(**options).show()
    # In some Tcl installations, yes/no is converted into a boolean.
    if isinstance(res, bool):
        return "yes" if res else "no"
    # In others we get a Tcl_Obj.
    return str(res)


def read_settings() -> dict[str, any]:
    """Reads the user settings and returns them as a dictionary."""
    # Default settings options
    settings = {
        "volume": 100,
        "muted": False,
        "left_key": "a",
        "right_key": "d",
        "jump_key": "space",
        "attack_key": "left_control",
        "pause_key": "escape",
        "highscore": 0,
        "start_money": 120,
        "showPlayerHitbox": False,
        "showCopHitboxes": False,
    }
    with open("data/settings.txt", "r", encoding="UTF-8") as file:
        # Reads the settings.txt file in which program settings are stored
        data = file.readlines()
    for line in data:
        line = line.rstrip()  # Removes trailing newlines from each line
        # Splits each line into an 'item' and a 'value'
        line = line.split("=", maxsplit=1)
        # Removes whitespaces from each item
        try:
            key, value = [itm.strip() for itm in line if itm.strip()]
            if value in ["True", "False"]:
                settings[key] = value == "True"
            else:
                try:
                    # Adds a dictionary entry for each item and integer value
                    value = int(value)
                except ValueError:
                    # Adds a dictionary entry for each item and string value
                    pass
                settings[key] = value
        except (IndexError, ValueError):
            # Uses value of '0' if none specified in settings.txt
            settings[key] = 0
    return settings


def init():
    """Checks if temporary file has already been made by previous instances."""
    if os.path.exists("data/temp.txt"):
        msg = (
            "Either Slav King didn't close properly last time, or it is already running. Click "
            "'abort' or close any other instances of the game, then try again.\n Choosing 'ign"
            "ore' and running multiple instances of Slav King may cause performance issues."
        )
        dialog_reply = ask_abort_retry_ignore("Already running", msg)
        if dialog_reply == "retry":
            # Uncomment below to launch restarted instances using pythonw.exe
            # instead of python.exe (no console). Creates a new instance (restarts the program)
            subprocess.call(["cmd.exe", "/c", "START", sys.executable, sys.argv[0]])
            # Kills current instance
            sys.exit()
        elif dialog_reply == "abort":
            # Kills current instance
            sys.exit()
        elif dialog_reply == "ignore":
            os.remove("data/temp.txt")
    # Creates temporary file to indicate the program is already running to future instances
    with open("data/temp.txt", "w+", encoding="UTF-8") as file:
        file.write("Slav King is running...")
    return read_settings()


def finish(updated_settings: dict):
    """Writes changed settings to settings.txt and removes the temp file."""
    with open("data/settings.txt", "w", encoding="UTF-8") as data_file:
        for key, value in updated_settings.items():
            current_line = f"{key} = {value}\n"
            data_file.write(current_line)
    try:
        os.remove("data/temp.txt")
    except FileNotFoundError:
        pass


if __name__ == "__main__":
    print(key_index)
