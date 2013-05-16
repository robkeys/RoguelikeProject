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
import math
import pygame
import random
import BaseGameObj
import Monsters
import LvlMap
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
        self.lvlMap = LvlMap.LvlMap(70, 50)
        self.player = BaseGameObj.Player(0, 0)
        self.monsters = Monsters.Monsters()

        # map variables
        self.lit = []

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

    def p_PlayerStartPos(self):
        """
        Finds valid map location to place the player object.
        """
        while True:
            x, y = self.player.getPos()
            try:
                self.lvlMap.addEntity(x, y, self.player)
            except (GameExceptions.NotValidMapLocation, IndexError):
                self.player.updatePos(1, 1)
            else:
                break

    def o_GenMonsters(self, numMonsters):
        """
        Finds a valid map location and inserts a monster.
        """
        lenX, lenY = self.lvlMap.getMax()
        for monster in xrange(numMonsters):
            self.monsters.addMonster((0, 0))
            newMonster = self.monsters.getMonster()
            while True:
                x = random.randrange(lenX)
                y = random.randrange(lenY)
                newMonster.setPos(x, y)
                try:
                    self.o_UpdateObj(newMonster, x, y)
                except IndexError:
                    pass
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
                    playerX, playerY = self.player.getPos()
                    newPos = monster.move(playerX, playerY)
                    try:
                        self.o_UpdateObj(monster, newPos[0], newPos[1])
                    except (GameExceptions.NotValidMapLocation, IndexError):
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
        oldX, oldY = gameObject.getPos()                   # get old position
        X, Y = (oldX + newX, oldY + newY)  # add new position
        if kill:
            self.lvlMap.rmTarget(gameObject)
        else:
            try:
                self.lvlMap.mvTarget(X, Y, gameObject)
            except GameExceptions.NotValidMapLocation as err:
                raise err
            except GameExceptions.LocationOccupied:
                subject = self.lvlMap.getTarget(X, Y, "entity")
                self.o_Interact(gameObject, subject)
            else:
                gameObject.updatePos(newX, newY)
        self.lvlMap.addUpdates((oldX, oldY), (X, Y))

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
        ext = (x, y) = self.lvlMap.getMax()
        if ext[0] < winX:   # |
            winX = ext[0]   # If map bounadary is greater than the
        if ext[1] < winY:   # boundary we got from window size then
            winY = ext[0]   # just make window size = map size
        win = (winX, winY)  # |

        half = (win[0] / 2, win[1] / 2)  # half max window coords
        ply = (x, y) = self.player.getPos()       # player coords

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

        return start[0], start[1], end[0], end[1]  # minX, minY, maxX, maxY

    def isBlocked(self, passable, x, y, bounds):
        """
        Returns True if tile is blocked from light source
        """
        return (not passable or x < bounds[0] or
                y < bounds[1] or x >= bounds[2] or y >= bounds[3])

    def m_FindLitArea(self, minX, minY, maxX, maxY):
        """
        Generates a list of tile coords to be lit/visible to player.
        Borrowed heavily from Python shadowcasting implementation on
        roguebasin.roguelikedevelopment.org direct: http://goo.gl/Bg5Qq
        """
        self.lit = []
        ox, oy = self.player.getPos()
        self.lit.append((ox, oy))
        #ox, oy = self.lit[0][0], self.lit[0][1]
        radius = self.player.getSight()
        bounds = (minX, minY, maxX, maxY)
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
                actX = ox + (relX * mult[0]) + (relY * mult[1])
                actY = oy + (relX * mult[2]) + (relY * mult[3])
                lSlope = (relX - 0.5) / (relY + 0.5)
                rSlope = (relX + 0.5) / (relY - 0.5)
                if start < rSlope:
                    continue
                elif end > lSlope:
                    break
                else:
                    try:
                        passable = self.lvlMap.testTilePassable(actX, actY)
                    except IndexError:
                        passable = False
                    if relX * relX + relY * relY < radiusSquared and \
                                 bounds[0] <= actX < bounds[2] and \
                                 bounds[1] <= actY < bounds[3]:
                        self.lit.append((actX, actY))
                        #if (actualX, actualY) not in self.seen:
                            ## tile has not been seen yet. add it to list
                            #self.seen[actualX][actualY] =
                    if blocked:
                        if self.isBlocked(passable, actX, actY, bounds):
                            new_start = rSlope
                            continue
                        else:
                            blocked = False
                            start = new_start
                    else:
                        if self.isBlocked(passable, actX, actY, bounds):
                            if i < radius:
                                blocked = True
                                self.m_LightSect(ox, oy, i + 1, start, lSlope,
                                                 radius, bounds, mult)
                                new_start = rSlope
            if blocked:
                break

    def getLightColor(self, color, x2, y2, flicker):
        """
        Adjust tile color based on proximity to light
        """
        if (x2, y2) in self.lit:
            sight = self.player.getSight()
            sightInc = 1.0 / (sight + random.choice((-1, 0, 1)))
            x1, y1 = self.player.getPos()
            if (x1, y1) == (x2, y2):
                return color
            prox = sight - math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
            adj = int(prox * (60 * sightInc)) + flicker
            red = max(0, min(color[0] + adj * 2, 255))
            green = max(0, min(color[1] + adj / 2, 255))
            blue = min(255, max(color[2] - adj, 0))
        else:
            red = min(255, max(color[0] - 100, 0))
            green = min(255, max(color[1] - 100, 0))
            blue = min(255, max(color[2] - 75, 0))
        tileColor = red, green, blue
        return tileColor

    def newFrame(self, flicker):
        """
        Draws the new frame, and then flips the display
        """
        # Set the screen background
        self.screen.fill(_E.black)

        # Blit GameObjects
        minX, minY, maxX, maxY = self.m_FindDrawnArea()
        # flicker = int(random.random() * 30)
        self.m_FindLitArea(minX, minY, maxX, maxY)
        drawX, drawY = 0, 0
        for tile in self.lvlMap.iterLvl(minX, minY, maxX, maxY, self.lit):
            img, color, bg = tile[0], tile[1], tile[2]
            relX, relY = tile[3], tile[4]
            X, Y = tile[5], tile[6]
            if relX == 0 and drawX != 0:  # new row
                drawX = 0
                drawY += self.met[4] + 8
            if img in ['#', '@']:
                self.setFont("courbd.ttf", self.fontSize)
            color = self.getLightColor(color, X, Y, flicker)
            mapText = self.font.render(img, 1, color, bg)
            self.screen.blit(mapText, (drawX, drawY))
            self.setFont(self.fontName, self.fontSize)
            drawX += self.met[1]

        # Limit to 20 frames per second
        self.clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()


