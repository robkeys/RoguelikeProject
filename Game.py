#--------------------------------------------------------------------------
# Name:         Game
# Purpose:      Controls aspects of running game
#
# Author:      Rob Keys
#
# Created:     05/04/2013
# Copyright:   (c) 2013, Rob Keys
# Licence:     This software is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with the software; If not, see <http://www.gnu.org/licenses/>.
#--------------------------------------------------------------------------
import pygame
import BaseGameObj
import Monsters
import Map
import GameExceptions
import random
import _ENV_VAR as _E


class Game(object):

    def __init__(self):
        # start pygame.
        pygame.init()

        # pygame variables

        self.wSize = [700, 500]  # <-- something better here
        self.screen = pygame.display.set_mode(self.wSize, pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.font = None
        self.fontName = "cour.ttf"
        self.fontSize = 24
        self.fontDict = {}

        # intial game objects.
        self.lvlMap = Map.ObjectMap(70, 50)
        self.player = BaseGameObj.Player(1, 1)
        self.monsters = Monsters.Monsters()

        # Initial declarations
        self.setFont(self.fontName, self.fontSize)
        self.setCaption("RoguelikeProject")

        # other variables
        self.met = self.font.metrics('@')[0]

    def setDisplay(self, size, args):
        """
        Sets the display
        """
        self.screen = pygame.display.set_mode(size, args)
        self.wSize = size

    def setFont(self, fontName, fontSize):
        """
        Just sets the font. No big.
        """
        try:
            self.font = self.fontDict[fontName]
        except KeyError:
            self.createFont(fontName, fontSize)

    def createFont(self, fontName, fontSize):
        """
        Creates fonts. Crazy.
        """
        self.font = pygame.font.Font(fontName, fontSize)
        self.fontDict[fontName] = self.font

    def setCaption(self, caption):
        """
        Sets game window caption.
        """
        pygame.display.set_caption(caption)

    def p_GetPlayer(self):
        """
        Returns current player object
        """
        return self.player

    def p_MovePlayer(self, newX, newY):
        """
        Updates player pos if no error is raised.
        """
        try:
            self.o_UpdateObj(self.player, newX, newY)
        except GameExceptions.NotValidMapLocation as err:
            print err.args


    def o_GenMonsters(self, numMonsters):
        """
        Finds a valid map location and inserts a monster.
        """
        lenX = self.lvlMap.getMaxX()
        lenY = self.lvlMap.getMaxY()
        for monster in xrange(numMonsters):
            self.monsters.addMonster((0, 0))
            newMonster = self.monsters.getMonster()
            while True:
                x = random.randrange(lenX)
                y = random.randrange(lenY)
                newMonster.setPos(x, y)
                try:
                    self.o_UpdateObj(newMonster, x, y)
                except GameExceptions.NotValidMapLocation:
                    pass
                else:
                    break

    def o_ValidateMonsterMove(self, pos):
        """
        Returns True if move was successfull
        """
        try:
            return self.lvlMap.testMapPos(pos)
        except GameExceptions.NotValidMapLocation:
            return False


    def o_MoveMonsters(self):
        """
        Moves all living monsters
        """
        count = 0
        for monster in self.monsters.iterMonsters():
            count += 1
            if monster.getAlive():
                for i in xrange(5):
                    oldPos = monster.getPos()
                    newPos = monster.move(self.player.getPos())
                    try:
                        self.o_UpdateObj(monster, newPos[0], newPos[1])
                    except GameExceptions.NotValidMapLocation:
                        monster.setPos(oldPos[0], oldPos[1])
                    else:
                        print "old", str(count), "=", str(oldPos)
                        print "move", str(count), "=", str(newPos)
                        break

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
            raise err
        else:
            oldMapPos = self.lvlMap.getMapObject(oldPos)
            # Fill the new space
            newMapPos.fillSpace(gameObject)
            if oldPos != newPos:
                # empty the old space
                oldMapPos.emptySpace()
            # and inform the gameObj of it's new home
            gameObject.updatePos(newX, newY)
            print "o_UpdateObj: ", str(gameObject.getPos())

    def m_FindDrawnArea(self):
        """
        Using player map location this finds the area of the map to be
        drawn in the frame. Must happen after player update.

        Returns - x, y - coords of top right corner of map area.
        """
        winX = self.wSize[0] / self.met[1]        # using win size
        winY = self.wSize[1] / (self.met[4] + 8)       # get viewable area
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
            if char[0] == 0:
                drawX = 0
                drawY += self.met[4] + 8
            else:
                if char[0] in ['#', '@']:
                    self.setFont("courbd.ttf", self.fontSize)
                # print "char: ", str(char)
                # print "char[0]: ", str(char[0])
                mapText = self.font.render(char[0], char[1], char[2], char[3])
                self.screen.blit(mapText, (drawX, drawY))
                self.setFont(self.fontName, self.fontSize)
                drawX += self.met[1]

        # Limit to 20 frames per second
        self.clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()


