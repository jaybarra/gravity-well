import pygame
from random import randrange as rrandom, choice
from uuid import uuid4
from math import sqrt, pow


pygame.init()

screen = pygame.display.set_mode((800,600)) 

pygame.display.set_caption("Gravity Well")

# SETTINGS
num_particles = 99

max_mass = 1e4
min_mass = 1

max_size = 10
min_size = 1

#CONSTANTS
#G = 6.67384e-11
G = 1e-2

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


screen_w, screen_h = pygame.display.get_surface().get_size()

# Classes
class Particle:

    def __init__(self, mass=1.0, size=3.0, location=(0, 0), velocity=(0.0, 0.0)):
        self.id = uuid4()
        self.mass = mass
        self.size = size
        self.location = location
        self.velocity = velocity

    def __repr__(self):
        return "[id={}, mass={}, size={}, location=({}, {}), velocity=({}, {})]".format(
            self.id,
            self.mass,
            self.size,
            self.location[0], self.location[1],
            self.velocity[0], self.velocity[1]
        )


# INITIALIZATION

particles = []
for x in range(num_particles):
    particles.append(Particle(mass=rrandom(min_mass,max_mass), size=rrandom(min_size, max_size), location=(rrandom(0, screen_w), rrandom(0, screen_h ))))


# main loop
run = True
while run:
    # process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN and event.key == 114: #R - reset
            for p in particles:
                p.location = (rrandom(0, screen_w), rrandom(0, screen_h))
   
    # refresh screen
    screen.fill(WHITE)
    w, h = pygame.display.get_surface().get_size()

    # draw shapes
    for p in particles:
        f_x = 0.0
        f_y = 0.0

        # TODO hold updates till the end and apply then, particles are being updated now before others
        for other in particles:
            if p is other:
                continue

            mass_component = G * p.mass * other.mass

            dx = p.location[0] - other.location[0]
            dy = p.location[1] - other.location[1]
            
            r = sqrt(pow(dx,2) +pow(dy,2))
           
            # apply no force if already touching
            if (p.size + other.size) > r:
                continue 

            f = mass_component / pow(r, 2)

            # subtract, gravity is attractive
            f_x -= f * dx / r
            f_y -= f * dy / r

        curr_x, curr_y = p.location
        
        # accelerate 1 unit of time
        v_x = p.velocity[0] + (f_x / p.mass)
        v_y = p.velocity[1] + (f_y / p.mass)
       
        # update velocity
        p.velocity = (v_x - p.velocity[0], v_y - p.velocity[1])
        
        # update location
        # TODO check for collisions even if the delta is large, otherwise particles could clip through each other

        normal_red = int((p.mass) / max_mass * 255.0)
        p.location = ((p.location[0] + v_x) % w, (p.location[1] + v_y) % h)

        pygame.draw.circle(screen, (normal_red, 0, 0), (int(p.location[0]),int(p.location[1])) , p.size)

        
    pygame.display.update()

pygame.quit()

