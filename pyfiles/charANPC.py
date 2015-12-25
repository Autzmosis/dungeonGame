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

from random import *
from kivy.clock import Clock
from threading import Thread

class Character(object):

    def __init__(self, gui):
        self.gui = gui
        self.inventory = {}
        self.equipment = {}
        self.battleStats = {'eva': 100, 'acc': 100}
        self.c = 0
        self.caught = None
        self.enemyNames = None
        self.responce = None
        self.arenaInstance = None
        
    def updateSelf(self):
        self.stats = self.gui.data.get('player')['stats']
        self.atkList = self.gui.data.get('player')['atkList']
        self.inventory = self.gui.data.get('player')['inventory']
        self.equipment = self.gui.data.get('player')['equipment']
        self.info = self.gui.data.get('player')['info']

    def updateBase(self):
        self.gui.data.put('player',
                stats = self.stats,
                atkList = self.atkList,
                inventory = self.inventory,
                equipment = self.equipment,
                info = self.info
                )

    def statModifier(self, statMod = {}):
        for x in statMod:
            stat = x
            mod = statMod[x]
            if stat in self.stats:
                if mod > 1 or mod < 0:
                    self.stats[stat] += mod
                elif 1 > mod > 0:
                    self.stats[stat] *= mod
            else:
                self.battleStats[stat] *= mod
        if self.stats['hp'] < 0:
            self.stats['hp'] = 0
        if self.info['name'] == self.gui.data.get('player')['info']['name']:
            self.gui.updateSmallStats()

    def isDead(self):
        if self.stats['hp'] == 0:
            return True
        else:
            return False 

    def regAtk(self):
        baseAtk = 5
        baseAcc = 95
        string = self.info['name'] + ' used ' + self.atkList[0]
        mod = {}
        modString = ''
        return [baseAtk, baseAcc, string,  mod, modString, False]

    def atkListCheck(self, string):
        if string not in self.atkList:
             return 'I don\'t think you can do that.'
        else:
            return self.atkDict[string]()

    def luck(self):
        x = randint(1, 160 + self.stats['lck'])
        for y in range(1, self.stats['lck'] + 1):
            if y == x:
                return 2
            else:
                return 1

    def askQuestion(self, question = None):
        if self.c == 0:
            self.gui.usr.bind(on_text_validate = self.askQuestion)
            self.arenaInstance.report(question)
            self.c = 1
        elif self.gui.usr.text != '' and self.c == 1:
            text = self.gui.usr.text
            self.c = 0
            self.responce = text
            self.gui.usr.text = ''
            if self.targetTwo():
                self.arenaInstance.contMainLoop()
        self.gui.trigger()

    def target(self, enemyNames, arenaInstance):
        self.enemyNames = enemyNames
        self.arenaInstance = arenaInstance
        newX = 0
        arenaInstance.report('Remaining enemies:')
        for x in enemyNames:
            arenaInstance.report(x)
        arenaInstance.report('\n')
        self.askQuestion(question = 'What do you want to do?')

    def targetTwo(self):
        returnedValue = None
        for x in range(len(self.responce) - 1):
            if self.responce[x:x+3] == 'run':
                returnedValue = 'run'
                self.arenaInstance.playerTarget = returnedValue
                return 1
            else:
                for y in self.atkList:
                    if self.responce[x:x+len(y)] == y:
                        newX = x +len(y) + 1
                        if self.responce[newX:newX+2] == 'at':
                            newX += 3
                            for e in self.enemyNames:
                                if self.responce[newX:newX+len(e)] == e:
                                    returnedValue = [e, self.atkListCheck(y)]
                                    self.arenaInstance.playerTarget = returnedValue
                                    return 1
                            self.arenaInstance.report('Unknown enemy, please try again\n')
                            self.target(self.enemyNames, self.arenaInstance)
                            return 0
                        else:
                            self.arenaInstance.report('Choosing random enemy...\n')
                            rand = randint(0, len(self.enemyNames) - 1)
                            returnedValue = [self.enemyNames[rand], self.atkListCheck(y)]
                            self.arenaInstance.playerTarget = returnedValue
                            return 1
                self.arenaInstance.report('Invalid attack, try again\n')
                self.target(self.enemyNames, self.arenaInstance)
                return 0


class ANPC(Character):

    def __init__(self, gui):
        self.gui = gui
        self.stats = {
                'hp': 10,
                'sp': 10,
                'atk': 7,
                'def': 7,
                'ma': 7,
                'md': 7,
                'spe': 10,
                'lck': 10,
                'exp': 10,
                'gol': 10
                }
        self.battleStats = {'eva': 100, 'acc': 100}
        self.atkDict = {
                'check': self.atkListCheck,
                'regular attack': self.regAtk
                }
        self.atkList = ['regular attack']

    def computerFunction(self, charNames, enemyNames):
        if self.aliance == 'player':
            rand = randint(0, len(enemyNames) - 1)
            randAtk = randint(0, len(self.atkList) - 1)
            return [enemyNames[rand], self.atkListCheck(self.atkList[randAtk])]
        elif self.aliance == 'enemy':
            rand = randint(0, len(charNames) - 1)
            randAtk = randint(0, len(self.atkList) - 1)
            return [charNames[rand], self.atkListCheck(self.atkList[randAtk])]
