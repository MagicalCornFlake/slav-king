"""Module containing ability purchasable behaviour."""

import pygame

from modules import init, variables
from modules.constants import IMAGE_DIR, WHITE, FRAME_WIDTH, FRAME_HEIGHT
from modules.classes.abstract import ShopItem, scale_image, centre_image
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
        self.dimensions = [
            self.x_pos,
            self.y_pos,
            FRAME_WIDTH * 3 // 4,
            FRAME_HEIGHT,
        ]
        self.owned = 0
        self.image, image_dimensions = scale_image(f"{IMAGE_DIR}icon_{name}.png")
        self.image_position = centre_image(image_dimensions, self.dimensions)
        self.text, self.text_position = self.get_text_position(f"{name} - ${cost}")

        self.text_x = ICON_MARGIN_LEFT
        self.icon_y = 80 + ICON_GAP * len(self.all)
        icon_text = bold_font.render(f"{name} ({name[0]})", 1, WHITE)
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
        bar_vertical_offset = (self.progress - 40) // 5
        self.bar_fill_dimensions = [
            self.bar_dimensions[0],
            self.bar_dimensions[1] + bar_vertical_offset,
            self.bar_dimensions[2],
            self.bar_dimensions[3] - bar_vertical_offset,
        ]

        self.all.append(self)

    def draw(self, win):
        """Render the weapon sprite in the shop."""
        owned_text = self.bold_font.render(str(self.owned), 1, WHITE)
        owned_text_position = (self.x_pos + 16, self.y_pos + 12)
        super().draw(win)
        if self.owned > 0:
            self.draw_white_border(win)
        win.blit(self.image, self.image_position)
        win.blit(self.text, self.text_position)
        win.blit(owned_text, owned_text_position)

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
            icon_text = bold_font.render(render_text, 1, WHITE)
            owned_text = bold_font.render(str(self.owned), 1, WHITE)
            win.blit(
                init.sprites[SPRITE_NAMES[self.name]],
                (self.icon_x, self.icon_y),
            )
        else:
            icon_text = bold_font.render(render_text, 1, [128] * 3)
            owned_text = bold_font.render("0", 1, [128] * 3)
            win.blit(
                init.sprites[SPRITE_NAMES[self.name] + "_bw"],
                (self.icon_x, self.icon_y),
            )
        win.blit(icon_text, (self.text_x, self.icon_y + 58))
        win.blit(
            owned_text,
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
