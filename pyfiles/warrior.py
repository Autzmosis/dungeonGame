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

    def __init__(self):
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
                'name': '',
                'gold': 0
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
