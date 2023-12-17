import pygame
import random

from modules import variables
from modules.constants import WIN_WIDTH, WIN_HEIGHT, SPRITE_DIR
from modules.classes.effect import Effect
from modules.classes.loot_drop import LootDrop


# P O L I C E
class Enemy:
    walkRight = []
    walkLeft = []
    for i in range(1, 12):
        walkRight.append(pygame.image.load(f"{SPRITE_DIR}ER{i}.png"))
        walkRight[-1] = pygame.transform.scale(walkRight[-1], (256, 256))
        walkLeft.append(pygame.image.load(f"{SPRITE_DIR}EL{i}.png"))
        walkLeft[-1] = pygame.transform.scale(walkLeft[-1], (256, 256))

    def __init__(self, x_pos, y_pos, width, height):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.path = [50, WIN_WIDTH - 50 - 64]
        self.walk_count = 0
        self.vel = -3
        self.hitbox = [self.x_pos + 78, self.y_pos + 58, 100, 190]
        self.health = 100
        self.sprite_area = [self.x_pos, self.y_pos, 256, 256]

    def draw(self, win, slav, settings):
        if not variables.paused:
            self.move(slav)
        # If within 50px of player and currently in 'attack' animation
        if abs(self.x_pos - slav.x_pos) > 50 and self.walk_count >= 24:
            self.walk_count = 0
        elif self.walk_count >= 32:
            self.walk_count = 0

        if self.vel > 0:
            win.blit(self.walkRight[self.walk_count // 3], (self.x_pos, self.y_pos))
            if not variables.paused:
                self.walk_count += 1
        elif self.vel < 0:
            win.blit(self.walkLeft[self.walk_count // 3], (self.x_pos, self.y_pos))
            if not variables.paused:
                self.walk_count += 1
        else:
            self.walk_count = 20
            win.blit(self.walkLeft[self.walk_count // 3], (self.x_pos, self.y_pos))
        self.hitbox = [self.x_pos + 78, self.y_pos + 58, 100, 190]
        # Drawing health bar
        pygame.draw.rect(
            win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 35, 100, 20)
        )
        pygame.draw.rect(
            win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 35, self.health, 20)
        )
        self.sprite_area = [self.x_pos, self.y_pos, 256, 256]
        if settings["showCopHitboxes"]:
            pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
            pygame.draw.rect(win, (0, 0, 255), self.sprite_area, 2)

    def move(self, slav):
        if variables.wanted_level == 0:
            self.vel = 0
        elif self.walk_count <= 24:
            if slav.x_pos > self.x_pos:
                self.vel = 3
                self.x_pos += self.vel
            else:
                self.vel = -3
                self.x_pos += self.vel

    def hit(self):  # When shot by bullet
        if variables.wanted_level == 0:
            variables.wanted_level += 1
        variables.sounds.append(Effect("bullet_hit"))
        minus = variables.selected_gun.dmg
        if variables.mayo_power:  # Double damage taken when player has mayo power
            minus *= 2
        if variables.beer_power:  # Triple damage taken when player has beer power
            minus *= 3
        if self.health - minus > 0:
            self.health -= minus
        else:
            if variables.wanted_level < 5:
                variables.wanted_level += 1
            variables.cop_amount += 1
            random_death_sound = f"die{random.randint(1, 3)}"
            variables.sounds.append(Effect(random_death_sound))
            self.health = 0
            for loot_type in ("ammo", "money"):
                variance = random.randint(3, 5)
                random_x = (
                    random.randint(
                        self.x_pos - 10 * variance, self.x_pos + 10 * variance
                    )
                    + 128
                )
                random_y = (
                    random.randint(
                        self.y_pos - 10 * variance, self.y_pos + 10 * variance
                    )
                    + 128
                )
                if random.randint(1, 3) > 1:
                    variables.drops.append(
                        LootDrop((random_x, random_y), variance, loot_type)
                    )
            variables.cops.remove(self)
            # Deletes the oldest created loot drop if there are more than ten
            if len(variables.drops) >= 10:
                variables.drops.pop(0)

    def regenerate(self):  # Respawn
        self.health = 100
        self.x_pos = WIN_WIDTH
        self.y_pos = WIN_HEIGHT - 93

    def touching_hitbox(self, hitbox: list[int, int, int, int]) -> bool:
        nw_corner = (hitbox[0], hitbox[1])
        ne_corner = (hitbox[0] + hitbox[2], hitbox[1])
        sw_corner = (hitbox[0], hitbox[1] + hitbox[3])
        se_corner = (hitbox[0] + hitbox[2], hitbox[1] + hitbox[3])
        return True in [
            self.touching_point(corner)
            for corner in [nw_corner, ne_corner, sw_corner, se_corner]
        ]

    def touching_point(self, point: tuple[int, int]) -> bool:
        return (
            self.hitbox[0] < point[0] < self.hitbox[0] + self.hitbox[2]
            and self.hitbox[1] < point[1] < self.hitbox[1] + self.hitbox[3]
        )
