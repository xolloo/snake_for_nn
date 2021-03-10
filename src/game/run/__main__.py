import pygame
from game.player import Game

# import socket
import sys

# sock = socket.create_server(("127.0.0.1", 8989), reuse_port=True)
is_video = "-v" in sys.argv

pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.HWSURFACE | pygame.DOUBLEBUF, 0, 0)
pygame.display.set_caption("MEGA SNAKE.")
work = True
while work:
    player = Game(
        size=(800, 600),
        fullscreen=False,
        box_size=10,
        fps=500,
        screen=screen,
    )
    work = player.run()
pygame.quit()
