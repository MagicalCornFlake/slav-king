import pygame

from modules.constants import IMAGE_DIR
from modules import variables, init


class AmmoPurchasable:
    """Base class for the ammo purchasable sprites in the shop."""

    def __init__(self, x_pos, y_pos, money_count, cost):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.img = pygame.image.load(IMAGE_DIR + "icon_bullets.png")
        self.img = pygame.transform.scale(self.img, (96, 96))
        self.cost = cost
        self.bold_font = init.fonts["bold_font"]
        self.text = self.bold_font.render("15x - ${cost}", 1, [255] * 3)
        self.owned_text = self.bold_font.render(str(variables.ammo_count), 1, [255] * 3)
        self.affordable = money_count >= self.cost
        self.flash_sequence = -1
        self.outer_hitbox = [self.x_pos, self.y_pos, 176, 164]
        self.hitbox = [
            self.x_pos + (self.outer_hitbox[2] - 96) // 2,
            self.y_pos + (144 - 96) // 2,
            96,
            96,
        ]
        self.text_position = [
            self.x_pos + self.outer_hitbox[2] // 2 - self.text.get_width() // 2,
            self.y_pos + 144 - 10,
        ]
        self.owned_text_position = [self.x_pos + 16, self.y_pos + 12]

    def draw(self, win):
        """Render the ammo purchasable sprite in the shop."""
        self.owned_text = self.bold_font.render(str(variables.ammo_count), 1, [255] * 3)
        self.owned_text_position = [self.x_pos + 16, self.y_pos + 12]
        if self.affordable:
            pygame.draw.rect(win, (0, 255, 0), self.outer_hitbox, 5)
        if self.flash_sequence >= 0:
            self.flash_sequence += 0.5
            if self.flash_sequence // 2 != self.flash_sequence / 2:
                pygame.draw.rect(win, (255, 96, 96), self.outer_hitbox)
                pygame.draw.rect(win, (255, 0, 0), self.outer_hitbox, 5)
        if self.flash_sequence >= 6:
            self.flash_sequence = -1
        win.blit(self.img, (self.hitbox[:2]))
        win.blit(self.text, self.text_position)
        win.blit(self.owned_text, self.owned_text_position)
        # Uncomment below to show powerup sprite hitboxes in store
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 1)

    def flash(self):
        """Perform the flash animation when the user cannot afford this ammo purchasable."""
        self.flash_sequence = 0
