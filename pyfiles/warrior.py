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
        self.special= ['random', self.berserk, 'Berserk']
        self.berserk = False
        self.stats = {
                'hp': 1,
                'sp': 1,
                'fullHP': 1,
                'fullSP': 1,
                'atk': 1,
                'def': 1,
                'ma': 1,
                'md': 1,
                'lck': 1,
                'spe': 1,
                'exp': 0,
                'gol': 0,
                'elem': ['none']
                }
	self.upStats = {
                'fullHP': [1, -.47, 96.9, -70],
                'fullSP': [1, -.05, 8.9, 6],
                'atk': [1, -.009, 2.2, 14.5],
                'def': [1, -.009, 2.3, 14],
                'ma': [1, -.009, 2, 5],
                'md': [1, -.009, 2, 6.3],
                'lck': [1, -.007, 1.35, 6],
                'spe': [1, -.007, 1.34, 6],
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
        super(Warrior, self).__init__(gui)

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
