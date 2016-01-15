#! /usr/bin/python2
#coding=utf-8

"""
Yet to be named dungeonGame
by EncodedPixel
coded by タダノデーモン(tadanodaemon)

This program conatins the Mage class
"""

from charANPC import Character
from random import *

class Mage(Character):

    def __init__(self, gui):
        self.special = ['random', self.ciphon, 'Ciphon']
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
                'fullHP': [1, -.43, 88.7, -70],
                'fullSP': [1, -.04, 8.9, 6],
                'atk': [1, -.011, 2.2, 5],
                'def': [1, -.009, 2.1, 10],
                'ma': [1, -.009, 2.19, 13.8],
                'md': [1, -.009, 2.29, 10.3],
                'lck': [1, -.007, 1.42, 10],
                'spe': [1, -.007, 1.43, 10],
		}
        self.atkList = [
                'knock',
                'magic blast',
                'summon',
                'cure'
                ]
        self.setTarget = [
                'cure'
                ]
        self.atkDict = {
                'knock': self.regAtk,
                'magic blast': self.magicBlast,
                'summon': self.summon,
                'cure': self.cure
                }
        super(Mage, self).__init__(gui)

    def ciphon(self, targetInfo):
        '''
        This is the mage's special ability
        random
        '''
        if targetInfo[0] != self.info['name']:
            targetInfo[3] += '\n-->ciphon is activated!'
            targetInfo[13] = [1, 'sp', .5]
        return targetInfo

    def magicBlast(self, target):
        baseAtk = 75
        baseAcc = 90
        string = '%s used magic blast on %s' %(self.info['name'], target)
        mod = {}
        modString = ''
        magAtk = True
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
            
    def summon(self, target):
        pug = [
                target,
                0,
                100,
                self.info['name'] + ' summoned a pug!\n--> Pug used Look Ugly',
                {'def': .7},
                '%s\'s defense lowered.' % target,
                False,
                [0],
                [0],
                [0],
                [0],
                [None],
                [0],
                [0],
                [0],
                ['none'],
                2,
                ]
        daMonkey = [
                target,
                85,
                85,
                '%s summoned Da Monkey!\n--> Da Monkey come into da village and throw barrels at %s' %(self.info['name'], target),
                {'spe': .7},
                '%s\'s speed lowered.' % target,
                False,
                [0],
                [0],
                [0],
                [0],
                [None],
                [0],
                [0],
                [0],
                ['none'],
                3,
                ]
        bahamut = [
                target,
                95,
                50,
                self.info['name'] + ' summoned Bahamut!\n--> Bahamut used Air Slice!',
                {},
                '',
                True,
                [0],
                [0],
                [0],
                [0],
                [None],
                [0],
                [0],
                [0],
                ['air'],
                5,
                ]
        summons = [pug, daMonkey, bahamut]
        y = randint(0, len(summons) -1)
        return summons[y]
            
    def cure(self):
        baseAtk = 0
        baseAcc = 100
        string = '%s used cure' %(self.info['name'])
        mod = {'hp': 5}
        modString = '%s regained some health!' %(self.info['name'])
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
        return [self.info['name'], baseAtk, baseAcc, string,  mod, modString, magAtk,
                skipToFront, waitForHit, waitForNextTurn, multHit, multTarget,
                targetLoseTurn, absorb, status, element, sp]
