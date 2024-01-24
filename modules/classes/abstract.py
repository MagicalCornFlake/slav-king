"""Definitions of abstract classes that other classes will inherit from."""

import pygame

from modules import variables, init
from modules.constants import RED, WHITE, GREEN, FRAME_WIDTH, FRAME_HEIGHT


def scale_image(
    image_path: str,
    max_width: int = FRAME_WIDTH - 16 * 3,
    max_height: int = FRAME_HEIGHT - 9 * 3 - 20,
):
    """Scales the image appropriately to the frame."""
    image = pygame.image.load(image_path)
    image_width = image.get_width()
    image_height = image.get_height()
    aspect_ratio = image_height / image_width
    if image_width >= max_width:
        dimensions = (max_width, aspect_ratio * max_width)
    else:
        dimensions = (max_height / aspect_ratio, max_height)

    scaled_image = pygame.transform.scale(image, dimensions)
    return scaled_image, dimensions


def centre_image(
    image_dimensions: tuple[int, int], parent_dimensions: tuple[int, int, int, int]
):
    """Returns the dimension box of an object with the given width and height
    centred within the parent dimension box."""
    return (
        parent_dimensions[0] + (parent_dimensions[2] - image_dimensions[0]) // 2,
        parent_dimensions[1] + (parent_dimensions[3] - image_dimensions[1]) // 2,
        image_dimensions[0],
        image_dimensions[1],
    )


class Clickable:
    """Abstract class for objects which will be hovered over or clicked by the user's mouse."""

    dimensions: list[int]

    def contains_point(
        self, mouse_pos: tuple[int, int], dimensions_override: list[int] = None
    ):
        """Checks if the given point is within the object's dimensions."""
        box: list[int] = (
            dimensions_override
            if dimensions_override is not None
            else self.hitbox
            if hasattr(self, "hitbox")
            else self.dimensions
        )
        return (
            box[0] < mouse_pos[0] < box[0] + box[2]
            and box[1] < mouse_pos[1] < box[1] + box[3]
        )


class ShopItem(Clickable):
    """Abstract class for shop item that is clickable."""

    def __init__(self, pos: tuple[int, int], name: str | int, cost: int):
        self.x_pos, self.y_pos = pos
        self.name = name
        self.cost = cost
        self.owned = 0
        self.flash_sequence = -1
        self.bold_font = init.fonts["bold_font"]

    @property
    def affordable(self):
        """Whether or not the player's balance is sufficient to buy this item."""
        return variables.money_count >= self.cost

    def draw(self, win):
        """Renders common shop item elements."""
        if self.owned > 0:
            pygame.draw.rect(win, (72, 240, 112), self.dimensions)
        elif self.affordable:
            pygame.draw.rect(win, GREEN, self.dimensions, 5)
        if self.flash_sequence >= 0:
            self.flash_sequence += 0.5
            if self.flash_sequence // 2 != self.flash_sequence / 2:
                pygame.draw.rect(win, (255, 96, 96), self.dimensions)
                pygame.draw.rect(win, RED, self.dimensions, 5)
        if self.flash_sequence >= 6:
            self.flash_sequence = -1

    def flash(self):
        """Perform the flash animation when the user cannot afford this powerup."""
        self.flash_sequence = 0

    def draw_white_border(self, win):
        """Draws a white 5-pixel-thick border around the shop card."""
        pygame.draw.rect(win, WHITE, self.dimensions, 5)

    def get_text_position(self, text: str):
        """Returns the text rendered in a bold font as well as its centred position."""
        text_surface = self.bold_font.render(text, 1, WHITE)
        text_position = (
            self.x_pos + (self.dimensions[2] - text_surface.get_width()) // 2,
            self.y_pos + self.dimensions[3] - text_surface.get_height() - 7,
        )
        return text_surface, text_position
