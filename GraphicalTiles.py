#--------------------------------------------------------------------------
# Name:        GraphicalTiles
# Purpose:     Creates tiles from images & handles instances of images
#
# Author:      Rob Keys
#
# Created:     05/18/2013
# Copyright:   (c) 2013, Rob Keys
# Licence:     This software is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with the software; If not, see <http://www.gnu.org/licenses/>.
#--------------------------------------------------------------------------
import pygame
import pygame.locals
import random


class Img(object):

    def __init__(self, img):
        self.img = img

    def getImg(self):
        """
        Returns self.img
        """
        return self.img

    def _shad(self, color):
        """
        Takes an RGB tuple and returns a new tuple of the that color's shadow.
        """
        R, G, B = color[0] / 2, color[1] / 2, color[2] / 2
        return (R, G, B)

    def recolor(self, newColor):
        """
        Using pygame PixelArray it returns a copy of the image with all pixels
        of exactly oldColor replaced with pixels of newColor.
        """
        pxArray = pygame.PixelArray(self.img.copy())
        oldColor = (238, 238, 204)
        pxArray.replace(oldColor, newColor)
        oldShadow = (138, 138, 104)
        newShadow = self._shad(newColor)
        pxArray.replace(oldShadow, newShadow)
        return pxArray.make_surface()


class ImgHandler(object):

    def __init__(self, tileSetFileName, tileX, tileY):
        self.tileSet = pygame.image.load(tileSetFileName).convert()
        self.tileX, self.tileY = tileX, tileY
        self.imgX, self.imgY = self.tileSet.get_size()
        self.imgs = []
        for y in range(self.imgY / self.tileY):
            self.imgs.append([])
            for x in range(self.imgX / self.tileX):
                rect = (x * self.tileX, y * self.tileY, self.tileX, self.tileY)
                newSurf = self.tileSet.subsurface(rect)
                self.imgs[y].append(Img(newSurf))

    def getImgObj(self, x, y):
        """
        Returns Img object at given pos
        """
        return self.imgs[y][x]

    def getImg(self, x, y):
        """
        Returns img from self.imgs
        """
        return self.imgs[y][x].getImg()

    def iterImgs(self):
        """
        Yields all Imgs in self.imgs
        """
        for y, col in enumerate(self.imgs):
            for x, img in enumerate(col):
                yield img, x, y


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((368, 368))
    screen.fill((0, 0, 0))
    imgs = ImgHandler("sos1.0.png", 16, 16)
    rRange = random.randrange
    x, y = 0, 0
    for img, i, j in imgs.iterImgs():
        if x >= 368:
            x = 0
            y += 16
        r, g, b = rRange(255), rRange(255), rRange(255)
        img.recolor((r, g, b))
        screen.blit(img.getImg(), (x, y))
        x += 16
    pygame.display.flip()
    while pygame.event.wait().type != pygame.locals.QUIT:
        pass