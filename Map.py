#--------------------------------------------------------------------------
# Name:        Map
# Purpose:  Does map stuff
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
import TileHandler
import GameExceptions as _ERR
import _ENV_VAR as _E


class ObjectMap(object):

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.mapList = ""
        self.tiles = TileHandler.TileHandler()
        self.objects = []
        self.tileArray, self.objArray = self.makeMap(x, y)
        self.toggle = 0

    def setMap(self, mapList):
        """
        Takes str as argument and sets to self.mapList
        """
        self.mapList = mapList

    def getMaxX(self):
        """
        Returns int representing the extent of the Map's x coords
        """
        return self.x

    def getMaxY(self):
        """
        Returns int representing the extent of the Map's y coords
        """
        return self.y

    def getTileArray(self):
        """
        Returns 2d array containing map elements
        """
        return self.tileArray

    def getMap(self, minInd, maxInd):
        """
        Uses map array to return map as a list of values required by pygame
        to blit the tile.

        minInd, maxInd - tuple, tuple - the two corners of the map to draw
        """
        newMapList = []
        yCount = minInd[1]
        while yCount < maxInd[1]:
            xCount = minInd[0]
            while xCount < maxInd[0]:
                if self.objArray[xCount][yCount] is None:
                    tile = self.tileArray[xCount][yCount]
                else:
                    tile = self.objArray[xCount][yCount]
                img, color, bg = tile.getTile()
                pos = (xCount, yCount)
                newMapList.append((img, 1, color, bg, pos))
                xCount += 1
            newMapList.append((0, 0, 0, 0))
            yCount += 1
        self.setMap(newMapList)
        return self.mapList

    def setObjArray(self, pos, Obj=None):
        """
        puts object in objArray.
        """
        self.objArray[pos[0]][pos[1]] = Obj

    def assignMapTile(self, x, y):
        """
        Replaces createBaseMap.
        Takes given index and returns the appropriate copy of a
        mapTile. Only one of any given kind of tile will exist.
        """
        maxX, maxY = self.getMaxX() - 1, self.getMaxY() - 1
        if x == 0 or x == maxX or y == 0 or y == maxY:
            return self.tiles.getTile(ID="00")  # ID="00" is a basic wall
        elif x in range(1, 4) or y in range(1, 4):
            #make sure player start is clear. This will have to change later
            return self.tiles.getTile(ID="!00")  # not the listed tileID
        elif x in range(4, maxX) and y in range(4, maxY):
            return self.tiles.getTile()
        else:
            print x, y
            raise _ERR.NotInBounds("Given coordinate is not in bounds")

    ##def createBaseMap(self, x, y):
        ##"""
        ##Soon to be deprecated.
        ##Takes given index and returns a BaseGameObj if that index is not
        ##on the outermost edge of the map, or out of range entirely.

        ##x, y - int, int - index to draw
        ##"""
        ##maxX, maxY = self.getMaxX() - 1, self.getMaxY() - 1
        ##if x in range(1, maxX) and y in range(1, maxY):
            ##if random.random() > 0.01:
                ##return BaseGameObj.BaseGameObj(x, y)
            ##else:
                ##return None
        ##elif x == maxX or x == 0 or y == maxY or y == 0:
            ##return None
        ##else:
            ##raise Exception('NotMapLocation')

    def makeMap(self, x, y):
        """
        Returns two (maybe three) versions of the map. The tileArray is
        all of the floor, wall, door, etc. tiles in a map. the objMap is
        all of the players, monsters, npcs, fountains, etc. in a map.

        x, y - int, int - dimensions of array
        """
        tileArray = []
        objArray = []
        for row in range(x):
            tileArray.append([])
            objArray.append([])
            for col in range(y):
                tileArray[row].append(self.assignMapTile(row, col))
                objArray[row].append(None)
        return tileArray, objArray

    def drawMap(self, minInd, maxInd):
        """
        generator that spits out one tile of the map at a time for to
        be blitted. Might be usefull to assign colors here as well?
        """
        newMapList = self.getMap(minInd, maxInd)
        while newMapList != []:
            tile = newMapList.pop(0)
            yield tile

    def testMapPos(self, pos, testLegal=False):
        """
        Tests map pos to see if it exists and is legal to move into.

        pos = tuple containing two ints
        """
        if pos[0] > 0 and pos[0] < self.getMaxX():
            if pos[1] > 0 and pos[1] < self.getMaxY():
                if self.tileArray[pos[0]][pos[1]].getID()[0] != "0":
                    if testLegal and self.objArray[pos[0]][pos[1]] == None:
                        return testLegal
                    else:
                        return False
        raise _ERR.NotValidMapLocation("Not a valid map space.")

    def getMapTile(self, pos):
        """
        Takes tuple representing location in tileArray and returns object

        pos = tuple containing two integers
        """
        try:
            self.testMapPos(pos)
        except _ERR.NotValidMapLocation as err:
            raise err
        else:
            if self.objArray[pos[0]][pos[1]] is None:
                return self.tileArray[pos[0]][pos[1]]
            else:
                return self.objArray[pos[0]][pos[1]]


def main():
    m = ObjectMap(3, 3)
    print m.getMap()

if __name__ == '__main__':
    main()
