import pygame

from modules import variables


class LootDrop:
    """Money/ammo drop class."""

    def __init__(self, pos: tuple[int, int], pickup_amount: int, loot_type: str):
        self.x_pos, self.y_pos = pos
        self.loot_type = loot_type
        self.pickup_amount = (
            3 * pickup_amount if loot_type == "money" else pickup_amount
        )
        self.hitbox = [self.x_pos + 8, self.y_pos, 48, 65]
        self.animation_cycle = 0
        font_size = 19 + self.animation_cycle
        self.current_font = pygame.font.SysFont("comicsans", font_size)
        self.text = self.current_font.render(f"+{self.pickup_amount}", True, [255] * 3)
        self.text_position = [
            self.hitbox[0] + self.hitbox[2] // 2 - self.text.get_width() // 2,
            self.hitbox[1] - 20,
        ]
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

        sprite_name = "bullet_stack" if self.loot_type == "ammo" else "coin_stack"
        win.blit(
            sprites[sprite_name],
            (self.x_pos, self.y_pos),
        )
        text_to_render = f"+{'$' * int(self.loot_type == 'money')}{self.pickup_amount}"
        self.text = self.current_font.render(text_to_render, True, [255] * 3)

        win.blit(self.text, self.text_position)
        self.hitbox = [self.x_pos + 8, self.y_pos, 48, 65]
        self.text_position = [
            self.hitbox[0] + self.hitbox[2] // 2 - self.text.get_width() // 2,
            self.hitbox[1] - 20,
        ]
        # Uncomment below to show dropped item hitboxes
        # pygame.draw.rect(v.win, (255, 0, 0), self.hitbox, 2)
