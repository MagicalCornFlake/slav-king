import pygame


class Projectile:
    """Bullet class."""

    def __init__(self, pos: tuple[int, int], radius: int, colour, facing: int) -> None:
        self.x_pos, self.y_pos = pos
        self.radius: int = radius
        self.colour = colour
        self.facing: int = facing
        self.vel: int = 32 * facing

    def draw(self, win) -> None:
        """Renders the bullet in the game window."""
        pos = self.x_pos, self.y_pos
        pygame.draw.circle(win, self.colour, pos, self.radius)
