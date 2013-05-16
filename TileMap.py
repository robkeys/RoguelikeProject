#--------------------------------------------------------------------------
# Name:         TileMap
# Purpose:      Child class of Map superclass. Contains copies of
#               Tile objects that are served up by the TileHandler.
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
import Map
import TileHandler


class TileMap(Map.Map):

    def __init__(self, maxX, maxY):
        self.tiles = TileHandler.TileHandler()
        super(TileMap, self).__init__(maxX, maxY)

    def makeMap(self):
        """
        Creates a 2d array based on the self.maxX and self.maxY dimensions.
        It fills the array with None objects.
        """
        Y = 0
        for Y in range(self.maxY + 1):
            self.array.append([])
            for X in range(self.maxX + 1):
                tile = self.tiles.makeTile(X, Y, self.maxX - 1, self.maxY - 1)
                self.array[Y].append(tile)

    def testMapPos(self, x, y):
        """
        Returns True if given coordinates point to a tile that can be
        occupied by entities or items.

        x, y - int - x, y coordinates of a tile to test.
        """
        return self.array[y][x].getPassable()