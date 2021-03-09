import pygame
from game.player import Game
import socket

sock = socket.create_server(("127.0.0.1", 8989), reuse_port=True)


pygame.init()
player = Game(size=(800, 600), fullscreen=False, box_size=10, fps=500, socket=sock)
player.run()
pygame.quit()
