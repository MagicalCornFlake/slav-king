import pygame
from modules.constants import SPRITE_DIR


class Human:
    def __init__(
        self,
        x_pos: int,
        y_pos: int,
        width: int,
        height: int,
        velocity: int,
        direction: int,
    ):
        self.x_pos = self.original_x_pos = x_pos
        self.y_pos = self.original_y_pos = y_pos
        self.width = width
        self.height = height
        self.animation_stage = 0
        self.velocity = velocity
        self.direction = direction  # 0: standing, 1: right, -1: left

    @property
    def hitbox(self):
        return [self.x_pos + 78, self.y_pos + 58, 100, 190]


def get_sprite_frames(num_frames: int, sprite_prefix: str = ""):
    frames_right = []
    frames_left = []
    for i in range(1, num_frames + 1):
        image = pygame.image.load(f"{SPRITE_DIR}{sprite_prefix}R{i}.png")
        scaled_image = pygame.transform.scale(image, (256, 256))
        frames_right.append(scaled_image)

        image = pygame.image.load(f"{SPRITE_DIR}{sprite_prefix}L{i}.png")
        image_scaled = pygame.transform.scale(image, (256, 256))
        frames_left.append(image_scaled)
    return frames_right, frames_left
