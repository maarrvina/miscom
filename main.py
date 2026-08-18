# Marvin Ho
# A parody of the classic Atari game Missile Command

import pygame
import random
import math
import time

# Need to import os module to avoid driver error in console
# this stops my stuff from trying to use nonexistent audio ! we don't ask why :)
import os

os.environ['SDL_AUDIODRIVER'] = 'dsp'

# initializes python, makes all pygame code available to use
pygame.init()
# create window, width of 800 pixels, height of 400 pixels.
SCREENWIDTH = 650
SCREENHEIGHT = 450
GAMESPEED = 80  # number of ticks per screen refresh. 1 tick = 1ms
EMFREQUENCY = 150  # Number of while loops to generate an enemy missle
WINDOW = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
clock = pygame.time.Clock()

score_value = 0
FONT = pygame.font.Font("freesansbold.ttf", 16)
scorex = 300
scorey = 20

silo_count = 4

# friendly_missile_image = pygame.image.load("bigblue.png")
# friendly_missile_image = pygame.transform.scale(friendly_missile_image,(50,50))

TURRET_STATES = {}

TURRET_STATES[0] = pygame.transform.scale(pygame.image.load("MT0.png"), (50, 50))
TURRET_STATES[1] = pygame.transform.scale(pygame.image.load("MT1.png"), (50, 50))
TURRET_STATES[2] = pygame.transform.scale(pygame.image.load("MT2.png"), (50, 50))
TURRET_STATES[3] = pygame.transform.scale(pygame.image.load("MT3.png"), (50, 50))
TURRET_STATES[4] = pygame.transform.scale(pygame.image.load("MT4.png"), (50, 50))
TURRET_STATES[5] = pygame.transform.scale(pygame.image.load("MT5.png"), (50, 50))
TURRET_STATES[6] = pygame.transform.scale(pygame.image.load("MT6.png"), (50, 50))
TURRET_STATES[7] = pygame.transform.scale(pygame.image.load("MT7.png"), (50, 50))
TURRET_STATES[8] = pygame.transform.scale(pygame.image.load("MT8.png"), (50, 50))
TURRET_STATES[9] = pygame.transform.scale(pygame.image.load("MT9.png"), (50, 50))
TURRET_STATES[10] = pygame.transform.scale(pygame.image.load("MT10.png"), (50, 50))
TURRET_STATES[11] = pygame.transform.scale(pygame.image.load("MT11.png"), (50, 50))
TURRET_STATES[12] = pygame.transform.scale(pygame.image.load("MT12.png"), (50, 50))
TURRET_STATES[13] = pygame.transform.scale(pygame.image.load("MT13.png"), (50, 50))
TURRET_STATES[14] = pygame.transform.scale(pygame.image.load("MT14.png"), (50, 50))
TURRET_STATES[15] = pygame.transform.scale(pygame.image.load("MT15.png"), (50, 50))
image_destroyed = pygame.transform.scale(pygame.image.load("Missile_Turret_Dead.png"), (50, 50))


class silo():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = True
        # TO DO get better graphic to replace turret
        self.image = TURRET_STATES[14]
        # self.image_destroyed = pygame.transform.scale(image_destroyed,(33,42))
        self.rectangle = self.image.get_rect()
        self.rectangle.center = (x, y)
        self.ammo = 15

    def draw(self):
        if self.alive == True:
            self.image = TURRET_STATES[self.ammo]
        else:
            self.image = image_destroyed
        WINDOW.blit(self.image, self.rectangle)


class friendly_missile():
    def __init__(self, start, speed, target):
        self.start = start
        self.target = target
        self.current = self.start
        self.radius = 0
        self.color = "blue"
        self.speed = speed
        self.velocity = self.getVelocity()
        self.target_marker_color_list = ["red", "green", "violet", "white", "blue"]
        self.marker_color = 0

    def getVelocity(self):
        DiffX = (self.target[0] - self.start[0])
        DiffY = (self.target[1] - self.start[1])
        H = math.sqrt(DiffX * DiffX + DiffY * DiffY)
        if H == 0:
            return (0, 0)
        Vx = DiffX / H * self.speed
        Vy = DiffY / H * self.speed

        return (Vx, Vy)

    def step(self):
        V = self.velocity
        self.current = (self.current[0] + V[0], self.current[1] + V[1])

    def draw(self):
        # TODO: draw missile trail, step method
        # pygame.draw.circle(surface, color, center, radius)
        pygame.draw.circle(WINDOW, self.color, self.current, self.radius)

        # line(surface, color, start_pos, end_pos, width=1)
        pygame.draw.line(WINDOW, self.color, self.start, self.current, 1)
        pygame.draw.circle(WINDOW, "black", self.target, self.radius)

        if self.marker_color == 4:
            self.marker_color = 0
        else:
            self.marker_color += 1
        color = self.target_marker_color_list[self.marker_color]
        pygame.draw.line(WINDOW, color, (self.target[0] - 3, self.target[1] - 3), (self.target[0] + 3, self.target[1] + 3), 2)
        pygame.draw.line(WINDOW, color, (self.target[0] - 3, self.target[1] + 3), (self.target[0] + 3, self.target[1] - 3), 2)


