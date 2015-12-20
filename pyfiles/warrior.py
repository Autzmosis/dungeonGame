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
                'up': 0,
                'gold': 0
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
        base = 5
        string = ' used atkone'
        return base, string
            
    def parry(self):
        base = 5
        string = ' used atkTwo'
        return base, string
            
    def warcry(self):
        base = 5
        string = ' used atkThree'
        return base, string
