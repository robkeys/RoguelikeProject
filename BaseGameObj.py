#--------------------------------------------------------------------------
# Name:        BaseGameObj
# Purpose:     Handles all whatsis related to tileacters, monsters,
#              NPCs, etc.
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
from math import sqrt as sqrt
import random
import _ENV_VAR as _E


class BaseGameObj(object):  # Referred to as BaGaOb in docs & comments

    def __init__(self, *args, **kwargs):
        self.img = ""
        self.color = ()
        self.bg = ()
        self.tag = None

    def getTag(self):
        """
        Returns tag of BaGaOb.
        """
        return self.tag

    def setImg(self, img):
        """
        Sets self.img which is the character that the map displays when
        this BaGaOb is drawn

        img - str - Currently the image is a string.
        """
        self.img = img

    def setColor(self, color):
        """
        Sets self.color to the (r, g, b) value of the color to display when
        this BaGaOb is drawn.

        color - tuple - Tuple of three ints that range from 0 - 255
        """
        self.color = color

    def setBG(self, bg):
        """
        Sets self.color to the (r, g, b) value of the color to display in
        the background when this BaGaOb is drawn.

        bg - tuple - Tuple of three ints that range from 0 - 255
        """
        self.bg = bg

    def setTag(self, tag):
        """
        Sets self.tag to the specified string. The name should change?
        """
        self.tag = tag

    def display(self):
        """
        Returns a img, color, and bg of the BaGaOb.

        img - str - Currently the character that represents the BaGaOb.
        color - tuple - The (red, green, blue) value of the BaGaOb
        bg - tuple - The (red, green, blue) value of the BaGaOb
        """
        return self.img, self.color, self.bg


class Entity(BaseGameObj):  # THIS IS PROBABLY BROKEN - LOTS OF CHANGES

    def __init__(self, x, y):
        super(Entity, self).__init__(x, y)
        self.x, self.y = x, y
        self.tag = "entity"

    def setPos(self, x, y):
        """
        Sets x, y position of tileacter. Returns tuple with (x, y) position
        of tileacter object. Assumes position exists on map/screen.

        x, y = int
        """
        self.x, self.y = x, y

    def getPos(self):
        """
        Returns tuple containing x, y position
        """
        return self.x, self.y

    def updatePos(self, x, y):
        """
        Adds x, y to self.x, self.y
        """
        self.x = self.x + x
        self.y = self.y + y


