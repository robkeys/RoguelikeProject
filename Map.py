#--------------------------------------------------------------------------
# Name:         Map
# Purpose:      Base class for game map objects.
#
# Author:       Rob Keys
#
# Created:      05/13/2013
# Copyright:    (c) 2013, Rob Keys
# Licence:      This software is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with the software; If not, see <http://www.gnu.org/licenses/>.
#--------------------------------------------------------------------------


class Map(object):

    def __init__(self, maxX, maxY):
        self.maxX, self.maxY = maxX, maxY
        self.array = []
        self.makeMap()

    def makeMap(self):
        """
        Creates a 2d array based on the self.maxX and self.maxY dimensions.
        It fills the array with None objects.
        """
        Y = 0
        for Y in range(self.maxY):
            self.array.append([])
            for X in range(self.maxX):
                self.array[Y].append(None)

    def getMax(self):
        """
        Returns self.maxX and self.maxY
        """
        return self.maxX, self.maxY

    def getArray(self):
        """
        Returns self.array
        """
        return self.array

    def setPos(self, x, y, data):
        """
        Places the declared data into self.array at the specified coords.

        x, y - int - The x, y coords of a point in the array.
        data - any - The data to be placed in the array.
        """
        self.array[y][x] = data

    def getPos(self, x, y):
        """
        Returns data stored in self.array at given coords.

        x, y - int - The x, y coords of a point in the array.
        """
        return self.array[y][x]

    def testMapPos(self, x, y):
        """
        Returns True if the given coords are in self.array

        x, y - int - The x, y coords of the point to test in the array.
        """
        try:
            testVar = self.array[y][x]
        except IndexError:
            return False
        else:
            del(testVar)
            return True

    def iterMap(self, x1, y1, x2, y2):
        """
        Generator that yields data from self.array in order from x1, y1 to
        x2, y2.

        x1, y1 - int - starting coords of data to be fetched.
        x2, y2 - int - ending coords of data to be fetched.
        """
        Y = y1
        while Y >= y2:
            X = x1
            while X >= x2:
                yield self.array[Y][X]
                X += 1
            Y += 1
