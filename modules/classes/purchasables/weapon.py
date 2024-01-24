"""Class definition for the weapons used by the player, purchasable in the shop."""

from modules import variables
from modules.constants import (
    IMAGE_DIR,
    INFINITE_AMMO,
    FRAME_WIDTH,
    FRAME_HEIGHT,
)
from modules.classes.human import Human
from modules.classes.effect import Effect
from modules.classes.abstract import ShopItem, scale_image, centre_image
from modules.classes.projectile import Projectile
from modules.classes.purchasables.ammo import AmmoPurchasable


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
        self.image_path = f"{IMAGE_DIR}gun_{name.lower()}.png"
        self.image, image_dimensions = scale_image(self.image_path)
        self.damage = damage
        self.rof = rof  # rate of fire
        self.full_auto = full_auto  # if fully automatic fire is permitted
        self.dimensions = [
            self.x_pos,
            self.y_pos,
            FRAME_WIDTH,
            FRAME_HEIGHT,
        ]
        self.image_dimensions = centre_image(image_dimensions, self.dimensions)

    def draw(self, win):
        """Renders the weapon sprite in the shop menu."""
        item_info = (
            "[SELECTED]"
            if variables.selected_gun == self
            else "[OWNED]"
            if self.owned
            else f"- ${self.cost}"
        )
        text, text_position = self.get_text_position(f"{self.name} {item_info}")
        super().draw(win)
        if self == variables.selected_gun:
            self.draw_white_border(win)
        win.blit(self.image, self.image_dimensions)
        win.blit(text, text_position)

    def fire(self, shooter: Human):
        """Handle weapon firing."""
        Effect(f"bullet_fire_{self.name}")
        variables.firing = True
        if variables.shot_cooldown_time_passed < variables.shot_cooldown:
            return
        # Makes the script wait a certain amount of time before a gun is able to fire again
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
