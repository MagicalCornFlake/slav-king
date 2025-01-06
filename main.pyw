"""Main module for Slav King."""

import random

import pygame

from modules import setup, init, variables, updater, gui, commandline
from modules.classes.button import Button, Slider
from modules.classes.effect import Effect
from modules.classes.enemy import Enemy
from modules.classes.player import Player
from modules.classes.purchasables.weapon import Weapon
from modules.classes.purchasables.ability import Ability
from modules.classes.purchasables.ammo import AmmoPurchasable
from modules.constants import (
    WIN_WIDTH,
    WIN_HEIGHT,
    PAUSE_INSTRUCTIONS,
    AUDIO_DIR,
    STORE_ICON_PADDING,
    INFINITE_AMMO,
    GOD_MODE,
    WHITE,
    FRAME_WIDTH,
    FRAME_GAP,
)

try:
    from modules.platforms import win_tools as os_tools
except ImportError:
    from modules.platforms import posix_tools as os_tools

if "no-update" not in commandline.get_run_arguments():
    updater.ensure_latest_version()
setup.ensure_singleton()
setup.read_settings()
win = init.init_window()
sprites = init.init_sprites()
fonts = init.init_fonts()
joysticks = init.init_joysticks()
clock = pygame.time.Clock()  # To make calling the method quicker

# Gets the volume from settings and converts it into decimal instead of percentage
volume = (
    0
    if variables.settings.getboolean("General", "muted")
    else variables.settings.getint("General", "volume") / 100
)
pygame.mixer.music.set_volume(volume)
pygame.mixer.music.load(AUDIO_DIR + "music.mp3")
pygame.mixer.music.play(-1)

variables.money_count = variables.settings.getint("Cheats", "start_money")


