"""Initialisation code"""

import configparser
import pygame

from modules import variables
from modules.constants import WIN_WIDTH, WIN_HEIGHT, IMAGE_DIR
from modules.classes.button import Button, Slider
from modules.classes.purchasables.weapon import Weapon


pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.mixer.init()
pygame.init()

sprites: dict[str, pygame.Surface] = {}
fonts: dict[str, pygame.font.Font] = {}


def init_window():
    win = pygame.display.set_mode(
        (WIN_WIDTH, WIN_HEIGHT), pygame.SRCALPHA
    )  # and pygame.RESIZABLE)
    pygame.display.set_caption("Slav King")

    for c in range(0, 8):
        pygame.mixer.Channel(c)

    # This is a PyCharm bug, the parameter is required
    pygame.mixer.set_reserved(1)

    return win


def init_sprites():
    bg_pause = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
    bg_pause.fill((0, 0, 0))
    bg_pause.set_alpha(192)

    bg = pygame.image.load(IMAGE_DIR + "bg_main.png")
    bg_store = pygame.image.load(IMAGE_DIR + "bg_store.png")
    ammo_light = pygame.image.load(IMAGE_DIR + "icon_ammo_light.png")
    ammo_heavy = pygame.image.load(IMAGE_DIR + "icon_ammo_heavy.png")
    bullet_light = pygame.image.load(IMAGE_DIR + "icon_bullet_light.png")
    bullet_heavy = pygame.image.load(IMAGE_DIR + "icon_bullet_heavy.png")
    coin_stack = pygame.image.load(IMAGE_DIR + "icon_coins.png")
    mayo_jar = pygame.image.load(IMAGE_DIR + "icon_mayo.png")
    mayo_jar_bw = pygame.image.load(IMAGE_DIR + "icon_mayo_bw.png")
    beer_bottle = pygame.image.load(IMAGE_DIR + "icon_beer.png")
    beer_bottle_bw = pygame.image.load(IMAGE_DIR + "icon_beer_bw.png")
    store_icon = pygame.image.load(IMAGE_DIR + "icon_store.png")
    mouse_icon = pygame.image.load(IMAGE_DIR + "icon_mouse.png")
    back = pygame.image.load(IMAGE_DIR + "icon_back.png")
    star_empty = pygame.image.load(IMAGE_DIR + "star_empty.png")
    star_filled = pygame.image.load(IMAGE_DIR + "star_filled.png")

    # Scaling of resources
    bg = pygame.transform.scale(bg, (960, 540))
    ammo_light = pygame.transform.scale(ammo_light, (64, 64))
    ammo_heavy = pygame.transform.scale(ammo_heavy, (64, 64))
    bullet_light = pygame.transform.scale(bullet_light, (6, 8))
    bullet_heavy = pygame.transform.scale(bullet_heavy, (14, 8))
    coin_stack = pygame.transform.scale(coin_stack, (64, 64))
    mayo_jar = pygame.transform.scale(mayo_jar, (37, 58))
    mayo_jar_bw = pygame.transform.scale(mayo_jar_bw, (37, 58))
    beer_bottle = pygame.transform.scale(beer_bottle, (20, 62))
    beer_bottle_bw = pygame.transform.scale(beer_bottle_bw, (20, 62))
    store_icon = pygame.transform.scale(store_icon, (64, 64))
    mouse_icon = pygame.transform.scale(mouse_icon, (64, 64))
    back = pygame.transform.scale(back, (128, 128))
    star_empty = pygame.transform.scale(star_empty, (48, 48))
    star_filled = pygame.transform.scale(star_filled, (48, 48))

    sprites.update(
        {
            "bg": bg,
            "bg_store": bg_store,
            "bg_pause": bg_pause,
            "ammo_light": ammo_light,
            "ammo_heavy": ammo_heavy,
            "bullet_light": bullet_light,
            "bullet_heavy": bullet_heavy,
            "coin_stack": coin_stack,
            "mayo_jar": mayo_jar,
            "mayo_jar_bw": mayo_jar_bw,
            "beer_bottle": beer_bottle,
            "beer_bottle_bw": beer_bottle_bw,
            "store_icon": store_icon,
            "mouse_icon": mouse_icon,
            "back": back,
            "star_empty": star_empty,
            "star_filled": star_filled,
        }
    )
    return sprites


