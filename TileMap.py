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
        for Y in range(self.maxY):
            self.array.append([])
            for X in range(self.maxX):
                newTile = self.tiles.makeTile(X, Y, self.maxX, self.maxY)
                # newTile.setColor(random.choice(ENV.cs_greys))
                self.array[Y].append(newTile)
        self.reflowWalls()

    def testMapPos(self, x, y):
        """
        Returns True if given coordinates point to a tile that can be
        occupied by entities or items.

        x, y - int - x, y coordinates of a tile to test.
        """

        return self.array[y][x].getPassable()

    def testSurroundingWalls(self, x, y):
        """
        Starts at the array pos of a tile that is not passable, and then
        tests and returns the passability of each of the surrounding walls
        in the four cardinal directions.

        x, y - int - Array position of the tile to test

        returns:
        dir[0], dir[1], dir[2], dir[3] - int - 1 if corresponding tile is not
                                               passable. Otherwise 0.
        """
        dirs = []
        for i in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            X, Y = x + i[0], y + i[1]
            try:
                passable = self.array[Y][X].getPassable()
            except IndexError:
                dirs.append(0)
            else:
                if X < 0 or X > self.maxX - 1 or Y < 0 or Y > self.maxY:
                    dirs.append(0)
                elif not passable:
                    dirs.append(1)
                else:
                    dirs.append(0)
        return dirs[0], dirs[1], dirs[2], dirs[3]

    def reflowWalls(self):
        """
        Iterates over walls then tests passability of surrounding walls. Once
        established it calls TileHandler to determine appropriate Tile obj.
        """
        for y, col in enumerate(self.array):
            for x, tile in enumerate(col):
                if not tile.getPassable() and tile is not None:
                    n, s, e, w = self.testSurroundingWalls(x, y)
                    if (n, s, e, w) == (0, 0, 0, 0):
                        pass
                    else:
                        newImg = self.tiles.ChooseWall(n, s, e, w)
                        self.array[y][x] = newImg