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
import GraphicalTiles


# Mulipliers to convert coords into octants of the circle around an object.
mult = [
        [1, 0, 0, -1, -1, 0, 0, 1],
        [0, 1, -1, 0, 0, -1, 1, 0],
        [0, 1, 1, 0, 0, -1, -1, 0],
        [1, 0, 0, 1, -1, 0, 0, -1]
       ]

# graphics
tileSize = 32
tileImgs = GraphicalTiles.ImgHandler("sos1.0.png", tileSize, tileSize)



# Some colors
black = (0, 0, 0)
white = (200, 200, 200)
grey01 = (150, 150, 150)
grey02 = (140, 140, 140)
grey03 = (130, 130, 130)
grey04 = (110, 110, 110)
grey05 = (100, 100, 100)
blue = (150, 150, 255)
green = (0, 255, 0)
red = (255, 150, 150)

# Color sets
cs_greys = [grey01, grey02, grey03, grey04, grey05]

# Other stuff (NOT IMPLEMENTED)
moods = ["Friendly", "Calm", "Neutral", "Aggressive", "Hostile"]
goodMoods = ["Friendly", "Calm"]
badMoods = ["Aggressive", "Hostile"]