class Player(Entity):  # THIS IS PROBABLY BROKEN - LOTS OF CHANGES

    def __init__(self, x, y):
        super(Player, self).__init__(x, y)
        self.img = '@'
        self.color = _E.blue
        self.bg = _E.black
        self.types = ["pc"]  # dont call these types
        self.hitPoints = 10
        self.alive = True
        self.sightRange = 12
        self.facing = (0, 1)  # represents the tile directly in front.
        self.baseDef = 0
        self.baseDodge = 0
        self.baseArmor = 0
        self.baseAtt = 0
        self.baseReact = 0
        self.baseDmg = 5
        self.baseDmgTypes = ["physical", "melee", "unarmed", "bludgeon",
                             "bone", "fist", "punch"]

    def getTypes(self):
        """
        Returns types list.
        """
        return self.types

    def isAlive(self):
        return self.alive

    def isAggressive(self, subjTypes):  # Maybe charm effects can go here.
        """
        Recieves the subjects types and returns True if Hostile to the
        subject, false otherwise.
        """
        for aType in subjTypes:
            if aType not in self.types:
                return True
        return False

    def getSight(self):
        return self.sightRange

    def getDef(self):
        """
        returns a number to be added to an attack roll. represents a
        characters parrying, feinting, shield use, magical auras and
        fields, etc.
        """
        return self.baseDef

    def getReact(self):
        """
        Returns base react score of character.
        """
        return self.baseReact

    def getDamage(self, baseDef):
        """
        Takes a baseDef score and returns damage.

        baseDef - int - A number to be added to the attack result

        Returns:
        dmg - int - Total possible damage of the attack
        type - list of strings - damage types that may modify the damage
        """
        # Currently attack roll is: 0 - 99
        #                           + Base Defense of subject
        #                           - Base Attack of subject
        attRoll = int(random.random() * 100) + baseDef - self.baseAtt
        # print self, "attack roll:", attRoll
        # Currently there is a base 1:20 chance of hitting a target
        if attRoll < 20:
            if attRoll == 0:
                # crit! double damage and crit type added
                dmg = self.baseDmg * 2
                types = self.baseDmgTypes[:]
                types.append("critical")
            else:
                dmg = self.baseDmg
                types = self.baseDmgTypes
            return dmg, types
        else:
            raise Exception("Missed!")

    def kill(self):
        """
        Kills character. For player this ends game.
        """
        self.alive = False
        raise Exception("Game Over.")

    def dodge(self, dmg, reactAdj=0):
        """
        Determines if character successfully dodges a source of damage

        dmg - Damage.Damage Object - The damage source
        reactionAdj - int - Number representing attackers ability to correct
                            its attack if it can react quickly.

        Returns:
        mod - int - amount of damage reduction due to dodging.
        """
        mod = 0
        # Currently dodge roll is: 0 - 99
        #                          + Base reaction score of attacker
        dodgeRoll = int(random.random() * 100) + reactAdj - self.baseDodge
        if dodgeRoll < 5:
            if dodgeRoll == 0:
                mod = dmg.getDMG()
            else:
                reduceBy = dodgeRoll * 0.20
                mod = dmg.getDMG() - int(dmg.getDMG() * reduceBy)
        return mod

    def armor(self, dmg):
        """
        Determines if character's armor protects it from a source of damage
        and to what degree it reduces the damage if any.

        dmg - Damage.Damage Object - the damage source

        returns:
        mod - int - amount of damage reduction due to armor.
        """
        # currently armor reduces damage 5% per point of armor
        mod = 0
        if self.baseArmor > 0:
            reduceBy = self.baseArmor * .5
            mod = dmg.getDMG() - int(dmg.getDMG() * reduceBy)
        return mod

    def applyDmg(self, dmg):
        """
        subtracts/adds dmg. Ultimately this will also look at damage types
        and adjust totals accordingly.

        dmg - Damage.Damage Object - the damage source
        """
        self.hitPoints -= dmg.getDMG()
        print self, "left:", self.hitPoints
        print "alive:", self.alive
        if self.hitPoints < 1:
            self.kill()
            print "dead! self.alive:", self.alive

    def __str__(self):
        return "You"


class Zombie(Player):  # THIS IS PROBABLY BROKEN - LOTS OF CHANGES

    def __init__(self, x, y):
        super(Zombie, self).__init__(x, y)
        self.img = 'Z'
        self.color = _E.red
        self.alive = True
        self.sightRange = 10
        self.types = ["monster", "hostile", "undead", "hungry", "evil"]
        self.hitPoints = 5
        self.baseDmg = 1

    def kill(self):
        """
        Makes monster dead.
        """
        self.alive = False

    def detectPlayer(self, x1, y1, x2, y2):
        """
        If player is detected zombie moves toward it.
        """
        if sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) < self.sightRange:
            return True
        else:
            return False

    def move(self, x2, y2):
        x1, y1 = self.x, self.y
        x, y = 0, 0
        if self.detectPlayer(x1, y1, x2, y2):
            if x1 > x2:    # player x smaller
                x += -1
            elif x1 < x2:  # player x bigger
                x += 1
            if y1 > y2:    # player y smaller
                y += -1
            elif y1 < y2:  # player y bigger
                y += 1
            return (x, y)
        elif random.random() > 0.7:
            return random.choice([(-1, 0), (1, 0), (-1, 1), (-1, -1),
                                   (1, -1), (1, 1), (0, -1), (0, 1)])
        else:
            return (x, y)

    def kickDoor(self):
        pass  # to do

    def __str__(self):
        return "Zombie"


def main():
    pass

if __name__ == '__main__':
    main()
