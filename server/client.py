# Imports
import keyboard
import socket
import threading
import pygame
import json
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('116.106.225.168', 1512))
def game_exit():
    while True:
        if keyboard.is_pressed('ESC'):
            pygame.quit
            client.send('stop'.encode('utf-8'))
            break