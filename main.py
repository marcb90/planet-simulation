from platform import python_branch
from sre_parse import HEXDIGITS
from turtle import distance
import pygame
import math


pygame.init()

WIDTH, HEIGHT = 800, 800
WIN  = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")


# RGB Values for Planet Colours.
WHITE = (255, 255, 255)
DARK_ORANGE = (193, 143, 23)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)

# Define Font for Distance label
FONT = pygame.font.SysFont("comicsans", 16)

class Planet:

    AU = 149.6e6 * 1000             # 1AU = 1 Astronomical UNIT
    G = 6.67428e-11
    SCALE = 250 / AU                # 1AU = 100 pixels
    TIMESTEP = 3600 * 14            # 1 day of panet movement around sun -> (3600 * 24), adjust for different speeds of simulation.

    def __init__(self, x, y, radius, colour, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0 

        self.x_vel = 0
        self.y_vel = 0
    
    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        # create orbit line
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2 
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            # draw orbit line
            pygame.draw.lines(win, self.colour, False, updated_points, 2)
       
        # display distance to Sun in KMs
        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)}km", 1 , WHITE)
            win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_width() /2))

        # draw planet
        pygame.draw.circle(win, self.colour, (x, y), self.radius)

    #DO THE MATH

    def attraction(self, other):
        # Calulate distance between two objects
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        # is other objeect the not the sun
        if other.sun: 
            self.distance_to_sun = distance
        
        force = self.G * self.mass * other.mass / distance**2 
        # Find Theta
        theta = math.atan2(distance_y, distance_x)
        # Calculate Forece and distance
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        return force_x, force_y
    
    def update_position(self, objects):
        total_fx = total_fy = 0
        for object in objects:
            if self == object:
                continue

            fx, fy = self.attraction(object)
            total_fx += fx
            total_fy += fy
        
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))


def main():
    run = True
    clock = pygame.time.Clock()

    # SUN
    sun = Planet(0, 0, 30, YELLOW, 1.9882 * 10**30)
    sun.sun = True

    # EARTH + Velocity
    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9743 * 10**24)
    earth.y_vel = 29.783 * 1000

    # MARS + Velocity
    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000

    # MERCURY + Velocity
    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10**23)
    mercury.y_vel = -47.4 * 1000

    # VENUS + Velocity
    venus = Planet(0.723 * Planet.AU, 0, 14, DARK_ORANGE, 4.685 * 10**24)
    venus.y_vel = -35.02 * 1000

    ##########################################################
    ## FOR ANY FUTURE PLANETS THAT ARE ADDED:               ##
    ##        THE FOLLOW ATT WILL NEED ADJUSTING:           ##
    ##                           WIDTH                      ##
    ##                           HEIGHT                     ##
    ##                           SCALE                      ##
    ##                                                      ##
    ##########################################################

    # Store the planets and sun as objects
    objects = [sun, earth, mars, mercury, venus]

    while run:
        clock.tick(60)                              #essentially 60 frames/second
        WIN.fill((0, 0, 0))                         #Refreshes background every cycle
        
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        for object in objects:
            object.update_position(objects)         #update planets position
            object.draw(WIN)                        #draw on screen.
        
        pygame.display.update()
        
    pygame.quit()

main()