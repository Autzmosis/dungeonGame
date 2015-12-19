#! /usr/bin/python2
#coding=utf-8

"""
Yet to be named dungeonGame
by EncodedPixel
coded by タダノデーモン(tadanodaemon)

This program contains the Character class for all fighting/active
classes and contains the Active Non-Player Character class for any teammates
and enemies for the game
"""

class Character(object):

    def __init__(self):
        self.stats = {}
        self.atkList = {}
        self.inventory = {}
        
    def statModifier(self, stat, mod):
        if mod > 1 or mod < 0:
            self.stats[stat] += mod
        elif 0 < mod < 1:
            self.stats[stat] *= mod

    def regAtk(self):
        base = 5
        string = ' used regatk'
        return base, string

    def atkListCheck(self, string):
        if string not in self.atkList:
             return 'Invalid command'

    def evadeRun(self):
        pass

    def critHit(self):
        pass


class ANPC(Character):

    def __init__(self):
        super(ANPC, self).__init__():

    def computerFunction(self, atkList):
        pass
