"""Initialisation code"""

import pygame

from modules.constants import WIN_WIDTH, WIN_HEIGHT, IMAGE_DIR


pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.mixer.init()
pygame.init()

sprites = {}
fonts = {}


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

    sprites.update(
        {
            "bg": bg,
            "bg_store": bg_store,
            "bg_pause": bg_pause,
            "bullet_stack": bullet_stack,
            "coin_stack": coin_stack,
            "mayo_jar": mayo_jar,
            "mayo_jar_bw": mayo_jar_bw,
            "beer_bottle": beer_bottle,
            "beer_bottle_bw": beer_bottle_bw,
            "store_icon": store_icon,
            "mouse_icon": mouse_icon,
            "back": back,
            "star_0": star_0,
            "star_1": star_1,
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
            "large_font": pygame.font.SysFont("comicsans", 100, False),
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
