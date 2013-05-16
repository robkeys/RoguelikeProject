#--------------------------------------------------------------------------
# Name:        GameExceptions
# Purpose:     Exceptions called by game.
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


class NotValidMapLocation(Exception):
    """
    Called when object cannot move into or generally interact with a
    given map location.
    """
    pass


class LocationOccupied(Exception):
    """
    Called when object cannot move into a space because a Game Object is
    already present.
    """
    pass


class NotInBounds(Exception):
    """
    Called when a request for an x, y coord is not within the bounds of
    a map.
    """
    pass


class InvalidGameObject(Exception):
    """
    Called when a given Game Object is not of the type required for the
    operation it was given for.
    """
    pass