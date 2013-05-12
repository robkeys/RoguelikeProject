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
import random
import BaseGameObj
import Monsters
import Map
import GameExceptions
import Damage as _DMG
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

    def o_MoveMonsters(self):
        """
        Moves all living monsters
        """
        count = 0
        for monster in self.monsters.iterMonsters():
            if not monster.isAlive():
                self.o_UpdateObj(monster, kill=True)
                self.monsters.remMonster(monster)
            else:
                count += 1
                for i in xrange(5):
                    oldPos = monster.getPos()
                    newPos = monster.move(self.player.getPos())
                    try:
                        self.o_UpdateObj(monster, newPos[0], newPos[1])
                    except GameExceptions.NotValidMapLocation:
                        monster.setPos(oldPos[0], oldPos[1])
                    else:
                        break

    def o_UpdateObj(self, gameObject, newX=0, newY=0, kill=False):
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
        if kill:
            self.lvlMap.setObjArray(oldPos)
        else:
            try:
                # check if valid move
                legal = self.lvlMap.testMapPos(newPos, testLegal=True)
            except GameExceptions.NotValidMapLocation as err:
                raise err
            else:
                if legal:
                    # Fill the new space
                    self.lvlMap.setObjArray(newPos, gameObject)
                    # empty the old space
                    self.lvlMap.setObjArray(oldPos)
                    # and inform the gameObj of it's new home
                    gameObject.updatePos(newX, newY)
                elif not legal:
                    subject = self.lvlMap.getMapTile(newPos)
                    self.o_Interact(gameObject, subject)

    def o_Interact(self, initObj, subject):
        """
        Uses context to determine the action the initiator object takes.

        initiator - game object that started the interaction
        target - game object that is the subject of the interaction
        """
        if initObj.isAggressive(subject.getTypes()):  # check if hostile
            # The following might work best in a combat handling class
            try:  # Did attack succeed?
                potentialDmg, dmgTypes = initObj.getDamage(subject.getDef())
            except Exception as err:
                print err.args
            else:
                dmg = _DMG.Damage(potentialDmg, dmgTypes)
                dmgMods = []
                #  Did they dodge & by how much. initObj has a change to
                #  correct for the dodge with reaction adj.
                dmgMods.append(subject.dodge(dmg, initObj.getReact()))
                #  Did armor protect the subject & by how much. Different
                #  damage types might effect armor differently. Also Armor
                #  wear and tear could be updated in this step.
                dmgMods.append(subject.armor(dmg))
                #  Damage is modified
                dmg.getDMG(dmgMods)
                #  The subject now has modified damage applied
                subject.applyDmg(dmg)

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

        return (start[0], start[1]), (end[0], end[1])  # minInd, maxInd

    def isBlocked(self, tile, x, y, bounds):
        """
        Returns True if tile is blocked from light source
        """
        return (tile is None or x < bounds[0] or y < bounds[1] or
                x >= bounds[2] or y >= bounds[3])

    def m_FindLitArea(self, minInd, maxInd):
        """
        Generates a list of tile coords to be lit/visible to player.
        Borrowed heavily from Python shadowcasting implementation on
        roguebasin.roguelikedevelopment.org direct: http://goo.gl/Bg5Qq
        """
        self.lit = []
        self.lit.append(self.player.getPos())
        ox, oy = self.lit[0][0], self.lit[0][1]
        radius = self.player.getSight()
        bounds = (minInd[0], minInd[1], maxInd[0], maxInd[1])
        for n in range(8):
            mult = (_E.mult[0][n], _E.mult[1][n], _E.mult[2][n], _E.mult[3][n])
            self.m_LightSect(ox, oy, 1, 1.0, 0.0, radius, bounds, mult)

    def m_LightSect(self, ox, oy, row, start, end, radius, bounds, mult):
        """
        steps through tiles determining if they are lit or not.
        """
        if start < end:
            return
        radiusSquared = radius * radius
        for i in range(row, radius + 1):
            relX, relY = -i - 1, -i  # Relative position of x, y coords
            blocked = False
            while relX <= 0:
                relX += 1
                actualX = ox + (relX * mult[0]) + (relY * mult[1])
                actualY = oy + (relX * mult[2]) + (relY * mult[3])
                lSlope = (relX - 0.5) / (relY + 0.5)
                rSlope = (relX + 0.5) / (relY - 0.5)
                if start < rSlope:
                    continue
                elif end > lSlope:
                    break
                else:
                    try:
                        tile = self.lvlMap.getMapTile((actualX, actualY))
                    except GameExceptions.NotValidMapLocation:
                        tile = None
                    if relX * relX + relY * relY < radiusSquared and \
                                 bounds[0] <= actualX < bounds[2] and \
                                 bounds[1] <= actualY < bounds[3]:
                        self.lit.append((actualX, actualY))
                    if blocked:
                        if self.isBlocked(tile, actualX, actualY, bounds):
                            new_start = rSlope
                            continue
                        else:
                            blocked = False
                            start = new_start
                    else:
                        if self.isBlocked(tile, actualX, actualY, bounds):
                            if i < radius:
                                blocked = True
                                self.m_LightSect(ox, oy, i + 1, start, lSlope,
                                                 radius, bounds, mult)
                                new_start = rSlope
            if blocked:
                break

    def newFrame(self):
        """
        Draws the new frame, and then flips the display
        """
        # Set the screen background
        self.screen.fill(_E.black)

        # Blit GameObjects
        minInd, maxInd = self.m_FindDrawnArea()
        self.m_FindLitArea(minInd, maxInd)
        # Here we could call the lighting function to generate a new
        # list of lit squares
        drawX, drawY = 0, 0
        for tile in self.lvlMap.drawMap(minInd, maxInd):
            if tile[0] == 0:  # new row
                drawX = 0
                drawY += self.met[4] + 8
            elif tile[4] in self.lit:
                if tile[0] in ['#', '@']:
                    self.setFont("courbd.ttf", self.fontSize)
                # print "tile: ", str(tile)
                # print "tile[0]: ", str(tile[0])
                mapText = self.font.render(tile[0], tile[1], tile[2], tile[3])
                self.screen.blit(mapText, (drawX, drawY))
                self.setFont(self.fontName, self.fontSize)
                drawX += self.met[1]
            else:  # draw a blank space
                mapText = self.font.render(" ", 1, _E.black, _E.black)
                self.screen.blit(mapText, (drawX, drawY))
                drawX += self.met[1]

        # Limit to 20 frames per second
        self.clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()


