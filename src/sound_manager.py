# src/sound_manager.py
import pygame
import os

class SoundManager:
    def __init__(self, allocate_sound_path, request_sound_path):
        try:
            pygame.mixer.init()
            self.sound_for_allocate = pygame.mixer.Sound(allocate_sound_path)
            self.sound_for_request = pygame.mixer.Sound(request_sound_path)
            self.sound_enabled = True
        except (pygame.error, FileNotFoundError) as error:
            print(f"Could not initialize Pygame sound or load sound files: {error}")
            print("The program will continue without sounds.")
            self.sound_for_allocate = None
            self.sound_for_request = None
            self.sound_enabled = False

    def play_allocate_sound(self):
        if self.sound_enabled and self.sound_for_allocate:
            self.sound_for_allocate.play()

    def play_request_sound(self):
        if self.sound_enabled and self.sound_for_request:
            self.sound_for_request.play()

    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        return self.sound_enabled