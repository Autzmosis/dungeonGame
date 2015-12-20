#! /usr/bin/python2
#coding=utf-8

"""
Yet to be named dungeonGame
by EncodedPixel
coded by タダノデーモン(tadanodaemon)

This program conatins the Mage class
"""

from charANPC import Character

class Mage(Character):

    def __init__(self, data):
        super(Mage, self).__init__(data)
        self.stats = {
                'hp': 19,
                'sp': 16,
                'atk': 5,
                'def': 10,
                'ma': 15,
                'md': 15,
                'lck': 5,
                'spe': 10,
                'up': 0,
                'gold': 0
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
        base = 5
        string = ' used atkone'
        return base, string
            
    def summon(self):
        base = 5
        string = ' used atkTwo'
        return base, string
            
    def cure(self):
        base = 5
        string = ' used atkThree'
        return base, string
