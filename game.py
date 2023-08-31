import random
import sys
import pygame
from pygame.locals import *

#global Var
FPS = 40
GAMEWIDTH = 290
GAMEHEIGHT = 510
SCREEN = pygame.display.set_mode((GAMEWIDTH,GAMEHEIGHT))
BASEY = GAMEHEIGHT * 0.8
GAME_SPRITES = {}
GAME_AUDIO = {}
ACTOR = "visuals/bird.png"
BG = "visuals/background.jpg"
OBSTACLE = "visuals/tube.png"


def start():
    actorx = int(GAMEWIDTH/5)
    actory = int((GAMEHEIGHT - GAME_SPRITES["actor"].get_height())/2)
    startx = int((GAMEWIDTH - GAME_SPRITES["start"].get_width())/2)
    starty = int(GAMEHEIGHT*0.4)
    basex = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            
            else:
                SCREEN.blit(GAME_SPRITES["bg"],(0,0))
                SCREEN.blit(GAME_SPRITES["actor"],(actorx,actory))
                SCREEN.blit(GAME_SPRITES["start"],(startx,starty))
                SCREEN.blit(GAME_SPRITES["base"],(basex,BASEY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def isCollide(actorx,actory,upperObs,lowerObs):
    if actory > BASEY - 25 or actory < 0:
        GAME_AUDIO["hit"].play()
        return True
    for obs in upperObs:
        obsHeight = GAME_SPRITES['obs'][0].get_height()
        if(actory < obsHeight + obs['y'] and abs(actorx - obs['x']) < GAME_SPRITES["obs"][0].get_width()):
            GAME_AUDIO["hit"].play()
            return True
        
    for obs in lowerObs:
        if (actory + GAME_SPRITES['actor'].get_height() > obs['y']) and abs(actorx - obs['x']) < GAME_SPRITES["obs"][0].get_width():
            GAME_AUDIO["hit"].play()
            return True
    
    return False


def flap():
    score = 0
    actorx = int(GAMEWIDTH/5)
    actory = int(GAMEWIDTH/5)
    basex = 0

    newObs1 = randomObs()
    newObs2 = randomObs()

    upperObs = [
        {"x":GAMEWIDTH + 200,"y":newObs1[0]['y']},
        {"x":GAMEWIDTH+200+(GAMEWIDTH/2),"y":newObs2[0]['y']}
    ]
    lowerObs = [
        {"x":GAMEWIDTH + 200,"y":newObs1[1]['y']},
        {"x":GAMEWIDTH+200+(GAMEWIDTH/2),"y":newObs2[1]['y']}
    ]

    obsVeloX = -4
    actorVeloY = -9
    actorMaxVeloY = 10
    actorMinVeloY = -8
    actorAccY = 1

    flapAcc = -8
    flapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if actory > 0:
                    actorVeloY = flapAcc
                    flapped = True
                    GAME_AUDIO["flap"].play()

        crash = isCollide(actorx,actory,upperObs,lowerObs)
        if crash:
            return
        
        actorPos = actorx + GAME_SPRITES['actor'].get_width()/2
        for obs in upperObs:
            obsMidPos = obs['x'] + GAME_SPRITES['obs'][0].get_width()/2
            if obsMidPos <= actorPos < obsMidPos+4:
                score = score+1
                print(score)
                GAME_AUDIO["score"].play()

        if actorVeloY < actorMaxVeloY and not flapped:
            actorVeloY = actorVeloY + actorAccY

        if flapped:
            flapped = False
        actorHeight = GAME_SPRITES['actor'].get_height()
        actory = actory + min(actorVeloY,BASEY - actory - actorHeight)

        for upperOb,lowerOb in zip(upperObs,lowerObs):
            upperOb['x'] += obsVeloX
            lowerOb['x'] += obsVeloX

        if 0<upperObs[0]['x']<5:
            newObs = randomObs()
            upperObs.append(newObs[0])
            lowerObs.append(newObs[1])

        if upperObs[0]['x'] < -GAME_SPRITES['obs'][0].get_width():
            upperObs.pop(0)
            lowerObs.pop(0)

        SCREEN.blit(GAME_SPRITES["bg"],(0,0))
        for upperOb,lowerOb in zip(upperObs,lowerObs):
            SCREEN.blit(GAME_SPRITES["obs"][0],(upperOb['x'],upperOb['y']))
            SCREEN.blit(GAME_SPRITES["obs"][1],(lowerOb['x'],lowerOb['y']))
            
        SCREEN.blit(GAME_SPRITES["base"],(basex,BASEY))
        SCREEN.blit(GAME_SPRITES["actor"],(actorx,actory))

        myScore = [int(x) for x in list(str(score))]
        width = 0
        for digit in myScore:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (GAMEWIDTH - width)/2

        for digit in myScore:
            SCREEN.blit(GAME_SPRITES["numbers"][digit],(Xoffset,GAMEHEIGHT*0.12))
            Xoffset += GAME_SPRITES["numbers"][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def randomObs():
    obsHeight = GAME_SPRITES["obs"][0].get_height()
    offset = GAMEHEIGHT/3
    y2 = offset + random.randrange(0,int(GAMEHEIGHT - GAME_SPRITES['base'].get_height() - 1.2*offset))
    obsX = GAMEWIDTH + 10
    y1 = obsHeight - y2 + offset
    obs = [{'x': obsX, "y":-y1},
           {'x':obsX,"y":y2}]
    return obs


if __name__ == "__main__":
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("FLAP")
    GAME_SPRITES["numbers"]  = (
        pygame.image.load("visuals/0.png").convert_alpha(),
        pygame.image.load("visuals/1.png").convert_alpha(),
        pygame.image.load("visuals/2.png").convert_alpha(),
        pygame.image.load("visuals/3.png").convert_alpha(),
        pygame.image.load("visuals/4.png").convert_alpha(),
        pygame.image.load("visuals/5.png").convert_alpha(),
        pygame.image.load("visuals/6.png").convert_alpha(),
        pygame.image.load("visuals/7.png").convert_alpha(),
        pygame.image.load("visuals/8.png").convert_alpha(),
        pygame.image.load("visuals/9.png").convert_alpha()
    )
    GAME_SPRITES["start"] = pygame.image.load("visuals/start.png").convert_alpha()
    GAME_SPRITES["base"] = pygame.image.load("visuals/base.png").convert_alpha()
    GAME_SPRITES["obs"] = (pygame.transform.rotate(pygame.image.load(OBSTACLE).convert_alpha(),180),
                           pygame.image.load(OBSTACLE).convert_alpha())
    GAME_SPRITES["bg"] = pygame.image.load("visuals/background.png").convert()
    GAME_SPRITES['actor'] = pygame.image.load(ACTOR).convert_alpha()

    GAME_AUDIO["hit"] = pygame.mixer.Sound("audio/hit.mp3")
    GAME_AUDIO["score"] = pygame.mixer.Sound("audio/score.mp3")
    GAME_AUDIO["flap"] = pygame.mixer.Sound("audio/flap.mp3")

    while True:
        start()
        flap()
