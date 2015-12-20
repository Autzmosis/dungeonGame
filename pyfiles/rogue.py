#! /usr/bin/python2
#coding=utf-8

"""
Yet to be named dungeonGame
by EncodedPixel
coded by タダノデーモン(tadanodaemon)

This program contains the Rogue class
"""

from charANPC import Character

class Rogue(Character):
    
    def __init__(self, data):
        super(Rogue, self).__init__(data)
        self.stats = {
            'hp': 22,
            'sp': 13,
            'atk': 10,
            'def': 5,
            'ma': 10,
            'md': 5,
            'lck': 15,
            'spe': 15,
            'up': 0,
            'gold': 0
            }
        self.atkList = [
                'shank',
                'smokescreen',
                'backstab',
                'throw'
                ]
        self.atkDict = {
                'check': self.atkListCheck,
                'shank': self.regAtk,
                'smokescreen': self.smokescreen,
                'backstab': self.backstab,
                'throw': self.throw
                }

    def smokescreen(self):
        base = 5
        string = ' used smokescreen'
        return base, string
            
    def backstab(self):
        base = 5
        string = ' used backstab'
        return base, string
            
    def throw(self):
        base = 5
        string = ' used throw'
        return base, string
