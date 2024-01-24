"""Class for items dropped by cops."""

import pygame

from modules import variables
from modules.constants import LOOT_TABLE, WHITE


class LootDrop:
    """Money/ammo drop class."""

    def __init__(self, pos: tuple[int, int], pickup_amount: int, loot_type: str):
        self.x_pos, self.y_pos = pos
        self.loot_type = loot_type
        self.pickup_amount = (
            LOOT_TABLE[loot_type]["pickup_amount_multiplier"] * pickup_amount
        )
        self.hitbox = [self.x_pos + 8, self.y_pos, 48, 65]
        self.animation_cycle = 0
        font_size = 19 + self.animation_cycle
        self.current_font = pygame.font.SysFont("comicsans", font_size)
        self.text = self.current_font.render(f"+{self.pickup_amount}", True, WHITE)
        self.text_position = (
            self.hitbox[0] + self.hitbox[2] // 2 - self.text.get_width() // 2,
            self.hitbox[1] - 20,
        )
        self.animation_direction = 1

    def draw(self, win, sprites):
        """Renders the loot drop in the game window."""
        self.current_font = pygame.font.SysFont("comicsans", 19 + self.animation_cycle)
        if self.animation_cycle == 0 and self.animation_direction == -1:
            self.animation_direction = 1
        elif self.animation_cycle == 5 and self.animation_direction == 1:
            self.animation_direction = -1
        if not variables.paused:
            self.animation_cycle += self.animation_direction

        sprite_name = "coin_stack" if self.loot_type == "money" else self.loot_type
        win.blit(
            sprites[sprite_name],
            (self.x_pos, self.y_pos),
        )
        dollar_sign = "$" if self.loot_type == "money" else ""
        text_to_render = f"+{dollar_sign}{self.pickup_amount}"
        self.text = self.current_font.render(text_to_render, True, WHITE)

        win.blit(self.text, self.text_position)
        self.hitbox = [self.x_pos + 8, self.y_pos, 48, 65]
        self.text_position = (
            self.hitbox[0] + self.hitbox[2] // 2 - self.text.get_width() // 2,
            self.hitbox[1] - 20,
        )
        # Uncomment below to show dropped item hitboxes
        # pygame.draw.rect(v.win, RED, self.hitbox, 2)
