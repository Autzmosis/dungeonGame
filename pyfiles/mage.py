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
                'gol': 0
                }
        self.atkList = [
                'knock',
                'magic blast',
                'summon',
                'cure'
                ]
        self.atkDict = {
                'check': self.atkListCheck,
                'knock': self.regAtk,
                'magic blast': self.magicBlast,
                'summon': self.summon,
                'cure': self.cure
                }

    def magicBlast(self):
        baseAtk = 7
        baseAcc = 90
        string = self.info['name'] + ' used magic blast'
        mod = {}
        modString = ''
        return [baseAtk, baseAcc, string, mod, modString, True]
            
    def summon(self):
        pug = [
                0,
                100,
                self.info['name'] + ' summoned a pug!\n--> Pug used Look Ugly',
                {'def': .7},
                'defense lowered.',
                False
                ]
        daMonkey = [
                5,
                85,
                self.info['name'] + ' summoned Da Monkey!\n--> Da Monkey come into da village and throw barrels',
                {'spe': .7},
                'speed lowered.',
                False
                ]
        bahamut = [
                10,
                50,
                self.info['name'] + ' summoned Bahamut!\n--> Bahamut used Fire Breath',
                {},
                '',
                True
                ]
        summons = [pug, daMonkey, bahamut]
        y = randint(0, len(summons) -1)
        return summons[y]
            
    def cure(self):
        baseAtk = 5
        baseAcc = 90
        string = self.info['name'] + ' used cure'
        mod = {}
        modString = ''
        return [baseAtk, baseAcc, string, mod, modString, False]
