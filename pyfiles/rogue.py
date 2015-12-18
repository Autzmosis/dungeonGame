#! /usr/bin/python2
#coding=utf-8

"""
Yet to be named dungeonGame
by EncodedPixel
coded by タダノデーモン(tadanodaemon)

This program is contains the Rogue class
"""

from charANPC import Character

class Rogue(Character):

    def __init__(self):
        super(Rogue, self).__init__()
        self.stats = {
                'hp': 22,
                'sp': 13,
                'atk': 10,
                'def': 5,
                'ma': 10,
                'md': 5,
                'lck': 15,
                'spe': 15,
                'up': 0
                }
        self.atkList = {
                'check': self.atkListCheck,
                'regular attack': self.regAtk,
                'attack one': self.attackOne,
                'attack two': self.attackTwo,
                'attack Three': self.attackThree
                }

    def attackOne(self):
        base = 5
        string = ' used atkone'
        return base, string
            
    def attackTwo(self):
        base = 5
        string = ' used atkTwo'
        return base, string
            
    def attackThree(self):
        base = 5
        string = ' used atkThree'
        return base, string
