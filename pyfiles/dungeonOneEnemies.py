#! /usr/bin/python2
#coding=utf-8

"""
Yet to be named dungeonGame
by EncodedPixel
coded by タダノデーモン(tadanodaemon)

This program contains the three basic enemies for the game
"""

from charANPC import *
from Rogue import Rogue
from Mage import Mage
from Warrior import Warrior

class enemyOne(Rogue, ANPC):

    def __init__(self):
        Rogue.__init__(self)

    def someAttack(self):
        pass
    
class enemyTwo(Mage, ANPC):

    def __init__(self):
        Mage.__init__(self)

    def someAttack(self):
        pass
    
class enemyThree(Warrior, ANPC):

    def __init__(self):
        Warrior.__init__(self)

    def someAttack(self):
        pass
