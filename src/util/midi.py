import pygame
import os

def play_music(music_name):
    pygame.mixer.init()
    midi_path = os.path.dirname(__file__) + "/../assets/midi/" + music_name
    if not os.path.isfile(midi_path):
        return
    pygame.mixer.music.load(midi_path)
    pygame.mixer.music.play()
    print('music stop')

def stop_music():
    pygame.mixer.music.pause()
    print('music stop')
