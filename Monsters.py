#--------------------------------------------------------------------------
# Name:        Monsters
# Purpose:     Used by Game object in controlling monster objects.
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
import BaseGameObj as BGO
# import random


class Monsters(object):

    def __init__(self):
        self.monsters = []

    def getMonster(self, listPos=-1):
        """
        Returns monster from self.monsters at pos
        """
        return self.monsters[listPos]

    def addMonster(self, coords):
        """
        Add monsters objects to list.
        """
        self.monsters.append(BGO.Zombie(coords[0], coords[1]))

    def remMonster(self, monster):
        self.monsters.remove(monster)

    def iterMonsters(self):
        """
        Generator for updating all monsters in list.
        """
        for monster in self.monsters:
                yield monster