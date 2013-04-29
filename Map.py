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
import BaseGameObj
import GameExceptions
import random
import _ENV_VAR as _E


class ObjectMap(object):

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.mapList = ""
        self.mapArray = self.makeMap(x, y)

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

    def getMapArray(self):
        """
        Returns 2d array containing map elements
        """
        return self.mapArray

    def getMap(self, minInd, maxInd):
        """
        Uses map array to return map as a str

        minInd, maxInd - tuple, tuple - the two corners of the map to draw
        """
        newMapList = []
        yCount = minInd[1]
        while yCount < maxInd[1]:
            xCount = minInd[0]
            while xCount < maxInd[0]:
                space = self.mapArray[xCount][yCount]
                if space is None:
                    newMapList.append(('#', 1, _E.white, _E.black))
                else:
                    newMapList.append(space.getChar())
                xCount += 1
            newMapList.append((0, 0, 0, 0))
            yCount += 1
        self.setMap(newMapList)
        return self.mapList

    def createBaseMap(self, x, y):
        """
        Takes given index and returns a BaseGameObj if that index is not
        on the outermost edge of the map, or out of range entirely

        x, y - int, int - index to draw
        """
        maxX, maxY = self.getMaxX() - 1, self.getMaxY() - 1
        if x in range(1, maxX) and y in range(1, maxY):
            if random.random() > 0.01:
                return BaseGameObj.BaseGameObj(x, y)
            else:
                return None
        elif x == maxX or x == 0 or y == maxY or y == 0:
            return None
        else:
            raise Exception('NotMapLocation')

    def makeMap(self, x, y):
        """
        Generates a simple map. Map is a 2d array of BaseGameObj to
        represent empty space. Empty array elements represent spaces
        that cannot be occupied by GameObj until explicity set.

        x, y - int, int - dimensions of array
        """
        mapArray = []
        for row in range(x):
            mapArray.append([])
            for col in range(y):
                mapArray[row].append(self.createBaseMap(row, col))
        return mapArray

    def drawMap(self, minInd, maxInd):
        """
        generator that spits out one character of the map at a time for to
        be blitted. Might be usefull to assign colors here as well?
        """
        newMapList = self.getMap(minInd, maxInd)
        while newMapList != []:
            char = newMapList.pop(0)
            yield char

    def testMapPos(self, pos):
        """
        Tests map pos to see if it exists

        pos = tuple containing two ints
        """
        if pos[0] > 0 and pos[0] < self.getMaxX():
            if pos[1] > 0 and pos[1] < self.getMaxY():
                if self.getMapArray()[pos[0]][pos[1]] is not None:
                    return True
        raise GameExceptions.NotValidMapLocation("Not a valid map space.")

    def getMapObject(self, pos):
        """
        Takes tuple representing location in mapArray and returns object

        pos = tuple containing two integers
        """
        try:
            self.testMapPos(pos)
        except GameExceptions.NotValidMapLocation as err:
            raise err
        else:
            return self.getMapArray()[pos[0]][pos[1]]


def main():
    m = ObjectMap(3, 3)
    print m.getMap()

if __name__ == '__main__':
    main()
