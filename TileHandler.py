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


class Tile(object):

    def __init__(self, ID='', img='', color=()):
        self.ID = ID
        self.img = img
        self.color = color
        self.bg = _E.black

    def setID(self, ID):
        """
        sets self.ID which refers to the location of the tile in the
        tileHandler's tileDict
        """
        self.ID = ID

    def setImg(self, img):
        """
        Sets self.img which is the character that the map displays when this
        tile is referenced.
        """
        self.img = img

    def setColor(self, color):
        """
        Sets self.color to the (r, g, b) value of the color to display when
        this tile is drawn.
        """
        self.color = color

    def getID(self):
        """
        Returns self.ID.
        """
        return self.ID

    def getTile(self):
        """
        Returns a img, color, and bg of the tile.
        """
        return self.img, self.color, self.bg


class TileHandler(object):

    def __init__(self):
        self.tileDict = {}
        self.tileImgs = ["#", ".", ",", ";", "'"]
        self.tileInfo = {self.tileImgs[0]: [_E.white],
                           self.tileImgs[1]: _E.cs_greys,
                           self.tileImgs[2]: _E.cs_greys,
                           self.tileImgs[3]: _E.cs_greys,
                           self.tileImgs[4]: _E.cs_greys}

    def genTile(self, openSpace=False):
        """
        Randomly generates tile instantiation information and returns it.
        """
        if random.random() > .1 or openSpace:
            imgInd = random.choice(xrange(1, len(self.tileImgs)))
        else:
            imgInd = 0
        img = self.tileImgs[imgInd]
        colorInd = random.choice(xrange(len(self.tileInfo[img])))
        color = self.tileInfo[img][colorInd]
        ID = str(imgInd) + str(colorInd)
        return ID, img, color

    def getTile(self, ID=""):
        """
        Creates or finds a previously created tile and returns it. The tileID
        relating to the tileDict can be declared, and is used to
        create wall tiles on the border of a map.

        tileID - str - the key of the tileDict that relates to the value of
                       the requested tile.
        """
        if not ID:
            # we must be making a new tile. Generate it.
            ID, img, color = self.genTile()
        elif ID[0] == "!":
            # we are making a new tile and cannot be a wall.
            ID, img, color = self.genTile(openSpace=True)
        else:
            img = self.tileImgs[int(ID[0])]
            color = self.tileInfo[img][int(ID[1])]
        # Currently tilesIDs are 2 digits. This limits us to 10 images & 10
        # colors of those images. This will need to be revisited.
        #
        # For safety's sake we reassign the value for the key in the
        # tileDict with its value again to take advantage of the get funct.
        self.tileDict[ID] = self.tileDict.get(ID, Tile(ID, img, color))
        return self.tileDict[ID]

    def setTileColor(self, ID, color):
        """
        Sets color for tile of givenID. Initially this is for debugging, but
        will probably be useful in the future, yeah?
        """
        tile = self.tileDict[ID]
        tile.setColor(color)