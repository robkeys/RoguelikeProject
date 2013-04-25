#--------------------------------------------------------------------------
# Name:         GameLoop
# Purpose:      Controls aspects of running game
#
# Author:      robk
#
# Created:     05/04/2013
# Copyright:   (c) robk 2013
# Licence:     <your licence>
#--------------------------------------------------------------------------
import pygame
import BaseGameObj
import Map
import GameExceptions

# Define some colors
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)

pygame.init()

# Set the height and width of the screen
size = [700, 500]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
font = pygame.font.SysFont('Courier', 24)

lvlMap = Map.ObjectMap(100, 100)
player = BaseGameObj.Player(1, 1)


def updateMapPos(gameObject, newX, newY):
    oldPos = gameObject.getPos()
    newPos = (oldPos[0] + newX, oldPos[1] + newY)
    try:
        newMapPos = lvlMap.getMapObject(newPos)
    except GameExceptions.NotValidMapLocation as err:
        print err.args
    else:
        oldMapPos = lvlMap.getMapObject(oldPos)
        newMapPos.fillSpace(gameObject)
        oldMapPos.emptySpace()
        gameObject.updatePos(newX, newY)
    finally:
        print gameObject.getPos()

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:
            done = True  # Flag that we are done so we exit this loop
        elif hasattr(event, 'key') and hasattr(event, 'unicode'):
            if event.key == pygame.K_ESCAPE:
                done = True
            if event.key == pygame.K_UP:
                updateMapPos(player, -1, 0)
            if event.key == pygame.K_DOWN:
                updateMapPos(player, 1, 0)
            if event.key == pygame.K_LEFT:
                updateMapPos(player, 0, -1)
            if event.key == pygame.K_RIGHT:
                updateMapPos(player, 0, 1)

    # Set the screen background
    screen.fill(black)

    # Blit GameObjects
    mapX = 0
    mapY = 0
    for char in lvlMap.drawMap():
        met = font.metrics('@')[0]
        if char == '\n':
            mapX = 0
            mapY += met[4] + 4
        else:
            mapText = font.render(char, 1, white)
            screen.blit(mapText, (mapX, mapY))
            mapX += met[1]

    # Blit game objects
    #text = font.render(player.getChar(), 1, white)
    #screen.blit(text, player.getPos())

    # Limit to 20 frames per second
    clock.tick(60)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