def init_fonts():
    # Fonts used
    fonts.update(
        {
            "standard_font": pygame.font.SysFont("comicsans", 18, False),
            "bold_font": pygame.font.SysFont("comicsans", 18, True),
            "big_font": pygame.font.SysFont("comicsans", 45, True),
            "big_outline_font": pygame.font.SysFont("comicsans", 49, True),
            "large_font": pygame.font.SysFont("bahnschrift", 100, False),
        }
    )
    return fonts


def init_joysticks():
    joysticks = [
        pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())
    ]
    for joystick in joysticks:
        joystick.init()
    return joysticks


def init_pause_buttons(settings: configparser.ConfigParser):
    def toggle_mute(button: Button):
        new_value = not settings.getboolean("General", "muted")
        settings["General"]["muted"] = str(new_value)
        button.selected = new_value
        if settings.getboolean("General", "muted"):
            pygame.mixer.music.set_volume(0)
        else:
            pygame.mixer.music.set_volume(settings.getint("General", "volume") / 100)

    def toggle_slav_hitbox(button: Button):
        """Toggles the visibility of the box drawn around the player sprite."""
        new_value = not settings.getboolean("Developer Options", "show_player_hitbox")
        settings["Developer Options"]["show_player_hitbox"] = str(new_value)
        button.selected = new_value

    def toggle_cop_hitbox(button: Button):
        """Toggles the visibility of the boxes drawn around the enemy sprites."""
        new_value = not settings.getboolean("Developer Options", "show_cop_hitboxes")
        settings["Developer Options"]["show_cop_hitboxes"] = str(new_value)
        button.selected = new_value

    def unpause(*_):
        variables.paused = False

    def quit_game(*_):
        variables.run = False

    Button("resume [ESC]", "main", on_click=unpause)
    Button("options...", "main", next_menu="options")
    Button("quit", "main", next_menu="quit")
    Button("music options...", "options", next_menu="volume")
    Button("developer options...", "options", next_menu="dev")
    Slider("volume: {vol}", "volume")
    Button(
        "mute background music",
        "volume",
        on_click=toggle_mute,
        selected=settings.getboolean("General", "muted"),
    )
    Button("back... [ESC]", "volume", next_menu="options")
    Button("toggle player hitbox", "dev", on_click=toggle_slav_hitbox)
    Button("toggle enemy hitboxes", "dev", on_click=toggle_cop_hitbox)
    Button("back... [ESC]", ["options", "dev"], next_menu="main")
    Button("no", "quit", next_menu="main")
    Button("yes", "quit", on_click=quit_game)
    for buttons in Button.all.values():
        for button in buttons:
            button.initialise_dimensions(buttons)


def init_weapons():
    Weapon(
        (16, WIN_HEIGHT // 8),
        name="Beretta",
        cost=50,
        damage=20,
        rof=1000,
        full_auto=False,
    )
    Weapon(
        (32, WIN_HEIGHT // 2),
        name="Deagle",
        cost=150,
        damage=60,
        rof=200,
        full_auto=False,
    )
    Weapon(
        (WIN_WIDTH // 2 - 128, WIN_HEIGHT // 2),
        name="MP5",
        cost=200,
        damage=30,
        rof=750,
        full_auto=True,
    )
    Weapon(
        (WIN_WIDTH - 256 - 32, WIN_HEIGHT // 2),
        name="AK-47",
        cost=300,
        damage=50,
        rof=630,
        full_auto=True,
    )
