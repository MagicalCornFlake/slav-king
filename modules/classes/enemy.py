"""Class definition for the cop characters."""

import random

import pygame

from modules import variables
from modules.constants import (
    WIN_WIDTH,
    WIN_HEIGHT,
    LOOT_TABLE,
    MAX_RENDERED_DROPS,
    RED,
    BLUE,
)
from modules.classes.effect import Effect
from modules.classes.loot_drop import LootDrop
from modules.classes.human import Human, get_sprite_frames


FRAMES_RIGHT, FRAMES_LEFT = get_sprite_frames(11, "E")


# P O L I C E
class Enemy(Human):
    """Cop enemy class."""

    all: list["Enemy"] = []

    def __init__(
        self, x_pos: int, y_pos: int, width: int, height: int, weapon_range: int
    ):
        super().__init__(x_pos, y_pos, width, height, 0, -1)
        self.weapon_range = weapon_range
        self.health = 100
        self.sprite_area = [self.x_pos, self.y_pos, 256, 256]
        self.all.append(self)

    def draw(self, win, slav):
        """Renders character to screen."""
        if not variables.paused:
            self.move(slav)
        if (
            self.animation_stage >= 24 and not self.within_range_of(slav)
        ) or self.animation_stage > 32:
            self.animation_stage = 0

        frames = FRAMES_RIGHT if self.direction == 1 else FRAMES_LEFT
        win.blit(frames[self.animation_stage // 3], (self.x_pos, self.y_pos))
        if self.velocity != 0 and not variables.paused:
            self.animation_stage += 1
        # Drawing health bar
        pygame.draw.rect(win, RED, (self.hitbox[0], self.hitbox[1] - 35, 100, 20))
        pygame.draw.rect(
            win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 35, self.health, 20)
        )
        self.sprite_area = [self.x_pos, self.y_pos, 256, 256]
        if variables.settings.getboolean("Developer Options", "show_cop_hitboxes"):
            pygame.draw.rect(win, RED, self.hitbox, 2)
            pygame.draw.rect(win, BLUE, self.sprite_area, 2)

    def within_range_of(self, target: Human):
        """Checks if the distance to the target is close enough to hit."""
        distance = abs(self.x_pos - target.x_pos)
        return distance <= self.weapon_range

    def move(self, target: Human):
        """Moves the cop towards the player if they are wanted."""
        if variables.wanted_level == 0:
            self.velocity = 0
            self.animation_stage = 18
        else:
            self.velocity = 3
            self.direction = 1 if target.x_pos > self.x_pos else -1
        if self.animation_stage > 24:
            return
        self.x_pos += self.velocity * self.direction

    def hit(self, player_status_effects: set[str]):
        """Called when shot by bullet"""
        if variables.wanted_level == 0:
            variables.wanted_level += 1
        Effect("bullet_hit")
        weapon_damage = variables.selected_gun.damage
        if (
            "mayo_power" in player_status_effects
        ):  # Double damage taken when player has mayo power
            weapon_damage *= 2
        if (
            "beer_power" in player_status_effects
        ):  # Triple damage taken when player has beer power
            weapon_damage *= 3
        if self.health - weapon_damage > 0:
            self.health -= weapon_damage
        else:
            if variables.wanted_level < 5:
                variables.wanted_level += 1
            variables.cop_amount += 1
            random_death_sound = f"die{random.randint(1, 3)}"
            Effect(random_death_sound)
            self.health = 0
            for loot_type in ("ammo_light", "ammo_heavy", "money"):
                seed = random.randint(1, 3)
                position_variance = seed + 2
                random_x = (
                    random.randint(
                        self.x_pos - 10 * position_variance,
                        self.x_pos + 10 * position_variance,
                    )
                    + 128
                )
                random_y = (
                    random.randint(
                        self.y_pos - 10 * position_variance,
                        self.y_pos + 10 * position_variance,
                    )
                    + 128
                )
                if random.randint(1, 5) <= LOOT_TABLE[loot_type]["drop_chance"]:
                    variables.drops.append(
                        LootDrop((random_x, random_y), seed, loot_type)
                    )
            variables.cops.remove(self)
            # Deletes the oldest created loot drop if there are more than the max
            if len(variables.drops) >= MAX_RENDERED_DROPS:
                variables.drops.pop(0)

    def regenerate(self):
        """Called on respawn."""
        self.health = 100
        self.x_pos = WIN_WIDTH
        self.y_pos = WIN_HEIGHT - 93