# RENDER GAME GRAPHICS / SPRITES
def redraw_game_window():
    """Renders the game's graphics to the window."""
    win.blit(sprites["bg"], (variables.win_x, 0))
    if variables.win_x > 0:
        win.blit(sprites["bg"], (variables.win_x - WIN_WIDTH, 0))
    elif variables.win_x < 0:
        win.blit(sprites["bg"], (variables.win_x + WIN_WIDTH, 0))
    for cop_to_draw in variables.cops:
        cop_to_draw.draw(win, slav)
    for drop in variables.drops:
        drop.draw(win, sprites)
    for bullet in variables.bullets:
        bullet.draw(win)
    slav.draw(win)
    score_text = fonts["bold_font"].render(f"score: {variables.score}", 1, WHITE)
    highscore = variables.settings["Cheats"]["highscore"]
    highscore_text = fonts["bold_font"].render(f"highscore: {highscore}", 1, WHITE)
    fps_byte = round(variables.fps / 27) * 255
    fps_colour = (255 - fps_byte, fps_byte, 0)
    fps_counter_text = fonts["bold_font"].render(
        f"{variables.fps:.1f} FPS", 1, fps_colour
    )
    money_count_text = fonts["bold_font"].render(
        f"money: ${variables.money_count}", 1, WHITE
    )
    paused_text = fonts["big_font"].render("PAUSED", 1, WHITE)
    paused_text_outline = fonts["big_outline_font"].render("PAUSED", 1, (0, 0, 0))
    quit_text = fonts["big_font"].render("Are you sure you want to quit?", 1, WHITE)
    for filled_star in range(1, variables.wanted_level + 1):
        win.blit(
            sprites["star_filled"],
            (WIN_WIDTH - 48 * filled_star - 10, WIN_HEIGHT - 48 - 10),
        )
    for empty_star in range(variables.wanted_level + 1, 6):
        win.blit(
            sprites["star_empty"],
            (WIN_WIDTH - 48 * empty_star - 10, WIN_HEIGHT - 48 - 10),
        )
    if variables.paused:
        win.blit(sprites["bg_pause"], (0, 0))
        for button_in_menu in Button.all[variables.pause_menu]:
            if isinstance(button_in_menu, Slider):
                button_in_menu.draw(win)
            else:
                button_in_menu.draw(win)
        if variables.pause_menu == "shop":
            win.blit(sprites["bg_store"], (0, 0))
            win.blit(sprites["back"], (16, WIN_HEIGHT - 16 - 64 - 16))
            for gun in Weapon.all:
                gun.draw(win)
            for ability_icon in Ability.all:
                ability_icon.draw(win)
            if AmmoPurchasable.selected_ammo_idx is not None:
                AmmoPurchasable.get_selected().draw(win)
        elif variables.pause_menu == "quit":
            win.blit(
                quit_text,
                (WIN_WIDTH // 2 - quit_text.get_width() // 2, WIN_HEIGHT // 3),
            )
        else:
            win.blit(
                paused_text_outline,
                (
                    WIN_WIDTH // 2 - paused_text_outline.get_width() // 2,
                    WIN_HEIGHT // 5 + 1,
                ),
            )
            win.blit(
                paused_text,
                (WIN_WIDTH // 2 - paused_text.get_width() // 2, WIN_HEIGHT // 5),
            )
            store_icon = sprites["store_icon"]
            win.blit(store_icon, (0, WIN_HEIGHT - 128))
    elif variables.cop_hovering_over is not None:
        win.blit(sprites["mouse_icon"], variables.cop_hovering_over)
    win.blit(score_text, (WIN_WIDTH - score_text.get_width() - 20, 10))
    win.blit(highscore_text, (WIN_WIDTH - highscore_text.get_width() - 20, 30))
    win.blit(fps_counter_text, (WIN_WIDTH - fps_counter_text.get_width() - 20, 50))
    if AmmoPurchasable.selected_ammo_idx is not None:
        if INFINITE_AMMO:
            ammo_count_text = fonts["bold_font"].render("ammo: ∞", 1, WHITE)
        else:
            ammo_count = AmmoPurchasable.get_selected().owned
            ammo_count_text = fonts["bold_font"].render(f"ammo: {ammo_count}", 1, WHITE)
        win.blit(ammo_count_text, (20, 30))
    win.blit(money_count_text, (20, 10))
    for ability_icon in Ability.all:
        ability_icon.draw_icon(win)
    pygame.display.update()


# Calling classes
init.init_pause_buttons()
init.init_weapons()

slav = Player(128, WIN_HEIGHT - 100 - 256 + 64, 256, 256)

AmmoPurchasable(
    (WIN_WIDTH - (FRAME_GAP * 2 + FRAME_WIDTH * 3) // 4, WIN_HEIGHT // 8),
    "ammo_light",
    cost=25,
    owned=20,
    quantity=5,
)
AmmoPurchasable(
    (WIN_WIDTH - (FRAME_GAP * 2 + FRAME_WIDTH * 3) // 4, WIN_HEIGHT // 8),
    "ammo_heavy",
    cost=49,
    owned=7,
    quantity=7,
)

Ability((FRAME_GAP * 3 // 2 + FRAME_WIDTH, WIN_HEIGHT // 8), name="mayo", cost=50)
Ability(
    (FRAME_GAP * 5 // 2 + FRAME_WIDTH + Ability.all[0].dimensions[2], WIN_HEIGHT // 8),
    name="beer",
    cost=60,
)


def get_key_index(key_name: str) -> int:
    """Returns the integer index corresponding to the key binding name."""
    return pygame.key.key_code(variables.settings["Keybindings"][key_name])


def get_button_index(key_name: str) -> int:
    """Returns the controller button index corresponding to the action name."""
    return {
        "select": 0,
        "back": 1,
        "attack": 2,
        "jump": 3,
        "pause": 7,
    }.get(key_name)


def update_selected_gun(gun: Weapon) -> None:
    """Event handler when the player selects a different gun."""
    if variables.selected_gun != gun:
        Effect("weapon_charge")
    variables.selected_gun = gun
    AmmoPurchasable.selected_ammo_idx = gun.name in ["Deagle", "AK-47"]


def handle_button_presses(mouse_pos: tuple[int, int]):
    """Checks each button if it is hovered, and if so, activates it.

    Returns a boolean telling if any button was pressed."""
    for button in Button.all[variables.pause_menu]:
        # Check if the mouse is within the button's boundary
        if not button.contains_point(mouse_pos):
            continue
        if isinstance(button, Slider):
            variables.slider_engaged = True
            variables.settings["General"]["muted"] = "False"
            Button.all["volume"][1].selected = False
        else:
            variables.slider_engaged = False
            button.do_action()  # Sends message that button was clicked
        return True
    return False


def is_key_pressed(key_name: str):
    """Checks if the given key is currently pressed this frame."""
    directions = {"right": 1, "left": -1}
    direction = directions.get(key_name)

    def check_joystick_movement(joystick: pygame.joystick.Joystick):
        joystick_x_axis = joystick.get_axis(0)
        return abs(joystick_x_axis) > 0.5 and joystick_x_axis * direction > 0

    def check_joystick_buttons(joystick: pygame.joystick.Joystick):
        button = get_button_index(key_name)
        return joystick.get_button(button)

    check_input = (
        check_joystick_buttons if direction is None else check_joystick_movement
    )

    if any(check_input(joystick) for joystick in joysticks):
        return True

    return get_key_index(key_name)


def go_back_in_pause_menu():
    """Handles the pause menu change when the user presses the 'back' button."""
    variables.pause_menu = PAUSE_INSTRUCTIONS[variables.pause_menu]
    if variables.pause_menu == "unpause":
        variables.paused = False
        pygame.mixer.unpause()
    elif variables.pause_menu == "prev":
        variables.pause_menu = variables.previous_pause_menu


def attempt_fire():
    """Checks if it is possible to fire the weapon, and if so, calls the weapon fire method."""
    if (
        variables.shot_cooldown_time_passed >= variables.shot_cooldown
        and variables.selected_gun is not None
    ):
        ammo_count = AmmoPurchasable.get_selected().owned
        if ammo_count > 0 or INFINITE_AMMO:
            variables.selected_gun.fire(slav)
        else:  # Plays empty mag sound effect if space was pressed this frame
            Effect("bullet_empty")
            variables.firing = False


def check_joysticks():
    """Cycles through all connected joysticks and checks if any of them is held."""
    _select_button_held = False
    for joystick in joysticks:
        if joystick.get_button(get_button_index("select")):
            _select_button_held = True
        os_tools.set_cursor_pos(joystick)
    return _select_button_held


def is_select_button_pressed(event: pygame.event.Event):
    """Checks if it was a mouse or controller event, and checks the corresponding select button."""
    return (
        event.button == 1
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP)
        else event.button == get_button_index("select")
    )


def handle_mouse_clicks(mouse_pos: tuple[int, int]):
    """Handles user mouse clicks."""

    if variables.paused and handle_button_presses(mouse_pos):
        return

    # If clicked mouse in game
    for ability in Ability.all:
        if (
            ability.contains_point(mouse_pos, ability.icon_dimensions)
            and ability.owned > 0
            and ability.progress == 0
        ):
            ability.activate(slav)
            return
    if variables.cop_hovering_over is not None:
        if variables.money_count >= 100:
            variables.money_count -= 100
            variables.wanted_level = 0
            Effect("purchase")

        else:
            Effect("error")
        return

    # Clicking "enter shop" icon
    if variables.pause_menu != "shop":
        # If clicked shop icon
        if (
            STORE_ICON_PADDING <= mouse_pos[0] <= 128 - STORE_ICON_PADDING
            and WIN_HEIGHT - STORE_ICON_PADDING - 128
            < mouse_pos[1]
            < WIN_HEIGHT - STORE_ICON_PADDING
        ):
            # Enter shop
            variables.previous_pause_menu = variables.pause_menu
            variables.pause_menu = "shop"
        return

    # If clicked mouse in shop
    if (
        16 < mouse_pos[0] < 16 + 128
        and WIN_HEIGHT - 16 - 64 < mouse_pos[1] < WIN_HEIGHT - 16
    ):
        # Go back
        variables.pause_menu = variables.previous_pause_menu
        return
    # If clicked on a gun
    for gun_item in Weapon.all:
        if not gun_item.contains_point(mouse_pos):
            continue
        if gun_item.owned:
            update_selected_gun(gun_item)
            continue
        if gun_item.affordable:
            gun_item.owned = True
            variables.money_count -= gun_item.cost
            Effect("purchase")
            update_selected_gun(gun_item)
        else:
            Effect("error")
            gun_item.flash()
    # If clicked on a powerup
    for usable_powerup in Ability.all:
        if not usable_powerup.contains_point(mouse_pos):
            continue
        if usable_powerup.affordable:
            usable_powerup.owned += 1
            variables.money_count -= usable_powerup.cost
            Effect("purchase")
        else:
            Effect("error")
            usable_powerup.flash()
    # If clicked on another purchasable
    if AmmoPurchasable.selected_ammo_idx is None:
        return
    ammo_purchasable = AmmoPurchasable.get_selected()
    if ammo_purchasable.contains_point(mouse_pos):
        if ammo_purchasable.affordable:
            variables.money_count -= ammo_purchasable.cost
            ammo_purchasable.owned += ammo_purchasable.quantity
            Effect("purchase")
            Effect("weapon_charge")
        else:
            Effect("error")
            ammo_purchasable.flash()


def handle_pygame_event(event: pygame.event.Event, mouse_pos: tuple[int, int]):
    """Handles the given Pygame event."""
    match (event.type):
        case pygame.QUIT:
            # If user clicks red 'x_pos' button to close
            variables.paused = True
            variables.pause_menu = "quit"
        case pygame.KEYDOWN | pygame.JOYBUTTONDOWN:
            # If the attack key was pressed this frame
            user_input, get_index_function = (
                (event.key, get_key_index)
                if event.type == pygame.KEYDOWN
                else (event.button, get_button_index)
            )
            # If escape was pressed this frame
            if variables.paused:
                if user_input == get_index_function("back"):
                    # Defines what pressing the escape key should do inside pause menu
                    go_back_in_pause_menu()
                    return
            elif user_input == get_index_function("pause"):
                # Pauses game if escape is pressed
                variables.paused = True
                variables.pause_menu = "main"
                pygame.mixer.pause()
                return
            elif user_input == get_index_function("attack"):
                attempt_fire()
                return
            else:
                for ability in Ability.all:
                    if (
                        ability.owned > 0
                        and ability.progress == 0
                        and user_input == get_index_function("activate_" + ability.name)
                    ):
                        ability.activate(slav)
                        break
            if user_input == get_index_function("open_shop"):
                if variables.paused and variables.pause_menu == "shop":
                    variables.paused = False
                else:
                    variables.paused = True
                    variables.pause_menu = "shop"
                    variables.previous_pause_menu = "main"
        # Sound effect code
        case pygame.KEYUP:
            if variables.firing and event.key == get_key_index("attack"):
                variables.firing = False
        case pygame.JOYBUTTONUP:
            if variables.firing and event.button == get_button_index("attack"):
                variables.firing = False
        case pygame.MOUSEBUTTONDOWN | pygame.JOYBUTTONDOWN:
            # If a mouse button is pressed this frame
            if is_select_button_pressed(event):
                handle_mouse_clicks(mouse_pos)
        case pygame.MOUSEBUTTONUP | pygame.JOYBUTTONUP:
            if not variables.slider_engaged:
                return
            if is_select_button_pressed(event):
                variables.slider_engaged = False
        case _:
            pass


def cycle_cops(mouse_pos: tuple[int, int]):
    """Checks events for each cop."""
    variables.cop_hovering_over = None
    # If player touches any cop
    for cop in variables.cops:
        # If any bullet touches any cop
        for fired_bullet in variables.bullets:
            if not cop.contains_point((fired_bullet.x_pos, fired_bullet.y_pos)):
                continue
            cop.hit(slav.status_effects)
            variables.score += 1
            variables.bullets.remove(fired_bullet)
            break

        if variables.wanted_level == 0:
            continue
        if cop.contains_point(mouse_pos):
            variables.cop_hovering_over = mouse_pos
        if GOD_MODE or not cop.within_range_of(slav) or cop.animation_stage < 30:
            continue
        slav.hit(win)
        variables.firing = False
        variables.score = 0
        for ammo_purchasable in AmmoPurchasable.all:
            ammo_purchasable.owned = ammo_purchasable.initial_owned_amount
        for ability in Ability.all:
            ability.progress = 0
        AmmoPurchasable.selected_ammo_idx = None
        variables.money_count = variables.settings.getint("Cheats", "start_money")
        variables.wanted_level = 0
        variables.cops = []
        variables.cop_amount = 1
        variables.bullets = []
        variables.drops = []
        variables.selected_gun = None
        variables.cop_hovering_over = None


def cycle_loot_drops():
    """Handle events for all loot drops."""
    # If player touches ammo drop
    for loot_drop in variables.drops:
        if (
            slav.hitbox[1] < loot_drop.hitbox[1] + loot_drop.hitbox[3]
            and slav.hitbox[1] + slav.hitbox[3] > loot_drop.hitbox[1]
        ):
            if (
                slav.hitbox[0] + slav.hitbox[2] > loot_drop.hitbox[0]
                and slav.hitbox[0] < loot_drop.hitbox[0] + loot_drop.hitbox[2]
            ):
                play_coin_pickup_sound = True
                if loot_drop.loot_type.startswith("ammo"):
                    ammo_idx = ("ammo_light", "ammo_heavy").index(loot_drop.loot_type)
                    ammo_type = AmmoPurchasable.all[ammo_idx]
                    ammo_type.owned += loot_drop.pickup_amount
                    if ammo_idx == AmmoPurchasable.selected_ammo_idx:
                        Effect("weapon_charge")
                        play_coin_pickup_sound = False
                else:
                    variables.money_count += loot_drop.pickup_amount
                if play_coin_pickup_sound:
                    # Plays random coin pickup sound
                    effect_number = random.randint(1, 10)
                    Effect(f"money_pickup{effect_number}")
                # Deletes loot drop sprite after collecting it
                variables.drops.remove(loot_drop)


def tick():
    """Main game loop."""
    clock.tick(27)  # Loops every 1/27 seconds (27 FPS)
    variables.fps = clock.get_fps()
    keys = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()

    for pygame_event in pygame.event.get():
        handle_pygame_event(pygame_event, mouse_pos)

    # If dragging volume slider
    if variables.slider_engaged and (
        check_joysticks() or pygame.mouse.get_pressed(num_buttons=3)[0]
    ):
        # Converts mouse position on slider into volume percentage
        temp_volume = int(
            (mouse_pos[0] - (WIN_WIDTH // 2 - WIN_WIDTH / 4)) / (WIN_WIDTH // 2) * 100
        )

        # Changes the volume setting with a minimum of 0% and maximum of 100%
        variables.settings["General"]["volume"] = str(max(min(temp_volume, 100), 0))
        pygame.mixer.music.set_volume(
            variables.settings.getint("General", "volume") / 100
        )

    # GAME LOGIC
    if not variables.paused:
        variables.shot_cooldown_time_passed += 1 / 27  # Seconds
        if (
            variables.firing
            and variables.selected_gun is not None
            and variables.selected_gun.full_auto
        ):
            attempt_fire()
        if len(variables.cops) < variables.cop_amount:
            if (
                variables.time_passed_since_last_cop_spawned
                >= variables.cop_spawn_delay
            ):
                variables.cops.append(
                    Enemy(
                        WIN_WIDTH - 1,
                        WIN_HEIGHT - random.randint(92, 112) - 256 + 64,
                        256,
                        256,
                        75,
                    )
                )
                variables.time_passed_since_last_cop_spawned = 0
                variables.cop_spawn_delay = random.randint(500, 3000) / 1000
            else:
                variables.time_passed_since_last_cop_spawned += 1 / 27

        # Continues the activation animation of each powerup if it has already been started
        for ability in Ability.all:
            if ability.progress > 0:
                ability.activate(slav)

        for fired_bullet in variables.bullets:
            if 0 < fired_bullet.x_pos < WIN_WIDTH:
                fired_bullet.x_pos += fired_bullet.velocity * fired_bullet.direction
            else:
                variables.bullets.remove(fired_bullet)
                continue
        cycle_cops(mouse_pos)
        cycle_loot_drops()

        # Moving left
        if keys[is_key_pressed("left")] or keys[pygame.K_LEFT]:
            slav.direction = -1
            slav.velocity = 10
        # Moving right
        elif keys[is_key_pressed("right")] or keys[pygame.K_RIGHT]:
            slav.direction = 1
            slav.velocity = 10
        # Not moving
        else:
            slav.animation_stage = 0
            slav.velocity = 0
        # Jumping
        if slav.jumping:
            slav.continue_jump()
        elif keys[is_key_pressed("jump")] or keys[pygame.K_UP]:
            slav.jumping = True

        if variables.score > variables.settings.getint("Cheats", "highscore"):
            # Updates high score if user has surpassed it
            variables.settings["Cheats"]["highscore"] = str(variables.score)
    redraw_game_window()


gui.hide_root()


while variables.run:
    tick()


pygame.quit()
setup.write_settings()
setup.cleanup()
