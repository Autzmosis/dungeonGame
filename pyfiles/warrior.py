#! /usr/bin/python2
#coding=utf-8

"""
Yet to be named dungeonGame
by EncodedPixel
coded by タダノデーモン(tadanodaemon)

This program contains the Warrior class, for the game
"""

from charANPC import Character

class Warrior(Character):

    def __init__(self, data):
        super(Warrior, self).__init__(data)
        self.stats = {
                'hp': 25,
                'sp': 10,
                'atk': 15,
                'def': 15,
                'ma': 5,
                'md': 10,
                'lck': 5,
                'spe': 10,
                'exp': 0,
                'gol': 0
                }
        self.atkList = [
                'slash',
                'shield bash',
                'parry',
                'warcry'
                ]
        self.atkDict = {
                'check': self.atkListCheck,
                'slash': self.regAtk,
                'shield bash': self.shieldBash,
                'parry': self.parry,
                'warcry': self.warcry
                }

    def shieldBash(self):
        baseAtk = 7
        baseAcc = 90
        string = self.info['name'] + ' used shield bash'
        mod = {'atk': .9}
        modString = ''
        return [baseAtk, baseAcc, string, mod, modString, False]
            
    def parry(self):
        baseAtk = 5
        baseAcc = 90
        string = self.info['name'] + ' used parry'
        mod = {}
        modString = ''
        return [baseAtk, baseAcc, string, mod, modString, False]
            
    def warcry(self):
        baseAtk = 5
        baseAcc = 90
        string = self.info['name'] + ' used warcry'
        mod = {}
        modString = ''
        return [baseAtk, baseAcc, string, mod, modString, False]
