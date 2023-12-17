import pygame


from modules import variables, init
from modules.constants import IMAGE_DIR


class Weapon:
    """Base class for the weapon object."""

    def __init__(self, pos, name, cost, damage, rof, full_auto, money_count):
        self.x_pos, self.y_pos = pos
        self.name = name
        image_path = IMAGE_DIR + f"gun_{name.lower()}.png"
        self.img = pygame.image.load(image_path)
        self.cost = cost
        self.damage = damage
        self.rof = rof  # rate of fire
        self.full_auto = full_auto  # if fully automatic fire is permitted
        self.bold_font = init.fonts["bold_font"]
        self.text = self.bold_font.render(f"{name} - ${cost}", 1, [255] * 3)
        self.affordable = money_count >= self.cost
        self.flash_sequence = -1
        self.outer_hitbox = [self.x_pos, self.y_pos, 256, 164]
        self.owned = False
        if self.name == "AK-47":
            self.hitbox = [self.x_pos, self.y_pos, 256, 144]
        elif self.name == "MP5":
            self.hitbox = [
                self.x_pos + (256 - 192) // 2,
                self.y_pos + (144 - 104) // 2,
                192,
                144,
            ]
        elif self.name == "Beretta":
            self.hitbox = [
                self.x_pos + (256 - 101) // 2,
                self.y_pos + (144 - 72) // 2,
                101,
                72,
            ]
        elif self.name == "Deagle":
            self.hitbox = [
                self.x_pos + (256 - 128) // 2,
                self.y_pos + (144 - 128) // 2,
                128,
                128,
            ]
        self.text_position = [
            self.x_pos + 256 // 2 - self.text.get_width() // 2,
            self.y_pos + 144 - 10,
        ]

    def draw(self, win):
        """Renders the weapon sprite in the shop menu."""
        if variables.selected_gun == self:
            self.text = self.bold_font.render(self.name + " [USING]", 1, [255] * 3)
        elif self.owned:
            self.text = self.bold_font.render(self.name + " [OWNED]", 1, [255] * 3)
        else:
            self.text = self.bold_font.render(
                f"{self.name} - ${self.cost}", 1, [255] * 3
            )
        self.text_position = [
            self.x_pos + 256 // 2 - self.text.get_width() // 2,
            self.y_pos + 144 - 10,
        ]
        if self.flash_sequence >= 0:
            self.flash_sequence += 0.5
            if self.flash_sequence // 2 != self.flash_sequence / 2:
                pygame.draw.rect(win, (255, 96, 96), self.outer_hitbox)
                pygame.draw.rect(win, (255, 0, 0), self.outer_hitbox, 5)
        if self.flash_sequence >= 6:
            self.flash_sequence = -1
        if self.owned:
            pygame.draw.rect(win, (72, 240, 112), self.outer_hitbox)
        elif self.affordable:
            pygame.draw.rect(win, (0, 255, 0), self.outer_hitbox, 5)
        if self == variables.selected_gun:
            pygame.draw.rect(win, [255] * 3, self.outer_hitbox, 5)
        win.blit(self.img, (self.hitbox[:2]))
        win.blit(self.text, self.text_position)
        # Uncomment below to show weapon sprite hitboxes in store
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 1)

    def flash(self):
        """Perform the flash animation when the user cannot afford this weapon."""
        self.flash_sequence = 0
