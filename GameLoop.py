#--------------------------------------------------------------------------
# Name:         GameLoop
# Purpose:      Controls aspects of running game
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
import pygame
import Game


#Loop until the user clicks the close button.
def main():
    done = False
    game = Game.Game()
    game.o_UpdateObj(game.getPlayer(), 0, 0)
    game.o_GenMonsters(10)
    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:
                done = True  # Flag that we are done so we exit this loop
            elif event.type == pygame.VIDEORESIZE:
                game.setDisplay(event.dict['size'], pygame.RESIZABLE)
            elif hasattr(event, 'key') and hasattr(event, 'unicode'):
                if event.key == pygame.K_ESCAPE:
                    done = True
                if event.key == pygame.K_UP:
                    game.o_UpdateObj(game.getPlayer(), 0, -1)
                if event.key == pygame.K_DOWN:
                    game.o_UpdateObj(game.getPlayer(), 0, 1)
                if event.key == pygame.K_LEFT:
                    game.o_UpdateObj(game.getPlayer(), -1, 0)
                if event.key == pygame.K_RIGHT:
                    game.o_UpdateObj(game.getPlayer(), 1, 0)

            # elif event.type == pygame.KEYUP:
                # game.o_UpdateObj(game.getPlayer(), 0, 0)
            game.o_MoveMonsters()
            game.newFrame()

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()

if __name__ == '__main__':
    main()
