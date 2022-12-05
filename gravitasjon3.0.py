"""
The program simulates gravitational forces between planets of different masses.
We have done some modifications to the mass sizes, speeds, and gravitanional formula for optimization purposes.
Use arrow up for zoom out, arrow down for zoom in, arrow left for decreasing delta time, arrow right for increasing delta time,
"a" for showing all pathes taken by the planets since the start of the simulation, and "s" has the same function as "a" except it only shows the 
paths for the planets on the screen.
One can also use the textbox to change the delta time.

Made by Da_Boat and ShailsehS1702
"""

import pygame as pg
import random as rdm
from pygame.locals import (K_s, K_a, K_BACKSPACE, K_RETURN, K_UP, K_DOWN, K_LEFT, K_RIGHT)

pg.init()

window_width = 1000
window_height = 700
window = pg.display.set_mode([window_width, window_height]) #makes the display window
done = False

window.fill((255, 255, 255))
clock = pg.time.Clock()
font = pg.font.Font(None, 24)

factor = 1 #zoom factor
dt = 0.01   

class Planet:
    def __init__(self, name, mass, radius, pos: list, speed_x, speed_y, color: tuple) -> None:
        self.name = name
        self.mass = mass
        self.radius = radius
        self.pos = pos
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.color = color
        self.gravity_x = 0
        self.gravity_y = 0
        self.dx = 0 
        self.dy = 0
        self.all_poses = []
        self.all_poses_zoomed = []
        self.zoomed_pos = [0, 0]
        self.zoomed_radius = self.radius / (factor * 0.3) if self.radius / (factor * 0.3) > 1 else 1
        

    def tyngdeMet(self, planet: object):
        """
        takes in an planet object
        """
        #calculates the gravity between itself and a given object. Does not use gamma, since it makes for easier calculations without it.
        gravity = (self.mass * planet.mass) /((self.pos[0] - planet.pos[0])**2 + (self.pos[1] - planet.pos[1])**2)

        dx = self.pos[0] - planet.pos[0] #change in x-position
        dy = self.pos[1] - planet.pos[1] #change in y-position

        r = (dx**2 + dy**2)**(1/2) #the distance between the two objects
        gravity_x = abs((gravity * dx) / r) #absolute value of gravity in x-direction
        gravity_y = abs((gravity * dy) / r) #absolute value of gravity in y-direction

        #se teoridelen
        #changes from gravity to acceleration
        if (self.pos[0] > planet.pos[0]): 
            
            self.gravity_x += -gravity_x / self.mass
            planet.gravity_x += gravity_x / planet.mass
        else:
            self.gravity_x += gravity_x / self.mass
            planet.gravity_x += -gravity_x   / planet.mass

        if (self.pos[1] > planet.pos[1]):
            self.gravity_y += -gravity_y / self.mass
            planet.gravity_y += gravity_y / planet.mass
        else:
            self.gravity_y += gravity_y / self.mass
            planet.gravity_y += -gravity_y / planet.mass  
               
    def move(self, t: float): #calculates how much the position changes.
        ax = self.gravity_x
        ay = self.gravity_y
        self.dx = 1 / 2 * ax * t**2 + self.speed_x * t #using s=1/2*a *t**2+v*t to find change in x and y directions
        self.dy = 1 / 2 * ay * t**2 + self.speed_y * t

        self.pos[0] = 1 / 2 * ax * t**2 + self.speed_x * t + self.pos[0]#using s=1/2*a *t**2+v*t +s_0 to find change new position
        self.pos[1] = 1 / 2 * ay * t**2 + self.speed_y * t + self.pos[1]
        self.speed_x = ax * t + self.speed_x #redefines the new speed for next iteration using v= a*t +v_0
        self.speed_y = ay * t + self.speed_y
        self.gravity_x = 0 #sets gravity to 0 to next iteration.
        self.gravity_y = 0

        self.zoomed_pos[0] = self.pos[0]/factor + (window_width - window_width/factor) / 2 #defines the zoomed positions using factor and moving the object to the center.
        self.zoomed_pos[1] = self.pos[1]/factor + (window_height - window_height/factor) / 2

        self.all_poses.append([self.pos[0], self.pos[1]])
        #append only object that are within the window to position list, to reduce the length of the list and making the program faster.
        """ if 0 - self.radius < self.pos[0] < window_width + self.radius and 0 - self.radius < self.pos[1] < window_height + self.radius:
            self.all_poses.append([self.pos[0], self.pos[1]]) """

        #if 0 - self.radius / (factor * 0.3) < self.zoomed_pos[0] < window_width + self.radius / (factor * 0.3) and 0 - self.radius / (factor * 0.3) < self.zoomed_pos[1] < window_height + self.radius / (factor * 0.3):

    def draw(self):
        """
        draws the planet based on wether the window is zoomed in or not.
        """
        #desplay_factor = factor*0.3 if factor > 3.3333 else factor*0.3
        self.zoomed_radius = self.radius / (factor * 0.3) if self.radius / (factor * 0.3) > 1 else 1
        pg.draw.circle(window, self.color, (self.zoomed_pos[0], self.zoomed_pos[1]), self.zoomed_radius)


