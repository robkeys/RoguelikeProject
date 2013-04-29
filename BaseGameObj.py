#--------------------------------------------------------------------------
# Name:     BaseGameObj
# Purpose:  Handles all whatsis realted to characters.
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
import GameExceptions
from math import sqrt as sqrt
import random
import _ENV_VAR as _E


class BaseGameObj(object):

    def __init__(self, x=-1, y=-1):
        self.setPos(x, y)     # The position of this object
        self.char = random.choice(['.', '.', '.', "'", ',', ';', ':'])
        self.color = random.choice([_E.grey01, _E.grey02, _E.grey03,
                                    _E.grey04, _E.grey05])
        self.space = None

    def setPos(self, x, y):
        """
        Sets x, y position of Character. Returns tuple with (x, y) position
        of Character object. Assumes position exists on map/screen.

        x, y = int
        """
        self.pos = (x, y)

    def getPos(self):
        """
        Returns tuple containing x, y position
        """
        return self.pos

    def updatePos(self, changeInX, changeInY):
        """
        Sets a new tuple containing an update to self.pos. Assumes
        position exists on map/screen.

        changeInX, changeInY = Positive or Negative Integer.
        """
        self.pos = (self.pos[0] + changeInX, self.pos[1] + changeInY)

    def getChar(self):
        """
        Returns four variables to be passed to a font object.
        """
        if self.space is None:
            char = self.char
            newChar = (char, 1, self.color, _E.black)
            # print str(newChar)
            return newChar
        else:
            return self.space.getChar()

    def testSpace(self):
        """
        Returns True if empty
        """
        if self.space is None:
            return True
        else:
            return False

    def fillSpace(self, gameObject):
        """
        Takes an object into itself. If the object is already full it throws
        an error
        """
        if self.space is None:
            self.space = gameObject
        else:
            print "SpaceOccupied"

    def emptySpace(self):
        """
        Sets self.space to None
        """
        self.space = None


class Player(BaseGameObj):

    def __init__(self, x, y):
        super(Player, self).__init__(x, y)
        self.char = '@'
        self.color = _E.blue

    def getChar(self):
        """
        returns tuple representing pygames font render args
        """
        return (self.char, 1, self.color, _E.black)

class Zombie(Player):

    def __init__(self, x, y):
        super(Player, self).__init__(x, y)
        self.char = 'Z'
        self.color = _E.red
        self.alive = True
        self.sightRange = 10

    def getAlive(self):
        """
        Returns life status.
        """
        return self.alive

    def kill(self):
        """
        Makes monster dead.
        """
        self.alive = False

    def detectPlayer(self, x1, y1, x2, y2):
        """
        If player is detected zombie moves toward it.
        """
        if sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) < self.sightRange:
            return True
        else:
            return False

    def move(self, playerPos):
        x1, y1 = self.pos[0], self.pos[1]
        x2, y2 = playerPos[0], playerPos[1]
        if self.detectPlayer(x1, y1, x2, y2):
            x, y = 0, 0
            if x1 > x2:  #player x smaller
                x += -1
            elif x1 < x2:  # player x bigger
                x += 1
            if y1 > y2:  # player y smaller
                y += -1
            elif y1 < y2:  # player y bigger
                y += 1
            return (x, y)
        elif random.random() > 0.7:
            return (random.choice([-1, 0, 1]), random.choice([-1, 0, 1]))
        else:
            return self.pos

    def kickDoor(self):
        pass  # to do




def main():
    pass

if __name__ == '__main__':
    main()
