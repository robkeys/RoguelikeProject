# -*- coding: utf-8 -*-


class Map(object):

    def __init__(self, width, height):
        self.width, self.height = width, height
        self.mapStr = ""

    def getMap(self):
        """
        Returns map as str
        """
        return self.mapStr

    def getMaxX(self):
        """
        Returns int representing the extent of the Map's x coords
        """
        return self.width

    def getMaxY(self):
        """
        Returns int representing the extent of the Map's y coords
        """
        return self.height

    def makeMap(self, x, y):
        """
        Base class just generates a plain map. Map is returned in a list of
        lines of a string.
        """
        mapStr = ""
        for x in range(x):
            for y in range(y):
                if x == 0 or y == 0 or x == self.height - 1 \
                   or y == self.width - 1:
                    mapStr += "#"
                else:
                    mapStr += "."
                if y == self.width - 1:
                    mapStr += "/n"
        self.mapStr = mapStr

    def drawMap(self):
        """
        Generator that spits out lines for to blit them
        """
        newMapStr = self.getMap()
        mapList = newMapStr.split('/n')
        while mapList != []:
            yield mapList.pop()
