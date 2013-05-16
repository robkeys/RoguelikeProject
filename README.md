About:
This is early days. I'm learning how to code, and I love roguelikes. So as a result here's this. I'm starting from scratch, I'm writing it in Python 2.7, and _trying_ not looking to any other code for solutions.

Objective:
Kill all 10 zombies before they kill you!

Controls:
7 8 9 -
 \|/   | Use the keypad to move in the eight directions. 5 to wait a turn.
4-5-6  | To attack press in the direction of the Zombie you want to attack.
 /|\   | You may also use the direction keys to move and '.' to wait a turn.
1 2 3 -
Esc - Quit

To install:
No such thing. You'll need Python and Pygame. To run navigate to wherever you extract this file and type python GameLoop.py. There's not much at this point.

Update History:
05/16/2013
In this update I completely rewrote the map system to accommodate future plans. It now references copies of tiles rather than having an instance of a tile for every map space. There is a map handler class which maintains and handles calls to the various 2d array locations that make up the map. It caches pygame draw information in a separate map subclass to limit calls to objects. This improved performance dramatically. I also added lighting "effects." 

Bug Fixes:
Player is now drawn on first frame and placed safely so as to not crash the game.