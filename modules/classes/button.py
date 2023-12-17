import pygame

from modules import variables, init
from modules.constants import WIN_WIDTH, WIN_HEIGHT


class Button:
    """Base class for the settings buttons."""

    def __init__(self, text: str, next_menu: str = None, on_click=None, selected=False):
        self.text_message = text
        self.standard_font = init.fonts["standard_font"]
        self.text = self.standard_font.render(text, 1, (0, 0, 0))
        self.dimensions = None
        self.selected = selected
        if on_click is None:
            if next_menu is not None:

                def callback():
                    variables.pause_menu = next_menu

                self.on_click = callback
        else:
            self.on_click = on_click

    def initialise_dimensions(self, buttons):
        """Initialises the sprite dimensions."""
        sibling_buttons = []
        for btns in buttons.values():
            if self in btns:
                sibling_buttons = btns
                break
        if len(sibling_buttons) == 2:
            # The index of the button is either 1 or 0, which means its x_centre is the window width * either 1/4 or 3/4
            x_centre = WIN_WIDTH * (1 + 2 * sibling_buttons.index(self)) // 4
            # The x_pos position is the x_pos centre minus half of the button's width
            # The y_pos position is almost at the halfway point of the window's height
            # The width of the button is one third of the window's width
            # The height of the button is 50px
            self.dimensions = [
                x_centre - WIN_WIDTH // 6,
                WIN_HEIGHT * 7 // 12,
                WIN_WIDTH // 3,
                50,
            ]
        else:
            # The index of the button is 0-2, which means its y_centre is the window height * either 3/8, 4/8 or 5/8
            y_centre = WIN_HEIGHT * (3 + sibling_buttons.index(self)) // 8
            # The x_pos position is at the halfway point of the window's width
            # The y_pos position is either at 1/3, 1/2 or 2/3 of the window's height
            # The width of the button is one half of the window's width
            # The height of the button is 50px
            self.dimensions = [
                WIN_WIDTH // 2 - WIN_WIDTH // 4,
                y_centre,
                WIN_WIDTH // 2,
                50,
            ]

    def draw(self, win, buttons, bg_shade=None):
        """Renders the button in the pause menu."""
        if self.dimensions is None:
            self.initialise_dimensions(buttons)
        if bg_shade is None:
            bg_shade = 64 if self.selected else 128
        pygame.draw.rect(win, [bg_shade] * 3, self.dimensions)
        # Renders button outline graphic
        pygame.draw.rect(win, (0, 0, 0), self.dimensions, 2)
        text_position = [
            self.dimensions[0] + self.dimensions[2] // 2 - self.text.get_width() // 2,
            self.dimensions[1] + self.dimensions[3] // 2 - self.text.get_height() // 2,
        ]
        win.blit(self.text, text_position)

    def do_action(self):
        """Click handler for the given button."""
        if not variables.paused:
            return
        self.on_click()


# SLIDER CODE
class Slider(Button):
    def __init__(self, text):
        super().__init__(text)
        self.label_text = text
        self.text = None
        self.slider_dimensions = None

    def draw(self, win, settings, bg_shade=32):
        if settings["muted"]:
            volume = 0
            volume_text = "MUTED"
        else:
            volume = settings["volume"] / 100
            volume_text = f"{settings['volume']}%"
        self.text = self.standard_font.render(
            self.label_text.format(vol=volume_text), 1, (0, 0, 0)
        )

        super().draw(bg_shade)

        self.slider_dimensions = [
            self.dimensions[0] + int((self.dimensions[2] - 20) * volume),
            self.dimensions[1],
            20,
            50,
        ]
        pygame.draw.rect(win, (128, 128, 128), self.slider_dimensions)
        pygame.draw.rect(win, (0, 0, 0), self.slider_dimensions, 2)
