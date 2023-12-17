"""Main module for Slav King."""
import pygame
import random

from modules import setup, init
from modules.classes.ability import Ability
from modules.classes.button import Button, Slider
from modules.classes.effect import Effect
from modules.classes.enemy import Enemy
from modules.classes.player import Player
from modules.classes.projectile import Projectile
from modules.classes.weapon import Weapon
from modules.classes.purchasables.ability import AbilityPurchasable
from modules.classes.purchasables.ammo import AmmoPurchasable
from modules.constants import WIN_WIDTH, WIN_HEIGHT, PAUSE_INSTRUCTIONS
from modules import variables

try:
    from modules import win_tools as os_tools
except ImportError:
    from modules import posix_tools as os_tools

setup.ensure_singleton()
settings = setup.read_settings()
win = init.init_window()
sprites = init.init_sprites()
fonts = init.init_fonts()
joysticks = init.init_joysticks()
clock = pygame.time.Clock()  # To make calling the method quicker

cop_spawn_delay = random.randint(500, 2500) / 1000

# Gets the volume from settings and converts it into decimal instead of percentage
volume = 0 if settings["muted"] else settings["volume"] / 100
pygame.mixer.music.set_volume(volume)

# Cheats - Change these :D
god_mode = False
INFINITE_AMMO = False
money_count = settings["start_money"]


def move(distance):
    """Move all objects on the screen with the character's movement."""
    if WIN_WIDTH // 3 > slav.x_pos + distance > 80:
        slav.x_pos += distance
        return
    if variables.win_x > WIN_WIDTH:
        variables.win_x = 0
    if variables.win_x < -WIN_WIDTH:
        variables.win_x = 0
    variables.win_x -= distance
    for cop_to_move in variables.cops:
        cop_to_move.x_pos -= distance
    for bullet in variables.bullets:
        bullet.x_pos -= distance
    for drop in variables.drops:
        drop.x_pos -= distance


