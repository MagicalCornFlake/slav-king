"""Class definition for the weapons used by the player, purchasable in the shop."""

import pygame

from modules import variables, init
from modules.constants import IMAGE_DIR, INFINITE_AMMO
from modules.classes.human import Human
from modules.classes.effect import Effect
from modules.classes.projectile import Projectile
from modules.classes.purchasables.shop_item import ShopItem
from modules.classes.purchasables.ammo import AmmoPurchasable


FRAME_WIDTH = 16 * 16
FRAME_HEIGHT = 9 * 16
WHITE = [255] * 3


def get_scaled_image_dimensions(
    image_path: str,
    max_width: int = FRAME_WIDTH - 16 * 3,
    max_height: int = FRAME_HEIGHT - 9 * 3,
):
    """Scales the image appropriately to the frame."""
    image = pygame.image.load(image_path)
    image_width = image.get_width()
    image_height = image.get_height()
    aspect_ratio = image_height / image_width
    if image_width >= max_width:
        dimensions = (max_width, aspect_ratio * max_width)
    else:
        dimensions = (max_height / aspect_ratio, max_height)

    scaled_image = pygame.transform.scale(image, dimensions)
    return scaled_image, dimensions


class Weapon(ShopItem):
    """Base class for the weapon object."""

    all: list["Weapon"] = []

    def __init__(
        self,
        pos: tuple[int, int],
        name: str,
        cost: int,
        damage: int,
        rof: int,
        full_auto: bool,
    ):
        super().__init__(pos, name, cost)
        self.all.append(self)
        self.image_path = IMAGE_DIR + f"gun_{name.lower()}.png"
        self.image, (width, height) = get_scaled_image_dimensions(self.image_path)
        self.damage = damage
        self.rof = rof  # rate of fire
        self.full_auto = full_auto  # if fully automatic fire is permitted
        self.bold_font = init.fonts["bold_font"]
        self.text = self.bold_font.render(f"{name} - ${cost}", 1, WHITE)
        self.flash_sequence = -1
        self.dimensions = [
            self.x_pos,
            self.y_pos,
            FRAME_WIDTH,
            FRAME_HEIGHT + 20,
        ]
        self.owned = False
        self.hitbox = [
            self.x_pos + (FRAME_WIDTH - width) // 2,
            self.y_pos + (FRAME_HEIGHT - height) // 2,
            width,
            height,
        ]
        self.text_position = [
            self.x_pos + (FRAME_WIDTH - self.text.get_width()) // 2,
            self.y_pos + FRAME_HEIGHT - 10,
        ]

    def draw(self, win):
        """Renders the weapon sprite in the shop menu."""
        if variables.selected_gun == self:
            self.text = self.bold_font.render(self.name + " [SELECTED]", 1, WHITE)
        elif self.owned:
            self.text = self.bold_font.render(self.name + " [OWNED]", 1, WHITE)
        else:
            self.text = self.bold_font.render(f"{self.name} - ${self.cost}", 1, WHITE)
        self.text_position = [
            self.x_pos + FRAME_WIDTH // 2 - self.text.get_width() // 2,
            self.y_pos + FRAME_HEIGHT - 10,
        ]
        if self.flash_sequence >= 0:
            self.flash_sequence += 0.5
            if self.flash_sequence // 2 != self.flash_sequence / 2:
                pygame.draw.rect(win, (255, 96, 96), self.dimensions)
                pygame.draw.rect(win, (255, 0, 0), self.dimensions, 5)
        if self.flash_sequence >= 6:
            self.flash_sequence = -1
        if self.owned:
            pygame.draw.rect(win, (72, 240, 112), self.dimensions)
        elif self.affordable:
            pygame.draw.rect(win, (0, 255, 0), self.dimensions, 5)
        if self == variables.selected_gun:
            pygame.draw.rect(win, WHITE, self.dimensions, 5)
        win.blit(self.image, (self.hitbox[:2]))
        win.blit(self.text, self.text_position)
        # Uncomment below to show weapon sprite hitboxes in shop
        # pygame.draw.rect(win, (255, 0, 0), self.dimensions, 1)

    def flash(self):
        """Perform the flash animation when the user cannot afford this weapon."""
        self.flash_sequence = 0

    def fire(self, shooter: Human):
        """Handle weapon firing."""
        Effect(f"bullet_fire_{self.name}")
        variables.firing = True
        if variables.shot_cooldown_time_passed < variables.shot_cooldown:
            return
        # Makes the script wait a certain amount of time before a gun is able to fire again (rof = Rate of Fire)
        rate_of_fire = self.rof / 60  # rounds per second
        shot_interval = 1 / rate_of_fire  # seconds
        variables.shot_cooldown_time_passed = 0
        variables.shot_cooldown = shot_interval
        # Fires bullet
        variables.bullets.append(
            Projectile(
                (
                    round(shooter.x_pos + shooter.width // 2),
                    round(shooter.y_pos + shooter.height // 2.5),
                ),
                shooter.direction,
            )
        )
        if INFINITE_AMMO or AmmoPurchasable.selected_ammo_idx is None:
            return
        AmmoPurchasable.get_selected().owned -= 1