class enemy_missile():
    def __init__(self, start, speed, *target):
        self.start = start
        self.target_list = [(50, 400), (225, 400), (400, 400), (575, 400)]
        self.target = self.target_list[random.randrange(0, 4)]
        # self.target = (500, 300)
        self.current = self.start
        self.radius = 2
        self.color = "red"
        self.speed = speed
        self.velocity = self.getVelocity()

    def getVelocity(self):
        Vy = self.speed
        DiffX = (self.target[0] - self.start[0])
        DiffY = (self.target[1] - self.start[1])
        Vx = (DiffX / DiffY) * Vy
        return (Vx, Vy)

    def step(self):
        V = self.velocity
        self.current = (self.current[0] + V[0], self.current[1] + V[1])

    def draw(self):
        # TODO: draw missile trail, step method
        # pygame.draw.circle(WINDOW,self.color,self.current,self.radius)

        # pygame.draw.line(surface, color, start_pos, end_pos, width=1)
        pygame.draw.line(WINDOW, "red", self.start, self.current, 2)


class explosion():
    def __init__(self, pos):
        self.position = pos
        self.frame = 0
        self.endframe = 100
        self.color_list = ["red", "green", "purple", "yellow", "blue", "white", "yellow", "orange", "white"]
        self.radius = self.frame
        self.color = 0

    def step(self):
        self.frame += 0.55
        if self.frame < 26:
            self.radius = self.frame
        else:
            self.radius = 52 - self.frame

    def draw(self):
        if self.color == 8:
            self.color = 0
        else:
            self.color += 1
        color = self.color_list[self.color]
        pygame.draw.circle(WINDOW, color, self.position, self.radius)


