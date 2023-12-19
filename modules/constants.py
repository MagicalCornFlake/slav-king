"""Constant variable definitions for Slav King."""

# Pygame window
WIN_WIDTH = 960
WIN_HEIGHT = 540

# Resources
IMAGE_DIR = "data/images/"
SPRITE_DIR = "data/sprites/"
AUDIO_DIR = "data/audio/"

PAUSE_INSTRUCTIONS = {
    "main": "unpause",
    "volume": "options",
    "options": "main",
    "dev": "options",
    "shop": "prev",
    "quit": "main",
}

LOOT_TABLE = {
    "money": {"drop_chance": 3, "pickup_amount_multiplier": 4},
    "ammo_light": {"drop_chance": 4, "pickup_amount_multiplier": 2},
    "ammo_heavy": {"drop_chance": 1, "pickup_amount_multiplier": 1},
}
