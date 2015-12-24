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

class Character(object):

    def __init__(self, data):
        self.inventory = {}
        self.equipment = {}
        self.battleStats = {'eva': 100, 'acc': 100}
        self.info = {'name': 'bill'}
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

    def askQuestion(self, question):
        return raw_input(question).lower()


    def target(self, enemyNames, arenaInstance):
        newX = 0
        arenaInstance.report('Remaining enemies:')
        for x in enemyNames:
            arenaInstance.report(x)
        arenaInstance.report('')
        arenaInstance.report('Available attacks:')
        for x in self.atkList:
            arenaInstance.report(x)
        arenaInstance.report('')
        responce = self.askQuestion('What do you want to do? ')
        returnedValue = None
        for x in range(len(responce) - 1):
            if responce[x:x+3] == 'run':
                returnedValue = 'run'
                return returnedValue
            else:
                for y in self.atkList:
                    if responce[x:x+len(y)] == y:
                        newX = x +len(y) + 1
                        if responce[newX:newX+2] == 'at':
                            newX += 3
                            for e in enemyNames:
                                if responce[newX:newX+len(e)] == e:
                                    returnedValue = [e, self.atkListCheck(y)]
                                    return returnedValue
                            arenaInstance.report('Unknown enemy, please try again')
                            returnedValue = self.target(enemyNames)
                            return returnedValue
                        else:
                            arenaInstance.report('Choosing random enemy...\n')
                            rand = randint(0, len(enemyNames) - 1)
                            returnedValue = [enemyNames[rand], self.atkListCheck(y)]
                            return returnedValue
                arenaInstance.report('Invalid attack, try again')
                returnedValue = self.target(enemyNames, arenaInstance)
                return returnedValue


class ANPC(Character):

    def __init__(self):
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
