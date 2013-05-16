#--------------------------------------------------------------------------
# Name:         EntityMap
# Purpose:      Child class of Map superclass. Contains Entity Objects.
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


class EntityMap(Map.Map):

    def __init__(self, maxX, maxY):
        super(EntityMap, self).__init__(maxX, maxY)

    def testMapPos(self, x, y):
        """
        Returns true if given coords are not already occupied by entity.
        """
        try:
            if self.array[y][x] is None:
                return True
            else:
                return False
        except IndexError:
            return False