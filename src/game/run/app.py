import pygame

from colors import Color

pygame.init()
timer = pygame.time.Clock()
fps = 120

game_scrin = pygame.display.set_mode(
    (1920, 1080),
    # pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.OPENGL,
)
pygame.display.set_caption("MEGA DRIVE")
game_scrin.fill(Color.GOLD)
pygame.display.flip()
work = True
while work:
    keys = pygame.key.get_pressed()
    work = not keys[pygame.K_ESCAPE]
    timer.tick(fps)
    events = pygame.event.get()
    for event in events:
        print(event)
        if event.type == pygame.WINDOWCLOSE:
            work = False

pygame.quit()