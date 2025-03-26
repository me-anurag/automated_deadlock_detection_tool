# src/sound_manager.py
import pygame

class SoundManager:
    def __init__(self, allocate_sound_path, request_sound_path):
        pygame.mixer.init()
        self.sound_enabled = True
        self.allocate_sound = None
        self.request_sound = None
        self.sounds_loaded = False  # New flag to track if sounds loaded successfully

        try:
            self.allocate_sound = pygame.mixer.Sound(allocate_sound_path)
            self.request_sound = pygame.mixer.Sound(request_sound_path)
            self.sounds_loaded = True  # Set to True if both sounds load successfully
        except Exception as e:
            print(f"Error loading sounds: {e}")
            self.sound_enabled = False  # Disable sound if loading fails

    def toggle_sound(self):
        if not self.sounds_loaded:
            return False  # Can't toggle sound if sounds didn't load
        self.sound_enabled = not self.sound_enabled
        return self.sound_enabled

    def play_allocate_sound(self):
        if self.sound_enabled and self.allocate_sound:
            self.allocate_sound.play()

    def play_request_sound(self):
        if self.sound_enabled and self.request_sound:
            self.request_sound.play()