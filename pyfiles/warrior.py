#! /usr/bin/python2
#coding=utf-8

"""
Yet to be named dungeonGame
by EncodedPixel
coded by タダノデーモン(tadanodaemon)

This program contains the Warrior class, for the game
"""

from charANPC import Character
from random import *

class Warrior(Character):

    def __init__(self, gui):
        super(Warrior, self).__init__(gui)
        self.special= ['random', self.berserk]
        self.berserk = False
        self.stats = {
                'hp': 25,
                'sp': 10,
                'fullHP': 25,
                'fullSP': 10,
                'atk': 15,
                'def': 15,
                'ma': 5,
                'md': 10,
                'lck': 5,
                'spe': 10,
                'exp': 0,
                'gol': 0,
                'elem': ['none']
                }
        self.atkList = [
                'slash',
                'shield bash',
                'parry',
                'warcry'
                ]
        self.setTarget = [
                'parry',
                'warcry'
                ]
        self.atkDict = {
                'slash': self.regAtk,
                'shield bash': self.shieldBash,
                'parry': self.parry,
                'warcry': self.warcry
                }

    def berserk(self, targetInfo):
        '''
        This is the warriors special ability
        '''
        targetInfo[3] += '\n-->%s just went berserk!' %(self.info['name'])
        self.statModifier({'atk': 1.5, 'def': .5})
        self.berserk = True
        return targetInfo

    def shieldBash(self, target):
        if self.berserk:
            self.statModifier({'atk': 2.0/3, 'def': 2.0})
            self.berserk = False
        baseAtk = 85
        baseAcc = 90
        string = '%s used shield bash on %s' %(self.info['name'], target)
        mod = {'atk': .9}
        modString = '%s\'s attack lowered' %(target)
        magAtk = False
        skipToFront = [0]
        waitForHit = [0]
        waitForNextTurn = [0]
        multHit = [0]
        multTarget = [None]
        targetLoseTurn = [0]
        absorb = [0]
        status = [0]
        element = ['none']
        sp = 3
        return [target, baseAtk, baseAcc, string,  mod, modString, magAtk,
                skipToFront, waitForHit, waitForNextTurn, multHit, multTarget,
                targetLoseTurn, absorb, status, element, sp]
            
    def parry(self):
        if self.berserk:
            self.statModifier({'atk': 2.0/3, 'def': 2.0})
            self.berserk = False
        target = self.info['name']
        baseAtk = 0
        baseAcc = 100
        string = self.info['name'] + ' used parry!'
        mod = {}
        modString = ''
        magAtk = False
        skipToFront = [0]
        waitForHit = [1, 0, 0, '%s parried the attack!' %(self.info['name'])]
        waitForNextTurn = [0]
        multHit = [0]
        multTarget = [None]
        targetLoseTurn = [0]
        absorb = [0]
        status = [0]
        element = ['none']
        sp = 1
        return [target, baseAtk, baseAcc, string,  mod, modString, magAtk,
                skipToFront, waitForHit, waitForNextTurn, multHit, multTarget,
                targetLoseTurn, absorb, status, element, sp]
            
    def warcry(self):
        if self.berserk:
            self.statModifier({'atk': 2.0/3, 'def': 2.0})
            self.berserk = False
        target = self.info['name']
        baseAtk = 0
        baseAcc = 95
        string = self.info['name'] + ' used warcry'
        mod = {'atk': 1.5, 'def': .75}
        modString = '%s\'s attack rose and defense lowered!' %(self.info['name'])
        magAtk = False
        skipToFront = [0]
        waitForHit = [0]
        waitForNextTurn = [0]
        multHit = [0]
        multTarget = [None]
        targetLoseTurn = [0]
        absorb = [0]
        status = [0]
        element = ['none']
        sp = 2
        return [target, baseAtk, baseAcc, string,  mod, modString, magAtk,
                skipToFront, waitForHit, waitForNextTurn, multHit, multTarget,
                targetLoseTurn, absorb, status, element, sp]
