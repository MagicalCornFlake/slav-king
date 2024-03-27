"""Initialisation code"""

import pygame

from modules import variables
from modules.constants import WIN_WIDTH, WIN_HEIGHT, IMAGE_DIR, FRAME_WIDTH, FRAME_GAP
from modules.classes.button import Button, Slider
from modules.classes.purchasables.weapon import Weapon


pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.mixer.init()
pygame.init()

sprites: dict[str, pygame.Surface] = {}
fonts: dict[str, pygame.font.Font] = {}


def init_window():
    """Initialises the game OS window."""
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
    """Initialises the sprite graphics used within the game UI."""
    sprites["bg_pause"] = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
    sprites["bg_pause"].fill((0, 0, 0))
    sprites["bg_pause"].set_alpha(192)

    sprites["bg"] = pygame.image.load(IMAGE_DIR + "bg_main.png")
    sprites["bg_store"] = pygame.image.load(IMAGE_DIR + "bg_store.png")
    sprites["ammo_light"] = pygame.image.load(IMAGE_DIR + "icon_ammo_light.png")
    sprites["ammo_heavy"] = pygame.image.load(IMAGE_DIR + "icon_ammo_heavy.png")
    sprites["bullet_light"] = pygame.image.load(IMAGE_DIR + "icon_bullet_light.png")
    sprites["bullet_heavy"] = pygame.image.load(IMAGE_DIR + "icon_bullet_heavy.png")
    sprites["coin_stack"] = pygame.image.load(IMAGE_DIR + "icon_coins.png")
    sprites["mayo_jar"] = pygame.image.load(IMAGE_DIR + "icon_mayo.png")
    sprites["mayo_jar_bw"] = pygame.image.load(IMAGE_DIR + "icon_mayo_bw.png")
    sprites["beer_bottle"] = pygame.image.load(IMAGE_DIR + "icon_beer.png")
    sprites["beer_bottle_bw"] = pygame.image.load(IMAGE_DIR + "icon_beer_bw.png")
    sprites["store_icon"] = pygame.image.load(IMAGE_DIR + "icon_store.png")
    sprites["mouse_icon"] = pygame.image.load(IMAGE_DIR + "icon_mouse.png")
    sprites["back"] = pygame.image.load(IMAGE_DIR + "icon_back.png")
    sprites["star_empty"] = pygame.image.load(IMAGE_DIR + "star_empty.png")
    sprites["star_filled"] = pygame.image.load(IMAGE_DIR + "star_filled.png")

    # Scaling of resources
    sprites["bg"] = pygame.transform.scale(sprites["bg"], (960, 540))
    sprites["ammo_light"] = pygame.transform.scale(sprites["ammo_light"], (64, 64))
    sprites["ammo_heavy"] = pygame.transform.scale(sprites["ammo_heavy"], (64, 64))
    sprites["bullet_light"] = pygame.transform.scale(sprites["bullet_light"], (6, 8))
    sprites["bullet_heavy"] = pygame.transform.scale(sprites["bullet_heavy"], (14, 8))
    sprites["coin_stack"] = pygame.transform.scale(sprites["coin_stack"], (64, 64))
    sprites["mayo_jar"] = pygame.transform.scale(sprites["mayo_jar"], (37, 58))
    sprites["mayo_jar_bw"] = pygame.transform.scale(sprites["mayo_jar_bw"], (37, 58))
    sprites["beer_bottle"] = pygame.transform.scale(sprites["beer_bottle"], (20, 62))
    sprites["beer_bottle_bw"] = pygame.transform.scale(
        sprites["beer_bottle_bw"], (20, 62)
    )
    sprites["store_icon"] = pygame.transform.scale(sprites["store_icon"], (128, 128))
    sprites["mouse_icon"] = pygame.transform.scale(sprites["mouse_icon"], (64, 64))
    sprites["back"] = pygame.transform.scale(sprites["back"], (128, 128))
    sprites["star_empty"] = pygame.transform.scale(sprites["star_empty"], (48, 48))
    sprites["star_filled"] = pygame.transform.scale(sprites["star_filled"], (48, 48))

    return sprites


def init_fonts():
    """Initialises the fonts used within the game UI."""
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
    """Initialises each connected joystick/controller device."""
    joysticks = [
        pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())
    ]
    for joystick in joysticks:
        joystick.init()
    return joysticks


def init_pause_buttons():
    """Initialises the buttons displayed in the pause menu."""

    def toggle_mute(button: Button):
        new_value = not variables.settings.getboolean("General", "muted")
        variables.settings["General"]["muted"] = str(new_value)
        button.selected = new_value
        if variables.settings.getboolean("General", "muted"):
            pygame.mixer.music.set_volume(0)
        else:
            pygame.mixer.music.set_volume(
                variables.settings.getint("General", "volume") / 100
            )

    def toggle_slav_hitbox(button: Button):
        """Toggles the visibility of the box drawn around the player sprite."""
        new_value = not variables.settings.getboolean(
            "Developer Options", "show_player_hitbox"
        )
        variables.settings["Developer Options"]["show_player_hitbox"] = str(new_value)
        button.selected = new_value

    def toggle_cop_hitbox(button: Button):
        """Toggles the visibility of the boxes drawn around the enemy sprites."""
        new_value = not variables.settings.getboolean(
            "Developer Options", "show_cop_hitboxes"
        )
        variables.settings["Developer Options"]["show_cop_hitboxes"] = str(new_value)
        button.selected = new_value

    def unpause(*_):
        variables.paused = False

    def quit_game(*_):
        variables.run = False

    Button("resume [ESC]", "main", unpause)
    Button("options...", "main", "options")
    Button("quit", "main", "quit")
    Button("music options...", "options", "volume")
    Button("developer options...", "options", "dev")
    Slider("volume: {vol}", "volume")
    Button(
        "mute background music",
        "volume",
        toggle_mute,
        selected=variables.settings.getboolean("General", "muted"),
    )
    Button("back... [ESC]", "volume", "options")
    Button("toggle player hitbox", "dev", toggle_slav_hitbox)
    Button("toggle enemy hitboxes", "dev", toggle_cop_hitbox)
    Button("back... [ESC]", ["options", "dev"], "main")
    Button("no", "quit", "main")
    Button("yes", "quit", quit_game)
    for buttons in Button.all.values():
        for button in buttons:
            button.initialise_dimensions(buttons)


def init_weapons():
    """Initialises the weapon instances for each purchasable gun."""
    Weapon(
        (FRAME_GAP // 2, WIN_HEIGHT // 8),
        name="Beretta",
        cost=50,
        damage=20,
        rof=1000,
        full_auto=False,
    )
    Weapon(
        (FRAME_GAP, WIN_HEIGHT // 2),
        name="Deagle",
        cost=150,
        damage=60,
        rof=200,
        full_auto=False,
    )
    Weapon(
        ((WIN_WIDTH - FRAME_WIDTH) // 2, WIN_HEIGHT // 2),
        name="MP5",
        cost=200,
        damage=30,
        rof=750,
        full_auto=True,
    )
    Weapon(
        (WIN_WIDTH - FRAME_GAP - FRAME_WIDTH, WIN_HEIGHT // 2),
        name="AK-47",
        cost=300,
        damage=50,
        rof=630,
        full_auto=True,
    )
