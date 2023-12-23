"""Class definition for the player character."""

import pygame

from modules import variables, init
from modules.constants import WIN_WIDTH
from modules.classes.human import Human, get_sprite_frames
from modules.classes.purchasables.ability import Ability
from modules.classes.purchasables.weapon import Weapon, get_scaled_image_dimensions


MAX_DIMENSIONS = (16 * 4, 9 * 4)

GUN_SPRITES = {
    gun.name: get_scaled_image_dimensions(gun.image_path, *MAX_DIMENSIONS)
    for gun in Weapon.all
}


# S L A V
class Player(Human):
    """Player character class."""

    frames_right, frames_left = get_sprite_frames(9)

    def __init__(self, x_pos: int, y_pos: int, width: int, height: int):
        super().__init__(x_pos, y_pos, width, height, 0, 1)
        self.jump_stage = 40
        self.jumping = False
        self.status_effects = set()
        self.reset()

    def reset(self):
        """Resets all object properties to their initial state."""
        self.jumping = True
        self.status_effects = set()
        self.velocity = 0
        self.animation_stage = 0
        self.jump_stage = 40
        self.jumping = False
        self.x_pos = self.original_x_pos
        self.y_pos = self.original_y_pos

    def draw(self, win):
        """Renders the player character to the screen."""
        if not variables.paused:
            self.move()
        if self.animation_stage >= 17:
            self.animation_stage = 0
        frames = self.frames_left if self.direction == -1 else self.frames_right
        frame_idx = int(self.animation_stage / 2)
        if not variables.paused:
            self.animation_stage += self.velocity / 10
        win.blit(frames[frame_idx], (self.x_pos, self.y_pos))
        dev_settings = variables.settings["Developer Options"]
        if dev_settings.getboolean("show_player_hitbox"):
            pygame.draw.rect(win, (0, 255, 0), self.hitbox, 2)
        if variables.selected_gun is None or not dev_settings.getboolean(
            "draw_experimental_player_weapon"
        ):
            return
        gun_sprite, dimensions = GUN_SPRITES[variables.selected_gun.name]
        if self.direction == -1:
            gun_sprite = pygame.transform.flip(gun_sprite, True, False)
        gun_hitbox = [
            self.hitbox[0]
            + (self.hitbox[2] - dimensions[0]) // 2
            + (dimensions[0] + 20) * self.direction,
            self.hitbox[1] + 40,
            *dimensions,
        ]
        win.blit(gun_sprite, gun_hitbox)

    def move(self):
        """Move all objects on the screen with the character's movement."""
        velocity_multiplier = 1
        for status_effect in self.status_effects:
            match status_effect:
                case "beer_power":
                    velocity_multiplier *= 0.5
                case "mayo_power":
                    velocity_multiplier *= 2
                case _:
                    break
        distance = self.velocity * self.direction * velocity_multiplier
        if distance == 0:
            return
        if WIN_WIDTH // 3 > self.x_pos + distance > 80:
            self.x_pos += distance
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

    def hit(self, win):
        """Called when killed by cop."""
        # Stops all sound effects
        pygame.mixer.stop()
        self.reset()
        text = init.fonts["large_font"].render("BUSTED", 1, (255, 0, 0))
        win.blit(text, ((WIN_WIDTH // 2) - (text.get_width() // 2), 200))
        pygame.display.update()
        i = 0
        for gun in Weapon.all:
            gun.owned = False
        for powerup in Ability.all:
            powerup.owned = 0
        while i < 100:  # Waits 100 * 10ms (one second)
            pygame.time.delay(10)
            i += 1
            # Checks to see if user has attempted to close v.window during that 1s
            for close_event in pygame.event.get():
                if close_event.type == pygame.QUIT:
                    i = 100
                    variables.paused = True
                    variables.pause_menu = "quit"

    def continue_jump(self):
        """Progresses to the next jump stage when in the process of jumping."""
        if self.jump_stage > -40:
            self.y_pos -= self.jump_stage
            self.jump_stage -= 8
        else:
            self.y_pos -= self.jump_stage
            self.jump_stage = 40
            self.jumping = False
