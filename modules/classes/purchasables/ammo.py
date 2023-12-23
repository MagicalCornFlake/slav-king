"""Class definition for the ammunition types purchasable in the shop."""

import pygame

from modules import init
from modules.constants import IMAGE_DIR
from modules.classes.abstract import ShopItem


class AmmoPurchasable(ShopItem):
    """Base class for the ammo purchasable sprites in the shop."""

    all: list["AmmoPurchasable"] = []
    selected_ammo_idx: None | int = None

    def __init__(
        self, pos: tuple[int, int], name: str, cost: int, owned: int, quantity: int
    ):
        super().__init__(pos, name, cost)
        image = pygame.image.load(f"{IMAGE_DIR}icon_{name}.png")
        self.image = pygame.transform.scale(image, (96, 96))
        self.bold_font = init.fonts["bold_font"]
        self.text = self.bold_font.render(f"{quantity}x - ${cost}", 1, [255] * 3)
        self.owned = self.initial_owned_amount = owned
        self.owned_text = self.bold_font.render(str(self.owned), 1, [255] * 3)
        self.flash_sequence = -1
        self.dimensions = [self.x_pos, self.y_pos, 176, 164]
        self.hitbox = [
            self.x_pos + (self.dimensions[2] - 96) // 2,
            self.y_pos + (144 - 96) // 2,
            96,
            96,
        ]
        self.text_position = [
            self.x_pos + self.dimensions[2] // 2 - self.text.get_width() // 2,
            self.y_pos + 144 - 10,
        ]
        self.owned_text_position = [self.x_pos + 16, self.y_pos + 12]
        self.quantity = quantity
        self.all.append(self)

    def draw(self, win):
        """Render the ammo purchasable sprite in the shop."""
        self.owned_text = self.bold_font.render(str(self.owned), 1, [255] * 3)
        self.owned_text_position = [self.x_pos + 16, self.y_pos + 12]
        if self.affordable:
            pygame.draw.rect(win, (0, 255, 0), self.dimensions, 5)
        if self.flash_sequence >= 0:
            self.flash_sequence += 0.5
            if self.flash_sequence // 2 != self.flash_sequence / 2:
                pygame.draw.rect(win, (255, 96, 96), self.dimensions)
                pygame.draw.rect(win, (255, 0, 0), self.dimensions, 5)
        if self.flash_sequence >= 6:
            self.flash_sequence = -1
        win.blit(self.image, (self.hitbox[:2]))
        win.blit(self.text, self.text_position)
        win.blit(self.owned_text, self.owned_text_position)
        # Uncomment below to show powerup sprite hitboxes in shop
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 1)

    def flash(self):
        """Perform the flash animation when the user cannot afford this ammo purchasable."""
        self.flash_sequence = 0

    @staticmethod
    def get_selected():
        """Convenience method to return the currently selected ammo type."""
        if AmmoPurchasable.selected_ammo_idx is None:
            return None
        return AmmoPurchasable.all[int(AmmoPurchasable.selected_ammo_idx)]
