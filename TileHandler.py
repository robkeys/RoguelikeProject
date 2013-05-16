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
import _ENV_VAR as _E


class Tile(BaseGameObj.BaseGameObj):

    def __init__(self, ID, img, color, passable):
        super(Tile, self).__init__()
        self.ID = ID
        self.img = img
        self.color = color
        self.bg = _E.black
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
        self.tileDict = {}
        self.tileImgs = ["#", ".", ",", ";", "'"]
        self.tileInfo = {self.tileImgs[0]: [_E.white],
                         self.tileImgs[1]: _E.cs_greys,
                         self.tileImgs[2]: _E.cs_greys,
                         self.tileImgs[3]: _E.cs_greys,
                         self.tileImgs[4]: _E.cs_greys}

    def makeTile(self, x1, y1, x2, y2):
        """
        Randomly generates tile instantiation information and returns it.
        Will not create passable tiles on map edge.
        """
        rand = random.random()
        if rand < .1 or x1 == 0 or x1 == x2 or y1 == 0 or y1 == y2:
            imgInd = 0
            passable = False
        else:
            imgInd = random.choice(xrange(1, len(self.tileImgs)))
            passable = True
        img = self.tileImgs[imgInd]
        colorInd = random.choice(xrange(len(self.tileInfo[img])))
        color = self.tileInfo[img][colorInd]
        ID = str(imgInd) + str(colorInd)
        self.tileDict[ID] = self.tileDict.get(ID,
                                         Tile(ID, img, color, passable))
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