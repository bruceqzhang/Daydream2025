import pygame
from random import randint
import math
from sys import exit
rect_width = 50
rect_height = 10
zombie_timer=5000
buff=True
shot_timer=1000
light_display_time=40
display_checker=0
game_status = 0 # 0 = welcome 1 = playing, 2 = paused, 3 = game over

class Background:
    def __init__(self, image_path):
        base_image = pygame.image.load(image_path).convert_alpha()
        zoom = 2
        self.image = pygame.transform.scale(
            base_image,
            (base_image.get_width() * zoom, base_image.get_height() * zoom)
        )
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def draw(self, surface, camera_x, camera_y):
        # Find top-left tile that should be drawn
        start_x = -(camera_x % self.width)
        start_y = -(camera_y % self.height)

        # Draw enough tiles to cover the screen
        for i in range(-1, surface.get_width() // self.width + 2):
            for j in range(-1, surface.get_height() // self.height + 2):
                surface.blit(self.image, (start_x + i * self.width, start_y + j * self.height))
    

class Supplies(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load('graphics/supplies.png').convert_alpha(), 0,0.1)
        self.rect = self.image.get_rect(center =(x, y))

    def update(self):
        if pygame.sprite.collide_rect(self, character.sprite):
            #trigger menu
            self.kill()
    
        
class Zombie(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.spawnlocation = randint(0,3)
        self.health = 3
        self.speed = 1
        self.image = pygame.transform.rotozoom(pygame.image.load('graphics/zombie.png').convert_alpha(), 0,0.1)
        if (self.spawnlocation==0):
            self.rect = self.image.get_rect(center=(-50, randint(0, dimensions[1])))
        elif (self.spawnlocation==1):
            self.rect = self.image.get_rect(center=(dimensions[0]+50, randint(0, dimensions[1])))
        elif (self.spawnlocation==2):
            self.rect = self.image.get_rect(center=(randint(0, dimensions[0]), -50))
        elif (self.spawnlocation==3):
            self.rect = self.image.get_rect(center=(randint(0, dimensions[0]), dimensions[1]+50))
        
        self.x_accumulation = 0.0
        self.y_accumulation = 0.0

    def move(self, x_velocity, y_velocity):
        zx_velocity = 0.0
        zy_velocity = 0.0
        hypotenuse = math.hypot(self.rect.x - dimensions[0]/2, self.rect.y - dimensions[1]/2)
        delta_y = self.rect.y - dimensions[1]/2
        delta_x = self.rect.x - dimensions[0]/2
            
        if self.rect.x < dimensions[0]/2:
            zx_velocity += math.sqrt(1-(delta_y**2)/(hypotenuse**2))
        if self.rect.x > dimensions[0]/2:
            zx_velocity -= math.sqrt(1-(delta_y**2)/(hypotenuse**2))
        if self.rect.y < dimensions[1]/2:
            zy_velocity += math.sqrt(1-(delta_x**2)/(hypotenuse**2))
        if self.rect.y > dimensions[1]/2:
            zy_velocity -= math.sqrt(1-(delta_x**2)/(hypotenuse**2))
        
        self.x_accumulation += zx_velocity - round(zx_velocity)  
        self.y_accumulation += zy_velocity - round(zy_velocity)

        if self.x_accumulation >= 1.0:
            zx_velocity += 1
            self.x_accumulation -= 1.0
        elif self.x_accumulation <= -1.0:
            zx_velocity -= 1
            self.x_accumulation += 1.0
        if self.y_accumulation >= 1.0:
            zy_velocity += 1
            self.y_accumulation -= 1.0
        elif self.y_accumulation <= -1.0:
            zy_velocity -= 1
            self.y_accumulation += 1.0

        self.rect.x += zx_velocity - x_velocity
        self.rect.y += zy_velocity - y_velocity
    
    def update(self, x_velocity, y_velocity):
        self.move(x_velocity, y_velocity)

    
        
class Lights(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load('graphics/igor.png').convert_alpha(), 0,0.1)
        screen.blit(self.image, (dimensions[0]//2 + 50, dimensions[1]//2))
        self.rect = self.image.get_rect(center = (dimensions[0]//2, dimensions[1]//2))
        self.energy = 50

        
    
    def dim_screen(self):
        dim_level = 50 + 3*self.energy
        darkness = pygame.Surface((dimensions[0], dimensions[1]), pygame.SRCALPHA)
        darkness.fill((0,0,0,255))
        pygame.draw.circle(darkness, (0,0,0,0), (self.rect.centerx, self.rect.centery), 100+dim_level)
        screen.blit(darkness, (0,0))


    
    def update(self, surface):
        if self.energy > 0:
            self.energy -= 0.05
        if self.energy <=0:
            self.energy = 0
        self.dim_screen()
        surface.blit(self.image, self.rect)


class Pistol(pygame.sprite.Sprite):
    global dimensions, background_rect, background_surface
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load('graphics/hannah.png').convert_alpha(), 0,0.4)
        self.rect = self.image.get_rect(center =(dimensions[0]//2 + 50, dimensions[1]//2))
        self.energy = 100

    def get_closest_zombie(self, zombie_group):
        global screen
        min_dist = float('inf')
        closest_zombie = None
        char_pos = self.rect.center
        for zombie in zombie_group:
            zombie_pos = zombie.rect.center
            dist = math.hypot(zombie_pos[0] - char_pos[0], zombie_pos[1] - char_pos[1])
            if dist < min_dist:
                min_dist = dist
                closest_zombie = zombie
        return closest_zombie
        
    def shoot(self, zombie_group):
        global shot_timer,display_checker
        if buff==True:
            shot_timer = 1000
        else:
            shot_timer = 2000
        closest_zombie = self.get_closest_zombie(zombie_group)
        if closest_zombie:
            zx, zy = closest_zombie.rect.center
            pygame.draw.line(screen, (255,255,0), (self.rect.centerx, self.rect.centery), (zx, zy), 5)                #closest_zombie.health -= 1
        display_checker = 1
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)


            


class Cheerleader(pygame.sprite.Sprite):
    global dimensions, background_rect, background_surface
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load('graphics/character.png').convert_alpha(), 0,0.1)
        self.rect = self.image.get_rect(center =(dimensions[0]//2, dimensions[1]//2))
        self.energy = 100
        print(self.rect.centerx, self.rect.centery)



    #def update(self):
    #     self.move()


def collisions():
    for zombie_1 in zombie_group:
        for zombie_2 in zombie_group:
            if zombie_1 != zombie_2 and pygame.sprite.collide_rect(zombie_1, zombie_2):
                if zombie_1.rect.x < zombie_2.rect.x:
                    zombie_1.rect.x -= 1
                else:
                    zombie_1.rect.x += 1
                if zombie_1.rect.y < zombie_2.rect.y:
                    zombie_1.rect.y -= 1
                else:
                    zombie_1.rect.y += 1
                # Simple collision response: move them apart

pygame.init()
dimensions = (1000,640)
screen = pygame.display.set_mode(dimensions)
pygame.display.set_caption("Daydream")
clock = pygame.time.Clock()
font = pygame.font.Font('fonts/Pixeltype.ttf', 50)


background = Background('graphics/background.jpg')
camera_x = 0
camera_y = 0

character= pygame.sprite.GroupSingle()
#character.add(Character())

lights = Lights()

pistol = Pistol()

zombie_group = pygame.sprite.Group()

zombie_spawn_timer = pygame.USEREVENT + 1
pygame.time.set_timer(zombie_spawn_timer, zombie_timer)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == zombie_spawn_timer:
            zombie_group.add(Zombie())
            if zombie_timer > 1000:
                zombie_timer -= 50

    collisions()
    # Detect Key Presses
    x_velocity = 0
    y_velocity = 0
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x_velocity -= 5
        
    if keys[pygame.K_RIGHT]:
        x_velocity += 5
    if keys[pygame.K_UP]:
        y_velocity -= 5
    if keys[pygame.K_DOWN]:
        y_velocity += 5
    
    if x_velocity != 0 and y_velocity != 0:
        length = math.hypot(x_velocity, y_velocity)
        x_velocity = (x_velocity / length) * 5
        y_velocity = (y_velocity / length) * 5


    # Camera offset accumulates player movement
    camera_x += x_velocity
    camera_y += y_velocity

    # Clear screen first
    screen.fill((0, 0, 0))

    # Draw background relative to camera
    background.draw(screen, camera_x, camera_y)
    
    character.update()
    character.draw(screen)

    pistol.update()
    pistol.draw(screen)
    

    shot_timer -= 10
    closest_zombie = pistol.get_closest_zombie(zombie_group)
    if closest_zombie:
        closestzombiex, closestzombiey = closest_zombie.rect.center
    if shot_timer <= 0:
        pistol.shoot(zombie_group)
    if display_checker==1:
        light_display_time -= 1
        if light_display_time <= 0:
            display_checker=0
            light_display_time=40

    zombie_group.update(x_velocity, y_velocity)
    zombie_group.draw(screen)

    lights.update(screen)
    lights.dim_screen()

    
    #screen.blit(lights.dim_surface)
    #pygame.draw.rect(screen,(50,50,50),(character.sprite.rect.centerx - rect_width // 2, character.sprite.rect.top - rect_height, rect_width, rect_height))
    #pygame.draw.rect(screen,(0,0,255),(character.sprite.rect.centerx - rect_width // 2, character.sprite.rect.top - rect_height, rect_width, rect_height))
    pygame.display.update()
    clock.tick(60)

