import pygame
from modules import variables,  init


class Ability:
    """Base class for the in-game abilities."""

    def __init__(self, x_pos, y_pos, name):
        self.text_x = x_pos
        self.y_pos = y_pos
        self.name = name
        self.bold_font = init.fonts["bold_font"]
        self.text = self.bold_font.render(name, 1, [255] * 3)
        self.owned_text = self.bold_font.render("0", 1, [255] * 3)
        self.owned = 0
        self.progress = 0
        self.x_pos = x_pos + self.text.get_width() // 2 - 37 // 2
        self.dimensions = [
            x_pos,
            y_pos,
            self.text.get_width(),
            58 + self.text.get_height(),
        ]
        self.bar_dimensions = [
            self.text_x + self.text.get_width() - 11,
            self.y_pos + 18,
            10,
            40,
        ]
        self.dummy_text = self.bold_font.render(str(self.owned)[0], 1, (0, 0, 0))
        self.bar_fill_dimensions = [
            self.bar_dimensions[0],
            self.bar_dimensions[1] + (self.progress - 40) // 5,
            self.bar_dimensions[2],
            self.bar_dimensions[3] - (self.progress - 40) // 5,
        ]

    def draw(self, win, purchasable_powerups):
        """Render the ability icons on the in-game sidebar."""
        if variables.paused and variables.pause_menu == "shop":
            return

        for (
            powerup
        ) in (
            purchasable_powerups
        ):  # Calculating how many powerups the user has purchased
            if powerup.name.startswith(self.name):
                self.owned = powerup.owned
                break
        self.dummy_text = self.bold_font.render(str(self.owned)[0], 1, (0, 0, 0))

        if self.owned > 0 or self.progress > 0:
            self.text = self.bold_font.render(self.name, 1, [255] * 3)
            self.owned_text = self.bold_font.render(str(self.owned), 1, [255] * 3)
            win.blit(
                init.sprites["mayo_jar"] if self.name == "mayo" else init.sprites["beer_bottle"],
                (self.x_pos, self.y_pos),
            )
        else:
            self.text = self.bold_font.render(self.name, 1, (128, 128, 128))
            self.owned_text = self.bold_font.render("0", 1, (128, 128, 128))
            win.blit(
                init.sprites["mayo_jar_bw"]
                if self.name == "mayo"
                else init.sprites["beer_bottle_bw"],
                (self.x_pos, self.y_pos),
            )
        win.blit(self.text, (self.text_x, self.y_pos + 58))
        win.blit(
            self.owned_text,
            (
                self.text_x + self.text.get_width() - self.dummy_text.get_width() + 5,
                self.y_pos - 2,
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

    def activate(self, slav, purchasable_powerups):
        """Enables the ability and starts its timer."""
        if self.progress == 0:
            for powerup in purchasable_powerups:
                if powerup.name.startswith(self.name):
                    powerup.owned -= 1
                    break
        if self.progress < 240:
            self.progress += 1
            if self.name == "mayo":
                variables.mayo_power = True
                slav.vel = 20
            elif self.name == "beer":
                variables.beer_power = True
                slav.vel = 5
        else:
            self.progress = 0
            if self.name == "mayo":
                variables.mayo_power = False
            elif self.name == "beer":
                variables.beer_power = False
            slav.vel = 10
