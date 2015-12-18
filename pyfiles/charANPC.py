#! /usr/bin/python2
#coding=utf-8

"""
Yet to be named dungeonGame
by EncodedPixel
coded by タダノデーモン(tadanodaemon)

This program contains the Character class for the Rogue, Mage, and Warrior
classes and contains the Active Non-Player Character class for any teammates
and enemies for the game
"""

class Character(object):

    def __init__(self):
        self.stats = {}
        self.atkList = {}

    def statModifier(self, stat, mod):
        pass

    def levelUp(self, stat, adder, level):
        pass

    def regAtk(self):
        base = 5
        string = ' used regatk'
        return base, string

    def atkListCheck(self, string):
        if string not in self.atkList:
             return 'Invalid command'


class ANPC(object):

    def __init__(self):
        pass

    def computerFunction(self, atkDict):
        pass
