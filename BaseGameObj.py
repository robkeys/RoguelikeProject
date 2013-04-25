#--------------------------------------------------------------------------
# Name:     BaseGameObj
# Purpose:  Handles all whatsis realted to characters.
#
# Author:      robk
#
# Created:     05/04/2013
# Copyright:   (c) robk 2013
# Licence:     <your licence>
#--------------------------------------------------------------------------
import GameExceptions


class BaseGameObj(object):

    def __init__(self, x=-1, y=-1):
        self.setPos(x, y)     # The position of this object
        self.char = '.'      # The character that represents this object.
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
        Returns a single character string.
        """
        if self.space is None:
            return self.char
        else:
            return self.space.getChar()

    def fillSpace(self, gameObject):
        """
        Takes an object into itself. If the object is already full it throws
        an error
        """
        if self.space is None:
            self.space = gameObject
        else:
            raise Exception("SpaceOccupied")

    def emptySpace(self):
        """
        Sets self.space to None
        """
        self.space = None


class Player(BaseGameObj):

    def __init__(self, x, y):
        super(Player, self).__init__(x, y)
        self.char = '@'


def main():
    pass

if __name__ == '__main__':
    main()
