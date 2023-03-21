"""Variable definitions for Slav King."""

import random
import pygame

pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.mixer.init()
pygame.init()

# Pygame window
WIN_WIDTH = 960
WIN_HEIGHT = 540
win = pygame.display.set_mode(
    (WIN_WIDTH, WIN_HEIGHT), pygame.SRCALPHA
)  # and pygame.RESIZABLE)
pygame.display.set_caption("Slav King")

# Resources
IMAGE_DIR = "data/images/"
SPRITE_DIR = "data/sprites/"
AUDIO_DIR = "data/audio/"

bg = pygame.image.load(IMAGE_DIR + "bg_main.png")
bg_store = pygame.image.load(IMAGE_DIR + "bg_store.png")
bullet_stack = pygame.image.load(IMAGE_DIR + "icon_bullets.png")
coin_stack = pygame.image.load(IMAGE_DIR + "icon_coins.png")
mayo_jar = pygame.image.load(IMAGE_DIR + "icon_mayo.png")
mayo_jar_bw = pygame.image.load(IMAGE_DIR + "icon_mayo_bw.png")
beer_bottle = pygame.image.load(IMAGE_DIR + "icon_beer.png")
beer_bottle_bw = pygame.image.load(IMAGE_DIR + "icon_beer_bw.png")
store_icon = pygame.image.load(IMAGE_DIR + "icon_store.png")
mouse_icon = pygame.image.load(IMAGE_DIR + "icon_mouse.png")
back = pygame.image.load(IMAGE_DIR + "icon_back.png")
star_0 = pygame.image.load(IMAGE_DIR + "star_empty.png")
star_1 = pygame.image.load(IMAGE_DIR + "star_filled.png")

# Scaling of resources
pause_bg = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
pause_bg.fill((0, 0, 0))
pause_bg.set_alpha(192)
bg = pygame.transform.scale(bg, (960, 540))
bullet_stack = pygame.transform.scale(bullet_stack, (64, 64))
coin_stack = pygame.transform.scale(coin_stack, (64, 64))
mayo_jar = pygame.transform.scale(mayo_jar, (37, 58))
mayo_jar_bw = pygame.transform.scale(mayo_jar_bw, (37, 58))
beer_bottle = pygame.transform.scale(beer_bottle, (20, 62))
beer_bottle_bw = pygame.transform.scale(beer_bottle_bw, (20, 62))
store_icon = pygame.transform.scale(store_icon, (64, 64))
mouse_icon = pygame.transform.scale(mouse_icon, (64, 64))
back = pygame.transform.scale(back, (128, 128))
star_0 = pygame.transform.scale(star_0, (32, 32))
star_1 = pygame.transform.scale(star_1, (32, 32))

# Game variables
score = 0
ammo_count = 20
wanted_level = 0
fps = 0
shot_cooldown_time_passed = 0
shot_cooldown = 0
time_passed_since_last_cop_spawned = 0
cop_spawn_delay = random.randint(500, 2500) / 1000
cop_amount = 1
win_x = 0
pause_menu = "main"
previous_pause_menu = ""
pause_instructions = {
    "main": "unpause",
    "volume": "options",
    "options": "main",
    "dev": "options",
    "shop": "prev",
    "quit": "main",
}
run = True
firing = False
paused = False
selected_gun = None
mayo_power = False
beer_power = False
slider_engaged = False
cop_hovering_over = (False, ())
cops = []
sounds = []
bullets = []
drops = []
purchasables = []

# Fonts used
standard_font = pygame.font.SysFont("comicsans", 18, False)
bold_font = pygame.font.SysFont("comicsans", 18, True)
big_font = pygame.font.SysFont("comicsans", 45, True)
big_outline_font = pygame.font.SysFont("comicsans", 49, True)
large_font = pygame.font.SysFont("comicsans", 100, False)

clock = pygame.time.Clock()  # To make calling the method quicker
for c in range(0, 8):
    pygame.mixer.Channel(c)

joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
for joystick in joysticks:
    joystick.init()

# This is a PyCharm bug, the parameter is required
pygame.mixer.set_reserved(1)