def distance(pos1, pos2):
    return (((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2) ** (1 / 2))


def show_score(score_value, scorex, scorey):
    # Update score variable, updating score value can be found where enemy missiles are popped and where buildings are destroyed
    score = FONT.render("Score : " + str(score_value), True, (255, 255, 255))
    WINDOW.blit(score, (scorex, scorey))


def game_over():
    print("game over")
    game_over_text = FONT.render("GAME OVER", True, (200, 200, 200))
    score_text = FONT.render("YOUR SCORE IS : " + str(score_value), True, (200, 200, 200))
    WINDOW.fill((0, 0, 0))
    WINDOW.blit(game_over_text, ((SCREENWIDTH / 2 - game_over_text.get_width() / 2), SCREENHEIGHT / 2 - 50))
    WINDOW.blit(score_text, ((SCREENWIDTH / 2 - score_text.get_width() / 2), SCREENHEIGHT / 2 - 100))

    pygame.display.update()
    time.sleep(5)


# REDRAW REDRAW REDRAW REDRAW REDRAW REDRAW REDRAW REDRAW REDRAW REDRAW REDRAW REDRAW
def redrawWindow(SILOs, FMs, EMs, EXPs):
    WINDOW.fill((0, 0, 0))

    for ID in SILOs:
        SILOs[ID].draw()
    for ID in FMs:
        FMs[ID].draw()
    for ID in EMs:
        EMs[ID].draw()
    for ID in EXPs:
        EXPs[ID].draw()
    show_score(score_value, scorex, scorey)


# declare dictionarys for objects
EMs = {}
FMs = {}
EXPs = {}
SILOs = {}

# used to give identifying key to all objects
FMid = 1000
EMid = 1000
EXPid = 1000

# initialize counters
EMCounter = EMFREQUENCY

# Test Objects
#########################################
projectile1 = enemy_missile((100, 5), 0.4)
EMs[EMid] = projectile1
EMid += 1
mouse_pos = (0, 0)
SILOs[0] = silo(50, 400)
SILOs[1] = silo(225, 400)
SILOs[2] = silo(400, 400)
SILOs[3] = silo(575, 400)

########################################

# everything is inside this while loop which causes the WINDOW to continue update through every cycle
run = True
while run:

    pygame.display.flip()

    # for loop will go through all possible user-input events like keystrokes in pygame
    for event in pygame.event.get():

        # pygame.QUIT is built into pygame and means whether the x in top right of pygame window is clicked
        if event.type == pygame.QUIT:
            # break out of while loop
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            available = False
            for ID in list(SILOs.keys()):
                if SILOs[ID].ammo > 0 and SILOs[ID].alive == True:
                    available = True
                else:
                    pass

            if available == True:
                if mouse_pos[1] <= 380:  # only fire a missile if mouse position is above launchpoint
                    distances = []
                    for ID in list(SILOs.keys()):

                        # TO DO only if silo is active do you check. make it so that it sets distance to high value if inactive
                        if SILOs[ID].alive == True and SILOs[ID].ammo > 0:
                            distances.append(abs(SILOs[ID].x - mouse_pos[0]))
                        else:  # if silo is destroyed remove possibility of it being used to launch missile
                            distances.append(100000)

                    mnv = min(distances)
                    min_pos = distances.index(mnv)
                    # reduce ammo of selected silo
                    SILOs[min_pos].ammo -= 1
                    # friendly_missile(self,start,speed,target)
                    FM = friendly_missile((SILOs[min_pos].x, 380), 3, mouse_pos)
                    FMs[FMid] = FM
                    FMid += 1
                    # use function to find closest silo
                    # create new FM object using mouse_pos and append to FMs list
                    # pass
                else:
                    pass

            else:
                pass
# -------------------------------------------------------------------

    # update object positions, checking for collision
# -------------------------------------------------------------------
    # FRIENDLY MISSILE
    for ID in list(FMs.keys()):
        FMs[ID].step()
        # if reach target explode
        if FMs[ID].current[1] <= FMs[ID].target[1]:
            # create explosion object
            EXP = explosion(FMs[ID].current)
            EXPs[EXPid] = EXP
            EXPid += 1
            # delete missile
            FMs.pop(ID)
# -------------------------------------------------------------------
    # ENEMY MISSILE

    # generate enemy missles every 2s from random locations top of screen
    if EMCounter > EMFREQUENCY:  # every constant number of loops
        EMs[EMid] = enemy_missile((random.randrange(0, SCREENWIDTH), 0), 0.4)
        EMid += 1
        EMCounter = 0
        EMs[EMid] = enemy_missile((random.randrange(0, SCREENWIDTH), 0), 0.4)
        EMid += 1
        EMCounter = 0
    else:
        EMCounter += 1

    # step all EMs, and check for explosions
    for ID in list(EMs.keys()):
        EMs[ID].step()
        # if contacting explosion explode
        for ID2 in list(EXPs.keys()):
            # add small amount for balance
            if distance(EMs[ID].current, EXPs[ID2].position) < EXPs[ID2].radius + 2:
                # create explosion and pop
                EXP = explosion(EMs[ID].current)
                EXPs[EXPid] = EXP
                EXPid += 1
                score_value += 100
                EMs.pop(ID)
                break
        # if reach target explode
        # I need the try except so it doesnt try to calculate stuff from EMS after I pop it.
        try:
            if EMs[ID].current[1] >= EMs[ID].target[1]:
                # create explosion and pop
                EXP = explosion(EMs[ID].current)
                EXPs[EXPid] = EXP
                EXPid += 1
                EMs.pop(ID)
        except:
            pass
# -------------------------------------------------------------------
    # check for buildings go boom boom
    for ID in list(SILOs.keys()):

        for ID2 in list(EXPs.keys()):
            # if contacting explosion
            if distance((SILOs[ID].x, SILOs[ID].y), EXPs[ID2].position) < EXPs[ID2].radius + 10:
                SILOs[ID].alive = False

                break

# -------------------------------------------------------------------
    # EXPLOSIONS
    for ID in list(EXPs.keys()):
        EXPs[ID].step()
        if EXPs[ID].radius <= 0:
            EXPs.pop(ID)
# -------------------------------------------------------------------

    redrawWindow(SILOs, FMs, EMs, EXPs)

    # updates display WINDOW, draws all elements
    pygame.display.update()

    # tells python that this while true loop should not run faster
    # each tick is 1ms, so each loop should be 60ms
    clock.tick(GAMESPEED)

    # End game once all silos destroyed, use game_over function
    if SILOs[0].alive == False and SILOs[1].alive == False and SILOs[2].alive == False and SILOs[3].alive == False:
        run = False
        game_over()

# use pygame.quit() because to uninitialize all things pygame
pygame.quit()
quit()