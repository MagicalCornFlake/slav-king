"""Class definition for the projectiles fired by the player weapon."""

import pygame

from modules import init
from modules.classes.purchasables.ammo import AmmoPurchasable

BULLET_VELOCITY = 32
AMMO_TYPES = ["light", "heavy"]


class Projectile:
    """Bullet class."""

    all: list["Projectile"] = []

    def __init__(self, pos: tuple[int, int], direction: int) -> None:
        self.x_pos, self.y_pos = pos
        self.direction = direction
        ammo_idx: int = AmmoPurchasable.selected_ammo_idx or 0
        ammo_type = AMMO_TYPES[ammo_idx]
        self.sprite = init.sprites[f"bullet_{ammo_type}"]
        if direction == -1:
            self.sprite = pygame.transform.flip(self.sprite, True, False)
        self.velocity = BULLET_VELOCITY

    def draw(self, win: pygame.Surface) -> None:
        """Renders the bullet in the game window."""
        pos = self.x_pos, self.y_pos
        win.blit(self.sprite, pos)
