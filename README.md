# Slav King

This is a 2D game written in Python using the `pygame` library. It is currently in early stages of development, but is in a stable state and is playable.
Some graphics are WIP and temporary sprites from third-party authors are currently used. This is subject to change, and they will be replaced with origial artwork.
The game settings are stored in `data/settings.ini` and can be changed to your preference.

## Gameplay

### Objective

You are a criminal 'slav', who roams the streets of Russia and is generally up to no good.
There is no clear goal, but the intended playthrough consists of buying a weapon and killing as many cops as you can.
As you shoot more cops, you earn more money, which you can use to buy better weapons and powerups such as mayonnaise and beer.

### Powerups

The powerups in the game can be purchased in the shop and are activated in-game by clicking the powerup icon.

#### Mayonnaise

Mayonnaise **increases** your speed by 2x and increases the damage dealt to cops by 2x. Cost: $50.

#### Beer

Beer **decreases** your speed by 2x and increases the damage dealt to cops by 3x. Cost: $60.

### Weapons

- Beretta ($50)
- Deagle ($150)
- MP5 ($200)
- AK-47 ($300)

## Installation

You must have Python 3 installed to play this game. The latest Python version is recommended and can be installed at [python.org](https://www.python.org/downloads/).
If you already have an older Python 3 version, the program should run fine.
The game has only been tested on `3.11` so if you encounter any problems consider upgrading your Python installation.

After installing python, you must install the required dependencies.
This can be done using Pip and the provided `requirements.txt` file.
Depending on your system, the exact commands may differ.
Below are some suggestions that should work for the majority of users.

Windows:

```sh
py -m pip install -r requirements.txt
```

Unix-based systems:

```sh
pip install -r requirements.txt
```

For the best results ensure that the `pip` package is up-to-date.
On fresh installations, this is not always the case!

To run the game, enter the `slav-king` directory and run the following command:

```sh
python main.pyw
```

## Hardware support

The game currently requires a keyboard and mouse to play to its full extent.
In the future, it is planned to only require a keyboard by implementing keyboard shortcuts for all needed tasks.
Additionally, for Windows users, there is controller support in the form of button and joystick bindings.
For tasks that require the mouse, the right stick can be used to artificially move the cursor (WIP solution).

## Supported command line arguments

These switches may be appended to the command when running the app from a terminal or console.

```sh
python main.pyw [...]
```

1. `-s` or `--skip-update-check`: Doesn't perform the automatic update check on startup. Effectively an 'offline mode'.

## Planned changes

- ~~add keybinds for powerups~~ *Edit 2023-12-23: Implemented in [85dbd5d](https://github.com/kguzek/slav-king/commit/85dbd5d3440a44535ec54e8df509c0d0bbc3d3c5)*
- add general keyboard support
- add keyboard shortcut editor
- add game objectives
- add info/help, item descriptions
- replace temp sprites with own artwork
- add 'crouching' and melee attacks
- add end-game cops who can shoot at the player

Thank you for reading!
