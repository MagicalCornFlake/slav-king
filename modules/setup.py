import os
import subprocess
import sys
import tkinter
import tkinter.messagebox

tkinter.Tk().wm_withdraw()  # Hides root window

key_index = {"escape": 27,
             "space": 32,
             "left_shift": 1073742049,
             "right_shift": 1073742053,
             "left_control": 1073742048,
             "right_control": 1073742052,
             "left_alt": 1073742050,
             "right_alt": 1073742054}
for char in "abcdefghijklmnopqrstuvwxyz":
    key_index[char] = ord(char)


# Define custom message box called 'abort/retry/ignore' using Tknter's template
def ask_abort_retry_ignore(title=None, message=None, _icon=tkinter.messagebox.WARNING,
                           _type=tkinter.messagebox.ABORTRETRYIGNORE, **options):
    if _icon and "icon" not in options:
        options["icon"] = _icon
    if _type and "type" not in options:
        options["type"] = _type
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


def init():
    default_settings = {
        "volume": 100, "muted": False,
        "left_key": "a", "right_key": "d", "jump_key": "space",
        "attack_key": "left_control", "pause_key": "escape",
        "highscore": 0, "start_money": 120,
        "showPlayerHitbox": False, "showCopHitboxes": False
        }
    if os.path.exists("data/temp.txt"):  # Checks if temporary file has already been made by previous instances
        msg = """Either Slav King didn't close properly last time, or it is already running. It is recommended to abort\
or to close that instance of the game before retrying.
Choosing 'ignore' and running multiple instances of Slav King may cause performance issues."""
        dialog_reply = ask_abort_retry_ignore("Already running", msg)
        if dialog_reply == "retry":
            # Uncomment below to launch restarted instances using pythonw.exe instead of python.exe (no console)
            # Creates a new instance (restarts the program)
            subprocess.call(["cmd.exe", "/c", "START", sys.executable, sys.argv[0]])
            
            # Kills current instance
            sys.exit()
        elif dialog_reply == "abort":
            # Kills current instance
            sys.exit()
        elif dialog_reply == "ignore":
            os.remove("data/temp.txt")
    # Creates temporary file to indicate the program is already running to future instances
    with open("data/temp.txt", "w+") as file:
        file.write("Slav King is running...")

    settings = {}
    with open("data/settings.txt", "r") as file:
        data = file.readlines()  # Reads the settings.txt file in which program settings are stored
        for line in data:
            line = line.rstrip()  # Removes trailing newlines from each line
            items = line.split("=")  # Splits each line into an 'item' and a 'value'
            for item in items:
                items[items.index(item)] = item.strip()  # Removes whitespaces from each item
                if item == "":
                    items.remove(item)
            try:
                if items[1] in ["True", "False"]:
                    settings[items[0]] = items[1] == "True"
                else:
                    try:
                        settings[items[0]] = int(items[1])  # Adds a dictionary entry for each item and integer value
                    except ValueError:
                        settings[items[0]] = items[1]  # Adds a dictionary entry for each item and string value
            except IndexError:
                settings[items[0]] = 0  # Uses value of '0' if none specified in settings.txt
    for key in default_settings:
        if key not in settings:
            settings[key] = default_settings[key]
    return settings


def finish(updated_settings):
    # Writes changed settings to settings.txt
    with open("data/settings.txt", "w") as data_file:
        for setting in updated_settings:
            current_line = setting + " = " + str(updated_settings[setting]) + "\n"
            data_file.write(current_line)
    os.remove("data/temp.txt")


if __name__ == "__main__":
    print(key_index)
