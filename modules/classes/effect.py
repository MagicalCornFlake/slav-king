import pygame

from modules.constants import AUDIO_DIR


class Effect:
    """Base class for all sound effects."""

    pygame.mixer.music.load(AUDIO_DIR + "music.mp3")
    pygame.mixer.music.play(-1)

    def __init__(self, name: str):
        channel = pygame.mixer.find_channel(True)
        self.timer = 0
        sound_object = pygame.mixer.Sound(f"{AUDIO_DIR}{name.lower()}.wav")
        channel.play(sound_object)
