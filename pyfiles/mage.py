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
        super(Mage, self).__init__(gui)
        self.stats = {
                'hp': 19,
                'sp': 16,
                'fullHP': 19,
                'fullSP': 16,
                'atk': 5,
                'def': 10,
                'ma': 15,
                'md': 15,
                'lck': 5,
                'spe': 10,
                'exp': 0,
                'gol': 0,
                'elem': ['none']
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

    def magicBlast(self, target):
        baseAtk = 7
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
        element = ['none']
        sp = 3
        return [target, baseAtk, baseAcc, string,  mod, modString, magAtk,
                skipToFront, waitForHit, waitForNextTurn, multHit, multTarget,
                targetLoseTurn, element, sp]
            
    def summon(self, target):
        pug = [
                target,
                0,
                100,
                self.info['name'] + ' summoned a pug!\n--> Pug used Look Ugly',
                {'def': .7},
                'defense lowered.',
                False,
                [0],
                [0],
                [0],
                [0],
                [None],
                [0],
                ['none'],
                2,
                ]
        daMonkey = [
                target,
                5,
                85,
                '%s summoned Da Monkey!\n--> Da Monkey come into da village and throw barrels at %s' %(self.info['name'], target),
                {'spe': .7},
                'speed lowered.',
                False,
                [0],
                [0],
                [0],
                [0],
                [None],
                [0],
                ['none'],
                3,
                ]
        bahamut = [
                target,
                10,
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
        element = ['none']
        sp = 2
        return [self.info['name'], baseAtk, baseAcc, string,  mod, modString, magAtk,
                skipToFront, waitForHit, waitForNextTurn, multHit, multTarget,
                targetLoseTurn, element, sp]