planet_list = []
num_of_planets = 50
# makes a list of planets in a random position within the window. the number of planets are specified in num_of_planets. they also get a random speed and mass.
for i in range(num_of_planets):
    rdm_num = rdm.randint(1, 4)
    planet_list.append(Planet("TEst", 10**rdm_num, rdm_num*2, [rdm.randint(0, window_width), rdm.randint(0, window_height)], rdm.randint(-100, 100), rdm.randint(-100, 100), (rdm.randint(0, 255), rdm.randint(0, 255), rdm.randint(0, 255))))

# make a central "star" and one planet with defined positions, masses and speeds.
main_r = 6
test = Planet("TEst", 10**main_r, main_r*2, [window_width / 2 - main_r, window_height / 2 - main_r], 0, 0, (rdm.randint(0, 255), rdm.randint(0, 255), rdm.randint(0, 255)))
planet_list.append(test)
planet_list.append(Planet("TEst", 10**3, 3*2, [window_width / 2 - main_r, window_height / 2 - main_r - 100], 105, 0, (rdm.randint(0, 255), rdm.randint(0, 255), rdm.randint(0, 255))))

#defines relevant variables.
zoomed_out = False
delay_i = 0
dt_input = "0.01"
active = False

while not done: 
    pressedKeys = pg.key.get_pressed()

    if active is True:
        pg.draw.rect(window,(211, 211, 211), (window_width - 100, 20, 75, 25))
    else:
        pg.draw.rect(window,(255, 255, 255), (window_width - 100, 20, 75, 25))
        
    input_rect_border = pg.draw.rect(window,(0, 0, 0), (window_width - 100, 20, 75, 25), width=1)

    for event in pg.event.get():
        # continues the game until closing he window 
        if event.type == pg.QUIT:
            done = True

        # activates the textbox
        if event.type == pg.MOUSEBUTTONDOWN and input_rect_border.collidepoint(event.pos):
            active = True
        elif event.type == pg.MOUSEBUTTONDOWN and input_rect_border.collidepoint(event.pos) is False:
            active = False
        
        if active:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE:
                    dt_input = dt_input[:-1]
                elif event.unicode == ".":
                    dt_input += event.unicode
                else:
                    try:
                        float(event.unicode)
                        dt_input += event.unicode
                    except:
                        print("Input a number")


    dt_input_display = font.render(str(dt_input), True, (0, 0, 0))
    window.blit(dt_input_display, (window_width - 100 + 6, 20 + 5))  
    dt_text = font.render("dt:", True, (0, 0, 0))
    window.blit(dt_text, (window_width - 130 + 6, 20 + 5))
    zoom_text = font.render(f"Zoom: {factor:.2f}x", True, (0, 0, 0))
    window.blit(zoom_text, (20, 20))     

    #finds the gravitational force between it self and all the other planets after it in the program.
    for i in range(len(planet_list)):
        for j in range(i + 1, len(planet_list)):
            planet_list[i].tyngdeMet(planet_list[j])

    if pressedKeys[K_RETURN]:
        dt = float(dt_input)
        active = False


    if pressedKeys[K_UP]:
        factor += 0.1

    if pressedKeys[K_DOWN] and factor > 1.05:
        factor -= 0.1

    if pressedKeys[K_LEFT] and dt >= 0.005:
        dt_input = str(round(float(dt_input) - 0.005, 5))
        dt = float(dt_input)

    if pressedKeys[K_RIGHT]:
        dt_input = str(round(float(dt_input) + 0.005, 5))
        dt = float(dt_input)

    #subtract the main objects change in x and y direction to all object and thereby centering the main object.
    for ele in planet_list:
        ele.pos[0] -= test.dx
        ele.pos[1] -= test.dy

    #draw all object and moves the objects.
    for ele in planet_list:
        ele.draw()
        ele.move(dt) 

    if pressedKeys[K_s] and pressedKeys[K_UP] is False and pressedKeys[K_DOWN] is False:
        for planet in planet_list:
            if 0 - planet.zoomed_radius < planet.zoomed_pos[0] < window_width + planet.zoomed_radius and 0 - planet.zoomed_radius < planet.zoomed_pos[1] < window_height + planet.zoomed_radius:
                for ele in planet.all_poses:
                    zoomed_posX = ele[0]/factor + (window_width - window_width/factor) / 2 # defines the zoomed positions using factor and moving the object to the center.
                    zoomed_posY = ele[1]/factor + (window_height - window_height/factor) / 2
                    pg.draw.circle(window, planet.color, (zoomed_posX, zoomed_posY), planet.zoomed_radius)

    if pressedKeys[K_a] and pressedKeys[K_UP] is False and pressedKeys[K_DOWN] is False:
        for planet in planet_list:
                for ele in planet.all_poses:
                    zoomed_posX = ele[0]/factor + (window_width - window_width/factor) / 2 # defines the zoomed positions using factor and moving the object to the center.
                    zoomed_posY = ele[1]/factor + (window_height - window_height/factor) / 2

                    if 0 - planet.zoomed_radius < zoomed_posX < window_width + planet.zoomed_radius and 0 - planet.zoomed_radius < zoomed_posY < window_height + planet.zoomed_radius:
                        pg.draw.circle(window, planet.color, (zoomed_posX, zoomed_posY), planet.zoomed_radius)
        
    #display window
    pg.display.flip()
    clock.tick(60)
    window.fill((255, 255, 255))

pg.quit()
