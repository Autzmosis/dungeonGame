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

    def __init__(self):
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
                'name': '',
                'gold': 0
                }
        self.atklist = {
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
