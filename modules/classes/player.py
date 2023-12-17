import pygame

from modules.constants import SPRITE_DIR, WIN_WIDTH, WIN_HEIGHT
from modules import variables, init


# S L A V
class Player:
    walkRight = []
    walkLeft = []
    for i in range(1, 10):
        walkRight.append(pygame.image.load(f"{SPRITE_DIR}R{i}.png"))
        walkRight[-1] = pygame.transform.scale(walkRight[-1], (256, 256))
        walkLeft.append(pygame.image.load(f"{SPRITE_DIR}L{i}.png"))
        walkLeft[-1] = pygame.transform.scale(walkLeft[-1], (256, 256))

    def __init__(self, x_pos, y_pos, width, height):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.vel = 10
        self.jumping = True
        self.left = False
        self.right = True
        self.walk_count = 0
        self.jump_count = 40
        self.standing = True
        self.hitbox = [self.x_pos + 78, self.y_pos + 58, 100, 190]

    def draw(self, win, show_player_hitbox):
        if self.walk_count >= 17:
            self.walk_count = 0
        if not self.standing:
            if self.left:
                win.blit(
                    self.walkLeft[round(self.walk_count) // 2], (self.x_pos, self.y_pos)
                )
                if not variables.paused:
                    self.walk_count += self.vel // 5 / 2
            elif self.right:
                win.blit(
                    self.walkRight[round(self.walk_count) // 2],
                    (self.x_pos, self.y_pos),
                )
                if not variables.paused:
                    self.walk_count += self.vel // 5 / 2
        else:
            if self.right:
                win.blit(self.walkRight[0], (self.x_pos, self.y_pos))
            else:
                win.blit(self.walkLeft[0], (self.x_pos, self.y_pos))
        self.hitbox = [self.x_pos + 78, self.y_pos + 58, 100, 190]
        if show_player_hitbox:
            pygame.draw.rect(win, (0, 255, 0), self.hitbox, 2)

    def hit(self, win, guns, purchasable_powerups):  # When killed
        # Stops all sound effects
        pygame.mixer.stop()
        # Resets all variables to start values
        self.jumping = True
        self.x_pos = 128
        self.y_pos = WIN_HEIGHT - 100 - 256 + 64
        self.vel = 10
        self.walk_count = 0
        self.jump_count = 40
        text = init.fonts["large_font"].render("BUSTED", 1, (255, 0, 0))
        win.blit(text, ((WIN_WIDTH // 2) - (text.get_width() // 2), 200))
        pygame.display.update()
        i = 0
        for gun in guns:
            gun.owned = False
        for powerup in purchasable_powerups:
            powerup.owned = 0
        while i < 100:  # Waits 100 * 10ms (one second)
            pygame.time.delay(10)
            i += 1
            # Checks to see if user has attempted to close v.window during that 1s
            for close_event in pygame.event.get():
                if close_event.type == pygame.QUIT:
                    i = 100
                    variables.paused = True
                    variables.pause_menu = "quit"
