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

    def __init__(self, data):
        self.inventory = {}
        self.equipment = {}
        self.info = {}
        self.data = data
        
    def updateSelf(self):
        self.stats = self.data.get('player')['stats']
        self.atkList = self.data.get('player')['atkList']
        self.inventory = self.data.get('player')['inventory']
        self.equipment = self.data.get('player')['equipment']
        self.info = self.data.get('player')['info']

    def updateBase(self):
        self.data.put('player',
                stats = self.stats,
                atkList = self.atkList,
                inventory = self.inventory,
                equipment = self.equipment,
                info = self.info
                )

    def statModifier(self, stat, mod):
        if mod > 1 or mod < 0:
            self.stats[stat] += mod
        elif 0 < mod < 1:
            self.stats[stat] *= mod

    def regAtk(self):
        base = 5
        string = ' used ' + self.atkList[0]
        return base, string

    def atkListCheck(self, string):
        if string not in self.atkList:
             return 'I don\'t think you can do that.'
        else:
            return self.atkDict[string]()

    def evadeRun(self):
        pass

    def critHit(self):
        pass


class ANPC(Character):

    def __init__(self):
        self.stats = {}
        self.atkDict = {}

    def computerFunction(self, atkList):
        pass
