#--------------------------------------------------------------------------
# Name:        LvlMap
# Purpose:     Handles all the maps that make up a level.
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
import Map
import TileMap
import EntityMap
import _ENV_VAR as ENV
import GameExceptions as ERR


class LvlMap(object):

    def __init__(self, maxX, maxY):
        self.maxX, self.maxY = maxX, maxY
        self.tiles = TileMap.TileMap(self.maxX, self.maxY)
        self.entities = EntityMap.EntityMap(self.maxX, self.maxY)
        self.cache = Map.Map(self.maxX, self.maxY)
        self.updates = []  # stores pos of recent updates to limit calls
        test = self.tiles.getArray()
        self.maxY, self.maxX = len(test), len(test[0])

    def _getTargetVars(self, target):
        """
        Returns variables to be used by another funtion to modify map.

        Returns:
        x, y, - int - Coords of target.
        targetMap - Map Object that contains the target.
        """
        x, y = target.getPos()
        tag = target.getTag()
        if tag == "entity":
            targetMap = self.entities
        elif tag == "item":
            pass
        elif tag == "tile":
            targetMap = self.tiles
        else:
            raise ERR.InvalidGameObject("Given Game Object not valid.")
        return x, y, targetMap

    def getMax(self):
        """
        Returns self.maxX and self.maxY
        """
        return self.maxX, self.maxY

    def getTarget(self, x, y, tag=None):
        """
        Takes coords of object in tile, entity, item maps and returns the
        'topmost' object unless a tag is specified.

        x, y - int - coords of object to be returned.
        """
        if tag == "entity" or self.entities.getPos(x, y) is not None:
            target = self.entities.getPos(x, y)
        elif tag == "tile" or self.tile.getPos(x, y) is not None:
            target = self.tile.getPos(x, y)
        return target

    def testTilePassable(self, x, y):
        return self.tiles.testMapPos(x, y)

    def getDisplay(self, x, y):
        """
        Returns the map object that is "on top" so that it can be drawn

        x, y - int - Coords of the map location to return display info for.

        returns:
        img - str - Currently the character of the object's display info.
        color - tuple - The (red, green, blue) value of cobject's display info.
        """
        if self.entities.getPos(x, y) is not None:
            img, color = self.entities.getPos(x, y).display()
        else:
            img, color = self.tiles.getPos(x, y).display()
        return img, color

    def getDisplayFromCache(self, x, y):
        """
        Returns the display info for the given coords in self.cache

        x, y - int - Coords of the map location to return display info for.

        returns:
        img - str - Currently the character of the cached display info.
        color - tuple - The (red, green, blue) value of cached display info.
        """
        disp = self.cache.getPos(x, y)
        return disp[0], disp[1]

    def addUpdates(self, *args):
        """
        Appends a tuple with coordinates to self.updates
        """
        for arg in args:
            self.updates.append(arg)

    def addEntity(self, x, y, entity):
        """
        puts object in objArray.
        """
        if self.entities.testMapPos(x, y) and self.tiles.testMapPos(x, y):
            self.entities.setPos(x, y, entity)
        else:
            raise ERR.NotValidMapLocation("Cannot add entity: Occupied.")

    def iterLvl(self, x1, y1, x2, y2, lit):
        """
        Generator that yields the appropriate drawing information from
        the tile, entity, item, and other maps.

        x1, y1 - int - The min coords of the map section to be drawn
        x2, y2 - int - The max coords of the map section to be drawn
        lit - list - A list of coords as tuples that represent lit tiles
                     all other tiles must be drawn from cache.

        returns:
        img - str - Currently the character of the referenced display info.
        color - tuple - The (red, green, blue) val of referenced display info.
        relativeX, relativeY - int - Pos of tile relative to x1, x2 as 0, 0.
        """
        relY = -1
        for Y in range(y1, y2):
            relY += 1
            relX = -1
            for X in range(x1, x2):
                relX += 1
                p = (X, Y)  # p as x, y Position
                toBeCached = True
                if p in lit or (p in lit and p in self.updates):
                    img, color = self.getDisplay(X, Y)
                elif p in lit and p not in self.updates:
                    if self.cache.getPos(X, Y) is None:
                        img, color = self.getDisplay(X, Y)
                    else:
                        toBeCached = False
                        img, color = self.getDisplayFromCache(X, Y)
                else:
                    toBeCached = False
                    if self.cache.getPos(X, Y) is None:
                        img = ENV.tileImgs.getImgObj(-1, -1)
                        color = (0, 0, 0)
                    else:
                        img, color = self.getDisplayFromCache(X, Y)
                if toBeCached:
                    self.cache.setPos(X, Y, (img, color))
                yield (img, color, relX, relY, X, Y)
        self.updates = []

    def mvTarget(self, x1, y1, target):
        """
        Places specified target in a new location and removes it from it's
        original one. Throws error if move is not valid or possible.

        x1, y1 - int - Coords to move target to.
        target - GameObject - The target to move.
        """
        x2, y2, targetMap = self._getTargetVars(target)
        if targetMap.testMapPos(x1, y1) is False:
            raise ERR.LocationOccupied("This location is already occupied")
        if self.tiles.testMapPos(x1, y1) is False:
            raise ERR.NotValidMapLocation("Invalid map position given")
        else:
            targetMap.setPos(x1, y1, target)
            targetMap.setPos(x2, y2, None)

    def rmTarget(self, target):
        """
        Removes specified target from it's original location. Throws error
        if move is not valid or possible.

        target - GameObject - The target to move.
        """
        x, y, targetMap = self._getTargetVars(target)
        targetMap.setPos(x, y, None)

    def swTarget(self, target, subject):
        """
        Swaps Game Objects in place
        """
        pass  # Not implemented.

