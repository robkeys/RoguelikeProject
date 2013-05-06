#--------------------------------------------------------------------------
# Name:        Damage
# Purpose:     Handles types, amounts & calculations relating to damage
#              that can be done to characters.
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

class Damage(object):

    def __init__(self, initialDamage=0, initialTypes=[]):
        self.dmgScore = initialDamage
        self.type = initialTypes  # don't call these types

    def getDMG(self, modList=[]):
        """
        Returns self with modifiers applied when declared.
        """
        for mod in modList:
            self.dmgScore -= mod
        return self.dmgScore