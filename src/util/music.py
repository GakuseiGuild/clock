import pygame
import os

def play_music(music_name):
    pygame.mixer.init()
    music_path = os.path.dirname(__file__) + "/../assets/music/" + music_name
    if not os.path.isfile(music_path):
        return
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play()
    print('music stop')

def stop_music():
    pygame.mixer.music.pause()
    print('music stop')
