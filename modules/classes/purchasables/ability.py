"""Module containing ability purchasable behaviour."""

import pygame

from modules import init, variables
from modules.constants import IMAGE_DIR
from modules.classes.abstract import ShopItem
from modules.classes.effect import Effect

ICON_MARGIN_LEFT = 20
ICON_GAP = 100

SPRITE_NAMES = {
    "beer": "beer_bottle",
    "mayo": "mayo_jar",
}


class Ability(ShopItem):
    """Base class for the ability sprites in the shop."""

    all: list["Ability"] = []

    def __init__(self, pos: tuple[int, int], name: str, cost: int):
        super().__init__(pos, name, cost)
        bold_font = init.fonts["bold_font"]
        self.text = bold_font.render(f"{name} - ${cost}", 1, [255] * 3)
        self.owned_text = bold_font.render("0", 1, [255] * 3)
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

        self.text_x = ICON_MARGIN_LEFT
        self.icon_y = 80 + ICON_GAP * len(self.all)
        icon_text = bold_font.render(f"{name} ({name[0]})", 1, [255] * 3)
        self.progress = 0
        self.icon_x = self.text_x + icon_text.get_width() // 2 - 37 // 2
        self.icon_dimensions = [
            self.text_x,
            self.icon_y,
            icon_text.get_width(),
            58 + icon_text.get_height(),
        ]
        self.bar_dimensions = [
            self.text_x + icon_text.get_width() + 1,
            self.icon_y + 18,
            10,
            40,
        ]
        self.dummy_text = bold_font.render(str(self.owned)[0], 1, (0, 0, 0))
        self.bar_fill_dimensions = [
            self.bar_dimensions[0],
            self.bar_dimensions[1] + (self.progress - 40) // 5,
            self.bar_dimensions[2],
            self.bar_dimensions[3] - (self.progress - 40) // 5,
        ]

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
        self.owned_text = init.fonts["bold_font"].render(str(self.owned), 1, [255] * 3)
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

    def draw_icon(self, win):
        """Render the ability icons on the in-game sidebar."""
        if variables.paused and variables.pause_menu == "shop":
            return
        self.dummy_text = init.fonts["bold_font"].render(
            str(self.owned)[0], 1, (0, 0, 0)
        )

        activation_keybinding = variables.settings["Keybindings"][
            "activate_" + self.name
        ]
        render_text = f"{self.name} ({activation_keybinding})"
        bold_font = init.fonts["bold_font"]
        if self.owned > 0 or self.progress > 0:
            icon_text = bold_font.render(render_text, 1, [255] * 3)
            self.owned_text = bold_font.render(str(self.owned), 1, [255] * 3)
            win.blit(
                init.sprites[SPRITE_NAMES[self.name]],
                (self.icon_x, self.icon_y),
            )
        else:
            icon_text = bold_font.render(render_text, 1, [128] * 3)
            self.owned_text = bold_font.render("0", 1, [128] * 3)
            win.blit(
                init.sprites[SPRITE_NAMES[self.name] + "_bw"],
                (self.icon_x, self.icon_y),
            )
        win.blit(icon_text, (self.text_x, self.icon_y + 58))
        win.blit(
            self.owned_text,
            (
                self.text_x + icon_text.get_width() - self.dummy_text.get_width() * 2,
                self.icon_y - 2,
            ),
        )
        if self.progress > 0:
            # Uncomment below to show powerup sprite hitboxes in game
            # pygame.draw.rect(win, (0, 204, 255), self.bar_dimensions)
            dims = self.bar_dimensions
            if self.progress < dims[3]:
                self.bar_fill_dimensions = [
                    dims[0],
                    dims[1] + dims[3] - self.progress,
                    dims[2],
                    self.progress,
                ]
            else:
                self.bar_fill_dimensions = [
                    dims[0],
                    dims[1] + (self.progress - 40) // 5,
                    dims[2],
                    dims[3] - (self.progress - 40) // 5,
                ]
            pygame.draw.rect(win, (204, 204, 0), self.bar_fill_dimensions)

    def activate(self, slav):
        """Enables the ability and starts its timer."""
        if self.progress == 0:
            self.owned -= 1
            Effect("mayo")
            Effect("eating")
        if self.progress < 240:
            self.progress += 1
            slav.status_effects.add(self.name + "_power")
        else:
            self.progress = 0
            slav.status_effects.remove(self.name + "_power")
