#! /usr/bin/python2
#coding=utf-8

"""
Yet to be named dungeonGame
by EncodedPixel
coded by タダノデーモン(tadanodaemon)

This program contains the three basic enemies for the game
"""

from charANPC import *

class enemyOne(ANPC):

    def __init__(self, gui):
        super(enemyOne, self).__init__(gui)
        self.aliance = 'enemy'
        self.info = {'name': 'bat'}
        self.inventory = ['potion']

    def someAttack(self):
        pass
    
class enemyTwo(ANPC):

    def __init__(self, gui):
        super(enemyTwo, self).__init__(gui)
        self.aliance = 'enemy'
        self.info = {'name': 'rat'}
        self.inventory = ['potion']

    def someAttack(self):
        pass
    
class enemyThree(ANPC):

    def __init__(self, gui):
        super(enemyThree, self).__init__(gui)
        self.aliance = 'enemy'
        self.info = {'name': 'goblin'}
        self.inventory = ['potion']

    def someAttack(self):
        pass
