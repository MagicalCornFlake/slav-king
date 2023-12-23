"""Global game variable definitions."""

from configparser import ConfigParser

# Game variables
score = 0
money_count = 0
wanted_level = 0
fps = 0
shot_cooldown_time_passed = 0
shot_cooldown = 0
time_passed_since_last_cop_spawned = 0
cop_amount = 1
win_x = 0
pause_menu = "main"
previous_pause_menu = ""

run = True
firing = False
paused = False
selected_gun = None
slider_engaged = False
cops = []
bullets = []
drops = []

settings: ConfigParser
