#--------------------------------------------------------------------------
# Name:        _ENV_VAR
# Purpose:     Environment variables
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

# Mulipliers to convert coords into octants of the circle around an object.
mult = [
        [1, 0, 0, -1, -1, 0, 0, 1],
        [0, 1, -1, 0, 0, -1, 1, 0],
        [0, 1, 1, 0, 0, -1, -1, 0],
        [1, 0, 0, 1, -1, 0, 0, -1]
       ]


# Define some colors
black = (0, 0, 0)
white = (255, 255, 255)
grey01 = (150, 150, 150)
grey02 = (140, 140, 140)
grey03 = (130, 130, 130)
grey04 = (110, 110, 110)
grey05 = (100, 100, 100)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)

moods = ["Friendly", "Calm", "Neutral", "Aggressive", "Hostile"]
goodMoods = ["Friendly", "Calm"]
badMoods = ["Aggressive", "Hostile"]