def fire():
    variables.sounds.append(Effect("bullet_fire_" + variables.selected_gun.name))
    if variables.shot_cooldown_time_passed >= variables.shot_cooldown:
        # Makes the script wait a certain amount of time before a gun is able to fire again (rof = Rate of Fire)
        rate_of_fire = variables.selected_gun.rof / 60  # rounds per second
        shot_interval = 1 / rate_of_fire  # seconds
        variables.shot_cooldown_time_passed = 0
        variables.shot_cooldown = shot_interval
        # Makes the bullet travel in the direction the player is facing
        if slav.left:
            facing = -1
        else:
            facing = 1
        # Fires bullet
        variables.bullets.append(
            Projectile(
                (
                    round(slav.x_pos + slav.width // 2),
                    round(slav.y_pos + slav.height // 2.5),
                ),
                3,
                (0, 0, 0),
                facing,
            )
        )
        if not INFINITE_AMMO:
            variables.ammo_count -= 1
    variables.firing = True


# RENDER GAME GRAPHICS / SPRITES
def redraw_game_window(cop_hovering_over):
    win.blit(sprites["bg"], (variables.win_x, 0))
    if variables.win_x > 0:
        win.blit(sprites["bg"], (variables.win_x - WIN_WIDTH, 0))
    elif variables.win_x < 0:
        win.blit(sprites["bg"], (variables.win_x + WIN_WIDTH, 0))
    for cop_to_draw in variables.cops:
        cop_to_draw.draw(win, slav, settings)
    slav.draw(win, settings)
    for drop in variables.drops:
        drop.draw(win, sprites)
    for bullet in variables.bullets:
        bullet.draw(win)
    score_text = fonts["bold_font"].render(
        "score: " + str(variables.score), 1, [255] * 3
    )
    highscore_text = fonts["bold_font"].render(
        "highscore: " + str(settings["highscore"]), 1, [255] * 3
    )
    fps_counter_text = fonts["bold_font"].render(
        str(round(variables.fps)) + " FPS",
        1,
        (255 - round(variables.fps / 27 * 255), round(variables.fps / 27 * 255), 0),
    )
    if INFINITE_AMMO:
        ammo_count_text = fonts["bold_font"].render("ammo: infinite", 1, [255] * 3)
    else:
        ammo_count_text = fonts["bold_font"].render(
            "ammo: " + str(variables.ammo_count), 1, [255] * 3
        )
    money_count_text = fonts["bold_font"].render(
        "money: $" + str(money_count), 1, [255] * 3
    )
    paused_text = fonts["big_font"].render("PAUSED", 1, [255] * 3)
    paused_text_outline = fonts["big_outline_font"].render("PAUSED", 1, (0, 0, 0))
    quit_text = fonts["big_font"].render("Are you sure you want to quit?", 1, [255] * 3)
    for filled_star in range(1, variables.wanted_level + 1):
        win.blit(
            sprites["star_1"], (WIN_WIDTH - 32 * filled_star - 10, WIN_HEIGHT - 32 - 10)
        )
    for empty_star in range(variables.wanted_level + 1, 6):
        win.blit(
            sprites["star_0"], (WIN_WIDTH - 32 * empty_star - 10, WIN_HEIGHT - 32 - 10)
        )
    if variables.paused:
        win.blit(sprites["bg_pause"], (0, 0))
        for button_in_menu in buttons[variables.pause_menu]:
            arg = settings if isinstance(button_in_menu, Slider) else buttons
            button_in_menu.draw(
                win,
                arg,
            )
        if variables.pause_menu == "shop":
            win.blit(sprites["bg_store"], (0, 0))
            win.blit(sprites["back"], (16, WIN_HEIGHT - 16 - 64 - 16))
            for gun in guns:
                gun.draw(win)
            for powerup in purchasable_powerups:
                powerup.draw(win)
            for purchasable_item in variables.purchasables:
                purchasable_item.draw(win)
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
            win.blit(sprites["store_icon"], (16, WIN_HEIGHT - 16 - 64))
    elif cop_hovering_over is not None:
        win.blit(sprites["mouse_icon"], cop_hovering_over)
    win.blit(score_text, (WIN_WIDTH - score_text.get_width() - 20, 10))
    win.blit(highscore_text, (WIN_WIDTH - highscore_text.get_width() - 20, 30))
    win.blit(fps_counter_text, (WIN_WIDTH - fps_counter_text.get_width() - 20, 50))
    win.blit(ammo_count_text, (20, 10))
    win.blit(money_count_text, (20, 30))
    for powerup_shop_icon in powerups:
        powerup_shop_icon.draw(win, sprites, purchasable_powerups)
    pygame.display.update()


# Calling classes
slav = Player(128, WIN_HEIGHT - 100 - 256 + 64, 256, 256)


def toggle_mute():
    button_mute_music.selected = settings["muted"] = not settings["muted"]
    if settings["muted"]:
        pygame.mixer.music.set_volume(0)
    else:
        pygame.mixer.music.set_volume(settings["volume"] / 100)


def toggle_slav_hitbox():
    """Toggles the visibility of the box drawn around the player sprite."""
    settings["showPlayerHitbox"] = not settings["showPlayerHitbox"]
    button_toggle_slav_hitbox.selected = settings["showPlayerHitbox"]


def toggle_cop_hitbox():
    """Toggles the visibility of the boxes drawn around the enemy sprites."""
    settings["showCopHitboxes"] = not settings["showCopHitboxes"]
    button_toggle_cop_hitbox.selected = settings["showCopHitboxes"]


def unpause():
    variables.paused = False


def quit_game():
    variables.run = False


button_resume = Button("resume [ESC]", fonts, on_click=unpause)
button_options = Button("options...", fonts, next_menu="options")
button_quit = Button("quit", fonts, next_menu="quit")
button_volume = Button("music options...", fonts, next_menu="volume")
button_options_dev = Button("developer options...", fonts, next_menu="dev")
button_back = Button("back... [ESC]", fonts, next_menu="main")
slider_volume = Slider("volume: {vol}", fonts)
button_mute_music = Button(
    "mute background music", fonts, on_click=toggle_mute, selected=settings["muted"]
)
button_back_volume = Button("back... [ESC]", fonts, next_menu="options")
button_toggle_slav_hitbox = Button(
    "toggle player hitbox", fonts, on_click=toggle_slav_hitbox
)
button_toggle_cop_hitbox = Button(
    "toggle enemy hitboxes", fonts, on_click=toggle_cop_hitbox
)
button_no = Button("no", fonts, next_menu="main")
button_yes = Button("yes", fonts, on_click=quit_game)

buttons = {
    "main": [button_resume, button_options, button_quit],
    "options": [button_volume, button_options_dev, button_back],
    "volume": [slider_volume, button_mute_music, button_back_volume],
    "dev": [button_toggle_slav_hitbox, button_toggle_cop_hitbox, button_back],
    "quit": [button_no, button_yes],
    "shop": [],
}

gun_beretta = Weapon(
    (16, WIN_HEIGHT // 8),
    name="Beretta",
    fonts=fonts,
    cost=50,
    dmg=20,
    rof=1000,
    full_auto=False,
    money_count=money_count,
)
gun_deagle = Weapon(
    (32, WIN_HEIGHT // 2),
    name="Deagle",
    fonts=fonts,
    cost=150,
    dmg=60,
    rof=200,
    full_auto=False,
    money_count=money_count,
)
gun_mp5 = Weapon(
    (WIN_WIDTH // 2 - 128, WIN_HEIGHT // 2),
    name="MP5",
    fonts=fonts,
    cost=200,
    dmg=30,
    rof=750,
    full_auto=True,
    money_count=money_count,
)
gun_ak47 = Weapon(
    (WIN_WIDTH - 256 - 32, WIN_HEIGHT // 2),
    name="AK-47",
    fonts=fonts,
    cost=300,
    dmg=50,
    rof=630,
    full_auto=True,
    money_count=money_count,
)
guns = [
    gun_beretta,
    gun_deagle,
    gun_mp5,
    gun_ak47,
]

purchasable_light_ammo = AmmoPurchasable(
    WIN_WIDTH - 16 - 176, WIN_HEIGHT // 8, fonts, money_count, cost=75
)
purchasable_heavy_ammo = AmmoPurchasable(
    WIN_WIDTH - 16 - 176, WIN_HEIGHT // 8, fonts, money_count, cost=100
)

purchasable_powerup_mayo = AbilityPurchasable(
    16 * 2 + 256, WIN_HEIGHT // 8, fonts, money_count, name="mayo", cost=50
)
purchasable_powerup_beer = AbilityPurchasable(
    16 * 3 + 256 + 224, WIN_HEIGHT // 8, fonts, money_count, name="beer", cost=100
)
purchasable_powerups = [purchasable_powerup_mayo, purchasable_powerup_beer]

powerup_mayo = Ability(20, 75, fonts, "mayo")
powerup_beer = Ability(20, 75 + 100, fonts, "beer")
powerups = [powerup_mayo, powerup_beer]


def get_key_index(key_name: str) -> int:
    """Returns the integer index corresponding to the key binding name."""
    return setup.key_index[settings[key_name]]


def get_button_index(key_name: str) -> int:
    """Returns the controller button index corresponding to the action name."""
    return {
        "select_key": 0,
        "back_key": 1,
        "attack_key": 2,
        "jump_key": 3,
        "pause_key": 7,
    }.get(key_name)


def update_selected_gun(gun: Weapon) -> None:
    variables.selected_gun = gun
    if gun.name in ["Beretta", "MP5"]:
        variables.purchasables = [purchasable_light_ammo]
    elif gun.name in ["Deagle", "AK-47"]:
        variables.purchasables = [purchasable_heavy_ammo]


# MAIN LOOP
while variables.run:
    clock.tick(27)  # Loops every 1/27 seconds (27 FPS)
    variables.fps = clock.get_fps()
    keys = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()

    def is_key_pressed(key_name: str):
        """Checks if the given key is currently pressed this frame."""
        directions = {"right_key": 1, "left_key": -1}
        direction = directions.get(key_name)

        def check_joystick_movement(joystick: pygame.joystick.Joystick):
            joystick_x_axis = joystick.get_axis(0)
            return abs(joystick_x_axis) > 0.5 and joystick_x_axis * direction > 0

        def check_joystick_buttons(joystick: pygame.joystick.Joystick):
            button = get_button_index(key_name)
            if button is None:
                print("Key name", key_name, "not programmed in! Developer error")
                return
            return joystick.get_button(button)

        check_input = (
            check_joystick_buttons if direction is None else check_joystick_movement
        )

        if any(check_input(joystick) for joystick in joysticks):
            return True

        return keys[get_key_index(key_name)]

    def go_back_in_pause_menu():
        variables.pause_menu = PAUSE_INSTRUCTIONS[variables.pause_menu]
        if variables.pause_menu == "unpause":
            variables.paused = False
            pygame.mixer.unpause()
        elif variables.pause_menu == "prev":
            variables.pause_menu = variables.previous_pause_menu

    def attempt_fire() -> None:
        if (
            variables.shot_cooldown_time_passed >= variables.shot_cooldown
            and variables.selected_gun is not None
        ):
            if variables.ammo_count > 0 or INFINITE_AMMO:
                fire()
            else:  # Plays empty mag sound effect if space was pressed this frame
                variables.sounds.append(Effect("bullet_empty"))
                variables.firing = False

    # Detects window updates
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If user clicks red 'x_pos' button to close
            variables.paused = True
            variables.pause_menu = "quit"
        elif event.type in [pygame.KEYDOWN, pygame.JOYBUTTONDOWN]:
            # If the attack key was pressed this frame
            user_input, get_index_function = (
                (event.key, get_key_index)
                if event.type == pygame.KEYDOWN
                else (event.button, get_button_index)
            )
            if user_input == get_index_function("attack_key"):
                attempt_fire()
            # If escape was pressed this frame
            elif (
                user_input == get_index_function("pause_key")
                or variables.paused
                and user_input == get_index_function("back_key")
            ):
                if variables.paused:
                    # Defines what pressing the escape key should do inside pause menu
                    go_back_in_pause_menu()
                else:  # Pauses game if escape is pressed
                    variables.paused = True
                    variables.pause_menu = "main"
                    pygame.mixer.pause()
        # Sound effect code
        elif variables.firing and (
            event.type == pygame.KEYUP
            and event.key == get_key_index("attack_key")
            or event.type == pygame.JOYBUTTONUP
            and event.button == get_button_index("attack_key")
        ):
            variables.firing = False

        # If a mouse button is pressed this frame
        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) or (
            event.type == pygame.JOYBUTTONDOWN
            and event.button == get_button_index("select_key")
        ):
            # If clicked mouse in pause menu
            if variables.paused:
                for button in buttons[variables.pause_menu]:
                    dim = button.dimensions
                    # Check if the mouse is within the button's boundary
                    if (
                        dim[0] < mouse_pos[0] < dim[0] + dim[2]
                        and dim[1] < mouse_pos[1] < dim[1] + dim[3]
                    ):
                        variables.slider_engaged = button is slider_volume
                        if button is slider_volume:
                            settings["muted"] = False
                            button_mute_music.selected = False
                        else:
                            button.do_action()  # Sends message that button was clicked
                        break  # Not sure if this is needed but it can't do any harm

            # If clicked mouse in game
            else:
                for powerup_icon in powerups:
                    dim = powerup_icon.dimensions
                    if (
                        dim[0] < mouse_pos[0] < dim[0] + dim[2]
                        and dim[1] < mouse_pos[1] < dim[1] + dim[3]
                        and powerup_icon.owned > 0
                        and powerup_icon.progress == 0
                    ):
                        powerup_icon.activate(slav, purchasable_powerups)
                        variables.sounds.append(Effect("mayo"))
                        variables.sounds.append(Effect("eating"))
                if variables.cop_hovering_over is not None:
                    if money_count >= 100:
                        money_count -= 100
                        variables.wanted_level = 0
                        variables.sounds.append(Effect("purchase"))

                    else:
                        variables.sounds.append(Effect("error"))
            # If clicked mouse in shop
            if variables.pause_menu == "shop":
                if (
                    16 < mouse_pos[0] < 16 + 128
                    and WIN_HEIGHT - 16 - 64 < mouse_pos[1] < WIN_HEIGHT - 16
                ):
                    # Go back
                    variables.pause_menu = variables.previous_pause_menu
                else:
                    # If clicked on a gun
                    for gun_icon in guns:
                        dim = gun_icon.outer_hitbox
                        if (
                            dim[0] < mouse_pos[0] < dim[0] + dim[2]
                            and dim[1] < mouse_pos[1] < dim[1] + dim[3]
                        ):
                            if gun_icon.owned:
                                update_selected_gun(gun_icon)
                            else:
                                if gun_icon.affordable:
                                    gun_icon.owned = True
                                    money_count -= gun_icon.cost
                                    variables.sounds.append(Effect("purchase"))
                                    update_selected_gun(gun_icon)
                                else:
                                    variables.sounds.append(Effect("error"))
                                    gun_icon.flash()
                        gun_icon.affordable = money_count >= gun_icon.cost
                    # If clicked on a powerup
                    for usable_powerup in purchasable_powerups:
                        dim = usable_powerup.outer_hitbox
                        if (
                            dim[0] < mouse_pos[0] < dim[0] + dim[2]
                            and dim[1] < mouse_pos[1] < dim[1] + dim[3]
                        ):
                            if usable_powerup.affordable:
                                usable_powerup.owned += 1
                                money_count -= usable_powerup.cost
                                variables.sounds.append(Effect("purchase"))
                            else:
                                variables.sounds.append(Effect("error"))
                                usable_powerup.flash()
                        usable_powerup.affordable = money_count >= usable_powerup.cost
                    # If clicked on another purchasable
                    for purchasable in variables.purchasables:
                        dim = purchasable.outer_hitbox
                        if (
                            dim[0] < mouse_pos[0] < dim[0] + dim[2]
                            and dim[1] < mouse_pos[1] < dim[1] + dim[3]
                        ):
                            if purchasable.affordable:
                                money_count -= purchasable.cost
                                variables.ammo_count += 15
                                variables.sounds.append(Effect("purchase"))
                            else:
                                variables.sounds.append(Effect("error"))
                                purchasable.flash()
                        purchasable.affordable = money_count >= purchasable.cost

            # If clicked shop icon
            elif (
                16 < mouse_pos[0] < 16 + 64
                and WIN_HEIGHT - 16 - 64 < mouse_pos[1] < WIN_HEIGHT - 16
            ):
                # Enter shop
                variables.previous_pause_menu = variables.pause_menu
                variables.pause_menu = "shop"
                for gun_icon in guns:
                    gun_icon.affordable = money_count >= gun_icon.cost
                for usable_powerup in purchasable_powerups:
                    usable_powerup.affordable = money_count >= usable_powerup.cost
                for purchasable in variables.purchasables:
                    purchasable.affordable = money_count >= purchasable.cost
        elif variables.slider_engaged and (
            event.type == pygame.MOUSEBUTTONUP
            and event.button == 1
            or event.type == pygame.JOYBUTTONUP
            and event.button == get_button_index("select_key")
        ):
            variables.slider_engaged = False

    # If dragging volume slider
    if variables.slider_engaged and (
        select_button_held or pygame.mouse.get_pressed(num_buttons=3)[0]
    ):
        # Converts mouse position on slider into volume percentage
        temp_volume = int(
            (mouse_pos[0] - (WIN_WIDTH // 2 - WIN_WIDTH / 4)) / (WIN_WIDTH // 2) * 100
        )

        # Changes the volume setting with a minimum of 0% and maximum of 100%
        if 0 <= temp_volume <= 100:
            settings["volume"] = temp_volume
        elif temp_volume < 0:
            settings["volume"] = 0
        elif temp_volume > 100:
            settings["volume"] = 100
        pygame.mixer.music.set_volume(settings["volume"] / 100)

    # print(mouse_abs_pos)
    select_button_held = False
    for joystick in joysticks:
        if joystick.get_button(get_button_index("select_key")):
            select_button_held = True
        os_tools.set_cursor_pos(joystick)
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
            if variables.time_passed_since_last_cop_spawned >= cop_spawn_delay:
                variables.cops.append(
                    Enemy(
                        WIN_WIDTH - 1,
                        WIN_HEIGHT - random.randint(92, 112) - 256 + 64,
                        256,
                        256,
                    )
                )
                variables.time_passed_since_last_cop_spawned = 0
                cop_spawn_delay = random.randint(500, 3000) / 1000
            else:
                variables.time_passed_since_last_cop_spawned += 1 / 27

        # Continues the activation animation of each powerup if it has already been started
        for powerup_icon in powerups:
            if powerup_icon.progress > 0:
                powerup_icon.activate(slav, purchasable_powerups)

        variables.cop_hovering_over = None
        # If player touches any cop
        for cop in variables.cops:
            if variables.wanted_level > 0:
                if cop.touching_point(mouse_pos):
                    variables.cop_hovering_over = (mouse_pos[0], mouse_pos[1])
                if (
                    not god_mode
                    and cop.touching_hitbox(slav.hitbox)
                    and 29 >= cop.walk_count >= 24
                ):
                    slav.hit(win, fonts, guns, purchasable_powerups)
                    for powerup_icon in powerups:
                        powerup_icon.progress = 0
                    variables.firing = False
                    variables.score = 0
                    variables.ammo_count = 20
                    money_count = settings["start_money"]
                    variables.wanted_level = 0
                    variables.cops = []
                    variables.cop_amount = 1
                    variables.bullets = []
                    variables.drops = []
                    variables.purchasables = []
                    variables.selected_gun = None
                    variables.mayo_power = False
                    variables.cop_hovering_over = None
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
                    if loot_drop.loot_type == "ammo":
                        variables.sounds.append(Effect("bullet_pickup"))
                        variables.ammo_count += loot_drop.pickup_amount
                    else:
                        # Plays random coin pickup sound
                        effect_number = random.randint(1, 10)
                        variables.sounds.append(
                            Effect("money_pickup" + str(effect_number))
                        )
                        money_count += loot_drop.pickup_amount
                        # Updates consumable affordability after picking up money
                        for gun_icon in guns:
                            gun_icon.affordable = money_count >= gun_icon.cost
                        for usable_powerup in purchasable_powerups:
                            usable_powerup.affordable = (
                                money_count >= usable_powerup.cost
                            )
                    # Deletes loot drop sprite after collecting it
                    variables.drops.remove(loot_drop)
        # If any bullet touches any cop
        for fired_bullet in variables.bullets:
            if 0 < fired_bullet.x_pos < WIN_WIDTH:
                fired_bullet.x_pos += fired_bullet.vel
            else:
                try:
                    variables.bullets.remove(fired_bullet)
                    continue
                except ValueError as e:
                    print("Uh oh. Idk what this error is. Exception:", e)
            for cop in variables.cops:
                if cop.touching_point((fired_bullet.x_pos, fired_bullet.y_pos)):
                    cop.hit()
                    variables.score += 1
                    variables.bullets.remove(fired_bullet)
                    break
        # Moving left
        if is_key_pressed("left_key") or keys[pygame.K_LEFT]:
            move(-slav.vel)
            slav.left = True
            slav.right = False
            slav.standing = False
        # Moving right
        elif is_key_pressed("right_key") or keys[pygame.K_RIGHT]:
            move(slav.vel)
            slav.right = True
            slav.left = False
            slav.standing = False
        # Not moving
        else:
            slav.standing = True
            slav.walk_count = 0
        # Jumping
        if not slav.jumping:
            if is_key_pressed("jump_key") or keys[pygame.K_UP]:
                slav.jumping = True
        elif slav.jump_count > -40:
            slav.y_pos -= slav.jump_count
            slav.jump_count -= 8
        else:
            slav.y_pos -= slav.jump_count
            slav.jump_count = 40
            slav.jumping = False

        if variables.score > settings["highscore"]:
            # Updates high score if user has surpassed it
            settings["highscore"] = variables.score
    redraw_game_window(variables.cop_hovering_over)
pygame.quit()
setup.finish(settings)
