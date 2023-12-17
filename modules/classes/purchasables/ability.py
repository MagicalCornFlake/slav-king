import pygame
from modules.constants import IMAGE_DIR
from modules import init


class AbilityPurchasable:
    """Base class for the ability sprites in the shop."""

    def __init__(self, x_pos, y_pos, money_count, name, cost):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.name = name
        self.img = pygame.image.load(f"{IMAGE_DIR}icon_{name}.png")
        self.cost = cost
        self.bold_font = init.fonts["bold_font"]
        self.text = self.bold_font.render(f"{name} - ${cost}", 1, [255] * 3)
        self.owned_text = self.bold_font.render("0", 1, [255] * 3)
        self.affordable = money_count >= self.cost
        self.flash_sequence = -1
        self.outer_hitbox = [self.x_pos, self.y_pos, 224, 164]
        self.owned = 0
        if self.name == "mayo":
            self.hitbox = [
                self.x_pos + (self.outer_hitbox[2] - 75) // 2,
                self.y_pos + (144 - 116) // 2,
                75,
                116,
            ]
            self.img = pygame.transform.scale(self.img, (75, 116))
        elif self.name == "beer":
            self.hitbox = [
                self.x_pos + (self.outer_hitbox[2] - 40) // 2,
                self.y_pos + (144 - 124) // 2,
                40,
                124,
            ]
            self.img = pygame.transform.scale(self.img, (40, 124))
        self.text_position = [
            self.x_pos + self.outer_hitbox[2] // 2 - self.text.get_width() // 2,
            self.y_pos + 144 - 10,
        ]
        self.owned_text_position = [self.x_pos + 16, self.y_pos + 12]

    def draw(self, win):
        """Render the weapon sprite in the shop."""
        self.owned_text = self.bold_font.render(str(self.owned), 1, [255] * 3)
        self.owned_text_position = [self.x_pos + 16, self.y_pos + 12]
        if self.owned > 0:
            pygame.draw.rect(win, (72, 240, 112), self.outer_hitbox)
            pygame.draw.rect(win, [255] * 3, self.outer_hitbox, 5)
        elif self.affordable:
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
        """Perform the flash animation when the user cannot afford this powerup."""
        self.flash_sequence = 0
