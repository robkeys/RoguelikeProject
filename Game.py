#--------------------------------------------------------------------------
# Name:         Game
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
import _ENV_VAR as _E


class Game(object):

    def __init__(self):
        # start pygame.
        pygame.init()

        # pygame variables

        self.wSize = [700, 500]  # <-- something better here
        self.screen = pygame.display.set_mode(self.wSize, pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Courier', 24)

        # intial game objects.
        self.lvlMap = Map.ObjectMap(70, 50)
        self.player = BaseGameObj.Player(1, 1)

        # other variables
        self.met = self.font.metrics('@')[0]

        # Initial declarations
        self.setCaption("RoguelikeProject")

    def setCaption(self, caption):
        """
        Sets game window caption.
        """
        pygame.display.set_caption(caption)

    def getPlayer(self):
        """
        Returns current player object
        """
        return self.player

    def o_UpdateObj(self, gameObject, newX, newY):
        """
        This function takes a game object as an argument as well as the
        change in the map coords of the potential new location of the
        object. It checks if the move is valid/possible and if we are all
        good it does it.

        gameObject - any superclass of BaseGameObject (players & monsters)
        newX, newY - int, int - change in objects current map coords
        """
        oldPos = gameObject.getPos()                   # get old position
        newPos = (oldPos[0] + newX, oldPos[1] + newY)  # add new position
        try:
            # check if valid position while assigning var
            newMapPos = self.lvlMap.getMapObject(newPos)
        except GameExceptions.NotValidMapLocation as err:
            # oop. Not really there.
            print err.args
        else:
            oldMapPos = self.lvlMap.getMapObject(oldPos)
            # all vars set. we move the gameObj to the new space
            newMapPos.fillSpace(gameObject)
            # empty the old space
            oldMapPos.emptySpace()
            # and inform the gameObj of it's new home
            gameObject.updatePos(newX, newY)

    def m_FindDrawnArea(self):
        """
        Using player map location this finds the area of the map to be
        drawn in the frame. Must happen after player update.

        Returns - x, y - coords of top right corner of map area.
        """
        winX = self.wSize[0] / self.met[1]        # using win size
        winY = self.wSize[1] / (self.met[4] + 8)  # get viewable area
        # map max coord
        ext = self.lvlMap.getMaxX(), self.lvlMap.getMaxY()
        if ext[0] < winX:   # |
            winX = ext[0]   # If map bounadary is greater than the
        if ext[1] < winY:   # boundary we got from window size then
            winY = ext[0]   # just make window size = map size
        win = (winX, winY)  # |

        half = (win[0] / 2, win[1] / 2)  # half max window coords
        ply = self.player.getPos()       # player coords

        #print "win: " + str(win)      # |
        #print "half: " + str(half)    # |
        #print "ext: " + str(ext)      # Debug stuff. Get rid of it.
        #print "ply: " + str(ply)      # |

        start, end = [0, 0], [0, 0]
        for i in range(2):
            if ply[i] - half[i] >= 0 and ply[i] + half[i] < ext[i]:
                start[i] = ply[i] - half[i]          # If within bounds
                end[i] = ply[i] + half[i]
            elif ply[i] - half[i] < 0 and ply[i] + half[i] < ext[i]:
                start[i] = 0                         # If at top/left
                end[i] = win[i]                      # but max in bounds
            elif ply[i] - half[i] >= 0 and ply[i] + half[i] >= ext[i]:
                start[i] = ext[i] - win[i]           # If at bottom/right
                end[i] = ext[i]                      # but min in bounds
            else:
                start[i] = 0                         # map is smaller
                end[i] = ext[i]                      # than viewable area

        #print "result: " + str(start), str(end)
        return (start[0], start[1]), (end[0], end[1])  # minInd, maxInd

    def newFrame(self):
        """
        Draws the new frame, and then flips the display
        """
        # Set the screen background
        self.screen.fill(_E.black)

        # Blit GameObjects
        minInd, maxInd = self.m_FindDrawnArea()
        drawX, drawY = 0, 0
        for char in self.lvlMap.drawMap(minInd, maxInd):
            if char == '\n':
                drawX = 0
                drawY += self.met[4] + 8
            else:
                mapText = self.font.render(char, 1, _E.white, _E.black)
                self.screen.blit(mapText, (drawX, drawY))
                drawX += self.met[1]

        # Limit to 20 frames per second
        self.clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()


