import pygame

from modules import init
from modules.constants import IMAGE_DIR
from modules.classes.purchasables.shop_item import ShopItem


class AbilityPurchasable(ShopItem):
    """Base class for the ability sprites in the shop."""

    all: list["AbilityPurchasable"] = []

    def __init__(self, pos: tuple[int, int], name: str, cost: int):
        super().__init__(pos, name, cost)
        self.bold_font = init.fonts["bold_font"]
        self.text = self.bold_font.render(f"{name} - ${cost}", 1, [255] * 3)
        self.owned_text = self.bold_font.render("0", 1, [255] * 3)
        self.flash_sequence = -1
        self.dimensions = [self.x_pos, self.y_pos, 224, 164]
        self.owned = 0
        image = pygame.image.load(f"{IMAGE_DIR}icon_{name}.png")
        self.image = self.get_scaled_image(image)
        self.text_position = [
            self.x_pos + self.dimensions[2] // 2 - self.text.get_width() // 2,
            self.y_pos + 144 - 10,
        ]
        self.owned_text_position = [self.x_pos + 16, self.y_pos + 12]
        self.all.append(self)

    def get_scaled_image(self, image: pygame.Surface):
        """Scales the given image such that the image fits within the shop item frame."""
        width = image.get_width()
        height = image.get_height()
        new_width = 116 / height * width
        new_height = 116
        self.hitbox = [
            self.x_pos + (self.dimensions[2] - new_width) // 2,
            self.y_pos + (144 - new_height) // 2,
            new_width,
            new_height,
        ]
        return pygame.transform.scale(image, (new_width, new_height))

    def draw(self, win):
        """Render the weapon sprite in the shop."""
        self.owned_text = self.bold_font.render(str(self.owned), 1, [255] * 3)
        self.owned_text_position = [self.x_pos + 16, self.y_pos + 12]
        if self.owned > 0:
            pygame.draw.rect(win, (72, 240, 112), self.dimensions)
            pygame.draw.rect(win, [255] * 3, self.dimensions, 5)
        elif self.affordable:
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
        """Perform the flash animation when the user cannot afford this powerup."""
        self.flash_sequence = 0
