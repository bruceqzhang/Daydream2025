import pygame
from sys import exit

pygame.init()
dimensions = (1000,640)
screen = pygame.display.set_mode(dimensions)
pygame.display.set_caption("Daydream")
clock = pygame.time.Clock()
font = pygame.font.Font('fonts/Pixeltype.ttf', 50)


background_surface = pygame.transform.rotozoom(pygame.image.load('graphics/background.jpg').convert_alpha(), 0, 3)
background_rect = background_surface.get_rect(topleft=(0, 0))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(background_surface, background_rect)

    pygame.display.update()
    clock.tick(60)

