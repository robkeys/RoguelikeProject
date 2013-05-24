#--------------------------------------------------------------------------
# Name:        TileHandler
# Purpose:     Creates and serves up map tiles.
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
import random
import BaseGameObj
import GraphicalTiles
import _ENV_VAR as ENV

WALL_DIRS = {(1, 0, 0, 0): 2,
             (0, 1, 0, 0): 0,
             (0, 0, 1, 0): 1,
             (0, 0, 0, 1): 0,
             (1, 0, 1, 0): 1,
             (0, 1, 0, 1): 0,
             (1, 1, 0, 0): 5,
             (0, 1, 1, 0): 3,
             (0, 0, 1, 1): 4,
             (1, 0, 0, 1): 6,
             (1, 1, 1, 0): 7,
             (0, 1, 1, 1): 9,
             (1, 0, 1, 1): 8,
             (1, 1, 0, 1): 10,
             (1, 1, 1, 1): 11}


class Tile(BaseGameObj.BaseGameObj):

    def __init__(self, ID, img, color, passable = False):
        super(Tile, self).__init__()
        self.ID = ID
        self.img = img
        self.color = color
        self.passable = passable
        self.tag = "tile"

    def setID(self, ID):
        """
        sets self.ID which refers to the location of the tile in the
        tileHandler's tileDict
        """
        self.ID = ID

    def setPassable(self, passable):
        """
        Sets tile's passability. Passable tiles can be occupied by
        entitites and may contain items.

        passable - bool - True if passable.
        """
        assert type(passable) == bool
        self.passable = passable

    def getID(self):
        """
        Returns self.ID which is a str.
        """
        return self.ID

    def getPassable(self):
        """
        Returns self.passable which is a bool.
        """
        return self.passable


class TileHandler(object):

    def __init__(self):
        self.tileImgs = GraphicalTiles.ImgHandler("sos1.0.png", ENV.tileSize, ENV.tileSize)
        self.tileDict = {}

    def makeTile(self, x1, y1, x2, y2):
        """
        Randomly generates tile instantiation information and returns it.
        Will not create passable tiles on map edge.
        """
        rand = random.random()
        if rand < .1 or x1 == 0 or x1 >= x2 - 1 or y1 == 0 or y1 >= y2 - 1:
            gY = 10                    # Y of graphic
            gX = random.randrange(12)  # X or graphic
            color = (238, 238, 204)
            p = False  # not passable
        else:
            gY = 8                    # Y of graphic
            gX = random.randrange(3)  # X of graphic
            color = (138, 138, 104)
            p = True  # passable
        ID = (gX, gY)
        img = self.tileImgs.getImgObj(gX, gY)
        self.tileDict[ID] = self.tileDict.get(ID, Tile(ID, img, color, p))
        return self.tileDict[ID]

    def getTile(self, ID):
        """
        Finds a previously created tile and returns it.

        tileID - str - the key of the tileDict that relates to the value of
                       the requested tile.
        """
        return self.tileDict[ID]

    def setTileColor(self, ID, color):
        """
        Sets color for tile of givenID. Initially this is for debugging, but
        will probably be useful in the future, yeah?
        """
        tile = self.tileDict[ID]
        tile.setColor(color)

    def ChooseWall(self, n, s, e, w):
        """
        Takes a list of four boolean arguments that represent the presence of
        walls around a central wall tile. The wall object that will most make
        the wall appear seamless is returned.

        n, s, e, w - in - 1 if wall present. 0 otherwise.
        """
        if (n, s, e, w) != (0, 0, 0, 0):
            arrayX = WALL_DIRS[(n, s, e, w)]
            ID = (arrayX, 10)
            img = self.tileImgs.getImgObj(arrayX, 10)
            color = (238, 238, 204)
            p = False
            self.tileDict[ID] = self.tileDict.get(ID, Tile(ID, img, color, p))
            return self.tileDict[ID]
