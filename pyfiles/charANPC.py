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
        self.inventory = []
        self.status = []
        self.curEquip = []
        self.avaEquip = []
        self.battleStats = {'eva': 100, 'acc': 100}
        self.c = 0
        self.dc = 0
        self.atk = None
        self.enemyNames = None
        self.charNames = None
        self.responce = None
        self.arenaInstance = None
        self.invalid = False
	self.question = ''

        #will hold all items in game
        #self.items = {
        #        'potion': [
        #            quantity,
        #            effect,
        #            descrip,
        #            sell price,
        #            buy price
        #            ],
        #        }
        
    def updateSelf(self):
        self.stats = self.gui.data.get('player')['stats']
        self.atkList = self.gui.data.get('player')['atkList']
        self.inventory = self.gui.data.get('player')['inventory']
        self.curEquip = self.gui.data.get('player')['curEquip']
        self.avaEquip = self.gui.data.get('player')['avaEquip']
        self.info = self.gui.data.get('player')['info']

    def updateBase(self):
        self.gui.data.put('player',
                stats = self.stats,
                atkList = self.atkList,
                inventory = self.inventory,
		curEquip = self.curEquip,
		avaEquip = self.avaEquip,
                info = self.info
                )

    def spHandle(self, atk):
        try:
            if self.atkDict[atk]()[16] > self.stats['sp']:
                return False
            else:
                return True
        except TypeError:
            if self.atkDict[atk]('target')[16] > self.stats['sp']:
                return False
            else:
                return True

    def spRegen(self):
        full = self.stats['fullSP']
        now = self.stats['sp']
        luck = self.luck()
        return int(round(luck * (full / now)))

    def statModifier(self, statMod):
        for x in statMod:
            stat = x
            mod = statMod[x]
            if stat in self.stats:
                if isinstance(mod, float):
                    self.stats[stat] *= mod
                else:
                    self.stats[stat] += mod
            else:
                self.battleStats[stat] *= mod
        if stat in ('hp', 'sp'):
            self.stats['hp'] = int(self.stats['hp'])
            self.stats['sp'] = int(self.stats['sp'])
        if self.stats['hp'] > self.stats['fullHP']:
            self.stats['hp'] = self.stats['fullHP']
        if self.stats['sp'] > self.stats['fullSP']:
            self.stats['sp'] = self.stats['fullSP']
        elif self.stats['hp'] < 0:
            self.stats['hp'] = 0
        if self.info['name'] == self.gui.data.get('player')['info']['name']:
            self.gui.updateSmallStats()

    def isDead(self):
        if self.stats['hp'] == 0:
            return True
        else:
            return False 

    def checkSpecial(self, targetInfo):
        if self.special[0] == 'random':
            rand = random() / self.luck()
            if rand < .1:
                return self.special[1](targetInfo)
            else:
                return targetInfo

    def regAtk(self, target):
        '''
        This is the regular attack for all characters.
        
        The syntax for setting up attacks is:

        [target, baseAtk, baseAcc, atkString, mod, modString, magAtk(t/f),
        skipToFront[(t/f), priority(0/1)], waitForHit[(t/f), (t/f), (t/f), string],
        waitforNextTurn[(t/f), (t/f), #, string], multHit[(t/f), (#/#algorithm), string], 
        multTarget(who#), targetLoseTurn[(t/f), string], absorb[(t/f), string, #],
        status[(t/f), string, #], element, sp]

        all variables are defined below:

        target: contains target name, can be individual or all
        
        baseAtk: the base atk damage of attack
        
        baseAcc: the base accuracy of attack expressed in percent value
        
        atkString: string that will be reported when atk is done
        
        mod: dictionary of mods set up: {<stat(s) being modded>:<mod number value>}
        
        modString: string that will be reported when mod is done
        
        magAtk: boolean that expresses whethe or not the atk i physical or magical
        
        skipToFront: list containg a boolen that expresses whether or not an atk will
        allow character to go first, and priority of that atk to go, either one or zero

        waitForHit: list that contains a boolean that expresses wether or not the atk 
        will wait for character to be hit before execution, a boolean that
        expresses whether or not the character will recieve the damage or not,
        a boolean expressing whether or not there will be a counter attack, 
        and a string that will be shown upon hit

        waitForNextTurn: list that contains a boolean that expresses whether or not 
        atk will wait for next turn to be executed, a boolean that expresses
        whether or not the character will be hit during wait or not, and number
        that expresses how many turns atk will wait, a string for what will be
        expressed upon wait, and a string that will be expressed after wait

        multHit: list that contains a boolean that indicates the atk to have mult hit
        capability or not, a number describing the number of times the atk will
        hit or letting the move algorithm decide, and a string that is to be printed
        or a nothing, meaning the string will be generic

        multTarget: contains a number (or None) that expresses whether or not, an atk
        hits mult targets, and if so who. 0 is for all char except person who launched
        the attack, 1 is for all enemies, and 2 is for all allies of character

        targetLoseTurn: contains a boolean that expresses whether or not the target will lose
        their turn upon execution and a string that also expresses this

        absorb: list that contains a boolean that determines if the atk is absorbing something,
        a string for which stat to be added to, and a number that expresses the factor of
        absorbtion

        status: list that contains a bool expressing whether or not the attack has a status effect,
        a string exxpressing what type of status effect, and a factor of severness of effect

        element: element of atk

        sp: sp atk requires

        ORDER IS EXTREMELY IMPORTANT
        '''
        if self.info['name'] == self.gui.data.get('player')['info']['name']:
            if self.info['class'] == 'warrior':
                if self.berserk:
                    self.statModifier({'atk': 2.0/3, 'def': 2.0})
                    self.berserk = False
        baseAtk = 60
        baseAcc = 95
        string = self.info['name'] + ' used ' + self.atkList[0] + ' on ' + target + '!'
        mod = {}
        modString = ''
        magAtk = False
        skipToFront = [0]
        waitForHit = [0]
        waitForNextTurn = [0]
        multHit = [0]
        multTarget = [None]
        targetLoseTurn = [0]
        absorb = [0]
        status = [0]
        element = ['none']
        sp = 0
        return [target, baseAtk, baseAcc, string,  mod, modString, magAtk,
                skipToFront, waitForHit, waitForNextTurn, multHit, multTarget,
                targetLoseTurn, absorb, status, element, sp]

    def luck(self):
        x = randint(1, 60)
        for y in range(1, self.stats['lck'] + 1):
            if y == x:
                return 2
            else:
                return 1

    def askQuestion(self, question, enemyNames = [], charNames = [], arenaInstance = None):
        if self.c == 0:
            if enemyNames != []:
		self.question = question
                self.enemyNames = enemyNames
                self.charNames = charNames
                self.arenaInstance = arenaInstance
		Clock.schedule_once(self.askQuestion, .5)
		return
            if self.dc == 0:
                if not self.invalid:
                    self.gui.keepinItCool()
                if 'silent' not in self.status:
                    self.statModifier({'sp': self.spRegen()})
                self.arenaInstance.report('Remaining enemies:')
                for x in self.enemyNames:
                    self.arenaInstance.report(x)
                self.arenaInstance.report('\n')
	    if self.question == '':
            	self.arenaInstance.report(question)
	    else:
		self.arenaInstance.report(self.question)
		self.question = ''
            self.c = 1
            if self.dc == 1:
                self.c = 2
            self.gui.usr.permission = True
        elif self.c == 1 and self.gui.usr.text != '':
            text = self.gui.usr.text.lower()
            self.gui.usr.text = ''
            self.c = 2
            self.checkEm(text, True)
        elif self.c == 2 and self.gui.usr.text != '':
            text = self.gui.usr.text.lower()
            self.gui.usr.text = ''
            self.c = 0
            self.checkEm(text, False)
        self.gui.trigger()

    def checkEm(self, text, tF):
        self.gui.usr.permission = False
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
        if text  == 'run':
            self.arenaInstance.playerTarget = text
            self.arenaInstance.report('>_' + text)
            self.c = 0
            self.dc = 0
            self.arenaInstance.decide()
        elif text in range(0,5):
            if text in range(0, len(array)):
                if array == self.atkList:
                    self.atk = array[text]
                    if self.spHandle(self.atk):
                        self.arenaInstance.report('>_' + str(array[text]))
                        self.gui.usr.tF = False
                        self.c = 0
                        self.dc = 1
                        if len(self.enemyNames) == 1 or self.atk in self.setTarget:
                            try:
                                self.arenaInstance.playerTarget = self.atkDict[self.atk](self.enemyNames[0])
                            except TypeError:
                                self.arenaInstance.playerTarget = self.atkDict[self.atk]()
                            self.gui.usr.tF = True
                            self.c = 0
                            self.dc = 0
                            self.arenaInstance.decide()
                        else:
                            self.askQuestion(question)
                    else:
                        self.arenaInstance.report('You don\'t have enough sp to do that')
                        self.c, self.d = invc
                        self.invalid = True
                        self.askQuestion(invQuestion)
                else:
                    self.arenaInstance.playerTarget = self.atkDict[self.atk](array[text])
                    self.arenaInstance.report('>_' + str(array[text]))
                    self.gui.usr.tF = True
                    self.c = 0
                    self.dc = 0
                    self.arenaInstance.decide()
            else:
                self.arenaInstance.report(invalid)
                self.c, self.d = invc
                self.invalid = True
                self.askQuestion(invQuestion)
        else:
            if array == self.atkList:
                if text in array:
                    self.atk = text
                    if self.spHandle(self.atk):
                        self.arenaInstance.report('>_' + text)
                        self.gui.usr.tF = False
                        self.c = 0
                        self.dc = 1
                        if len(self.enemyNames) == 1 or self.atk in self.setTarget:
                            try:
                                self.arenaInstance.playerTarget = self.atkDict[self.atk](self.enemyNames[0])
                            except TypeError:
                                self.arenaInstance.playerTarget = self.atkDict[self.atk]()
                            self.gui.usr.tF = True
                            self.c = 0
                            self.dc = 0
                            self.arenaInstance.decide()
                        else:
                            self.askQuestion(question)
                    else:
                        self.arenaInstance.report('You don\'t have enough sp to do that')
                        self.c, self.d = invc
                        self.invalid()
                        self.askQuestion(invQuestion)
                else:
                    self.arenaInstance.report(invalid)
                    self.c, self.dc = invc
                    self.invalid = True
                    self.askQuestion(invQuestion)
            else:
                if text in array:
                    self.arenaInstance.playerTarget = self.atkDict[self.atk](text)
                    self.arenaInstance.report('>_' + text)
                    self.gui.usr.tF = True
                    self.c = 0
                    self.dc = 0
                    self.arenaInstance.decide()
                else:
                    self.arenaInstance.report(invalid)
                    self.c, self.dc = invc
                    self.invalid = True
                    self.askQuestion(invQuestion)

class ANPC(Character):

    def __init__(self, gui):
        self.status = []
        self.gui = gui
        self.special = ['notrandom']
        self.stats = {
                'hp': 10,
                'sp': 10,
                'fullHP': 10,
                'fullSP': 10,
                'atk': 7,
                'def': 7,
                'ma': 7,
                'md': 7,
                'spe': 10,
                'lck': 10,
                'exp': 10,
                'gol': 10,
                'elem': ['none']
                }
        self.battleStats = {'eva': 100, 'acc': 100}
        self.atkDict = {
                'regular attack': self.regAtk
                }
        self.atkList = ['regular attack']

    def computerFunction(self, charNames, enemyNames):
        self.statModifier({'sp': self.spRegen()})
        if self.aliance == 'player':
            rand = randint(0, len(enemyNames) - 1)
            randAtk = randint(0, len(self.atkList) - 1)
            return self.atkDict[self.atkList[randAtk]](enemyNames[rand])
        elif self.aliance == 'enemy':
            rand = randint(0, len(charNames) - 1)
            randAtk = randint(0, len(self.atkList) - 1)
            return self.atkDict[self.atkList[randAtk]](charNames[rand])
