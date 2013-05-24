#--------------------------------------------------------------------------
# Name:         GameLoop
# Purpose:     Contains main program loop, and handles game timing and
#              inputs
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
import random
import pygame




def flicker(lastVal, lastDir):
    if lastVal > 25 and lastDir == 1:
        newDir = -1
        newVal = -5 * random.random() + lastVal
    elif lastVal < 5 and lastDir == -1:
        newDir = 1
        newVal = 5 * random.random() + lastVal
    else:
        newDir = random.choice((lastDir, -1, 1))
        newVal = newDir * (5 * random.random() + lastVal)
    return newVal, newDir



#Loop until the user clicks the close button.
def main():
    pygame.init()
    wSize = [704, 512]
    screen = pygame.display.set_mode(wSize, pygame.RESIZABLE)
    import Game
    game = Game.Game(screen, wSize)
    game.p_PlayerStartPos()
    game.o_GenMonsters()
    flickVal = 15
    flickDir = 1
    done = False
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
                if event.key == pygame.K_UP or event.key == pygame.K_KP8:
                    game.p_MovePlayer(0, -1)
                if event.key == pygame.K_DOWN or event.key == pygame.K_KP2:
                    game.p_MovePlayer(0, 1)
                if event.key == pygame.K_LEFT or event.key == pygame.K_KP4:
                    game.p_MovePlayer(-1, 0)
                if event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                    game.p_MovePlayer(1, 0)
                if event.key == pygame.K_KP7:
                    game.p_MovePlayer(-1, -1)
                if event.key == pygame.K_KP9:
                    game.p_MovePlayer(1, -1)
                if event.key == pygame.K_KP1:
                    game.p_MovePlayer(-1, 1)
                if event.key == pygame.K_KP3:
                    game.p_MovePlayer(1, 1)
                if event.key == pygame.K_PERIOD or event.key == pygame.K_KP5:
                    game.p_MovePlayer(0, 0)

                game.o_MoveMonsters()

            # elif event.type == pygame.KEYUP:
                # game.o_UpdateObj(game.getPlayer(), 0, 0)
        flickVal, flickDir = flicker(flickVal, flickDir)
        game.newFrame(flickVal)

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()

if __name__ == '__main__':
    main()
