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
        self.dc = 0
        self.atk = None
        self.enemyNames = None
        self.charNames = None
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

    def askQuestion(self, question, enemyNames = [], charNames = [], arenaInstance = None):
        if self.c == 0:
            if enemyNames != []:
                self.enemyNames = enemyNames
                self.charNames = charNames
                self.arenaInstance = arenaInstance
            if self.dc == 0:
                self.arenaInstance.report('Remaining enemies:')
                for x in self.enemyNames:
                    self.arenaInstance.report(x)
                self.arenaInstance.report('\n')
            self.arenaInstance.report(question)
            self.c = 1
            if self.dc == 1:
                self.c = 2
        elif self.c == 1:
            text = self.gui.usr.text.lower()
            self.gui.usr.text = ''
            self.c = 2
            self.checkEm(text, True)
        elif self.c == 2:
            text = self.gui.usr.text.lower()
            self.gui.usr.text = ''
            self.c = 0
            self.checkEm(text, False)
        self.gui.trigger()

    def checkEm(self, text, tF):
        if tF:
            array = self.atkList
            invalid = 'Invalid attack, try again.'
            question = 'Who do you want to attack?'
            invQuestion = 'What do you want to do?'
            invc = (0, 0)
        else:
            array = self.enemyNames
            invalid = 'Unknown enemy, try again.'
            invQuestion = 'Who do you want to attack?'
            invc = (0, 1)
        if text in range(0,5):
            if text in range(0, len(array)):
                if array == self.atkList:
                    self.atk = self.atkListCheck(array[text])
                    self.arenaInstance.report('>_' + str(array[text]))
                    self.gui.usr.tF = False
                    self.c = 0
                    self.dc = 1
                    self.askQuestion(question)
                else:
                    self.arenaInstance.playerTarget = [array[text], self.atk]
                    self.arenaInstance.report('>_' + str(array[text]))
                    self.gui.usr.tF = True
                    self.c = 0
                    self.dc = 0
                    self.arenaInstance.mainLoop()
            else:
                self.arenaInstance.report(invalid)
                self.c, self.d = invc
                self.askQuestion(invQuestion)
        else:
            if array == self.atkList:
                if text in array:
                    self.atk = self.atkListCheck(text)
                    self.arenaInstance.report('>_' + text)
                    self.gui.usr.tF = False
                    self.c = 0
                    self.dc = 1
                    self.askQuestion(question)
                else:
                    self.arenaInstance.report(invalid)
                    self.c, self.dc = invc
                    self.askQuestion(invQuestion)
            else:
                if text in array:
                    self.arenaInstance.playerTarget = [text, self.atk]
                    self.arenaInstance.report('>_' + text)
                    self.gui.usr.tF = True
                    self.c = 0
                    self.dc = 0
                    self.arenaInstance.mainLoop()
                else:
                    self.arenaInstance.report(invalid)
                    self.c, self.dc = invc
                    self.askQuestion(invQuestion)

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
