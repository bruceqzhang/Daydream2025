import pygame
from sys import exit

class Character(pygame.sprite.Sprite):
    global dimensions, background_rect, background_surface
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load('graphics/character.png').convert_alpha(), 0,0.1)
        self.rect = self.image.get_rect(center =(dimensions[0]//2, dimensions[1]//2))

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            background_rect.x += 5  # Move background in opposite direction
            if background_rect.left <= 0:

        if keys[pygame.K_RIGHT] and background_rect.right >= dimensions[0]:
            background_rect.x -= 5
        if keys[pygame.K_UP] and background_rect.top <= 0:
            background_rect.y += 5
        if keys[pygame.K_DOWN] and background_rect.bottom >= dimensions[1]:
            background_rect.y -= 5

    def update(self):
        self.move()



pygame.init()
dimensions = (1000,640)
screen = pygame.display.set_mode(dimensions)
pygame.display.set_caption("Daydream")
clock = pygame.time.Clock()
font = pygame.font.Font('fonts/Pixeltype.ttf', 50)


background_surface = pygame.transform.rotozoom(pygame.image.load('graphics/background.jpg').convert_alpha(), 0, 3)
background_rect1 = background_surface.get_rect(center=(dimensions[0]//2, dimensions[1]//2))
background_rect2 = background_surface.get_rect(center=(dimensions[0]//2, dimensions[1]//2))
background_rect3 = background_surface.get_rect(center=(dimensions[0]//2, dimensions[1]//2))
background_rect4 = background_surface.get_rect(center=(dimensions[0]//2, dimensions[1]//2))
character = pygame.sprite.GroupSingle()
character.add(Character())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(background_surface, background_rect1)
    character.update()
    character.draw(screen)
    pygame.display.update()
    clock.tick(60)

