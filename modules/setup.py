"""Settings loading, multi-instance program handling"""

import configparser
import os
import sys

from modules import variables, gui


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
        "activate_beer": "b",
        "activate_mayo": "m",
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
        dialog_reply = gui.ask_abort_retry_ignore("Already running", msg)
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
