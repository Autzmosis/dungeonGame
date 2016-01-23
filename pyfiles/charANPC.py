#! /usr/bin/python2
#coding=utf-8

"""
Yet to be named dungeonGame
by EncodedPixel
coded by タダノデーモン(tadanodaemon)

This program contains the Character class for all fighting/active
classes, the Player class for the usr, and the Active Non-Player 
Character(ANPC) class for any nonplayer characters
"""

from random import *
from kivy.clock import Clock
from threading import Thread
from rogue import Rogue
from warrior import Warrior
from mage import Mage

class Character(object):

    def __init__(self):
        self.inventory = []
        self.status = []
        self.battleStats = {'eva': 100, 'acc': 100}

    def makeSelf(self):
        for x in self.upStats:
            self.upgradeStat(x, True)

    def upgradeStat(self, stat, stop = False):
        if not stop:
            self.upStats[stat][0] += 1
        x, a, b, c = self.upStats[stat]
        self.stats[stat] = int(round((a * (x**2)) + (b * x) + c))
        if stat in ('fullHP', 'fullSP'):
            self.stats['hp'] = self.stats['fullHP']
            self.stats['sp'] = self.stats['fullSP']

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
        if self.stats['hp'] > self.stats['fullHP']:
            self.stats['hp'] = self.stats['fullHP']
        if self.stats['sp'] > self.stats['fullSP']:
            self.stats['sp'] = self.stats['fullSP']
        elif self.stats['hp'] < 0:
            self.stats['hp'] = 0

    def isDead(self):
        if self.stats['hp'] == 0:
            return True
        else:
            return False 

    def checkSpecial(self, targetInfo):
        if targetInfo == 'run':
            return 'run'
        elif self.special[0] == 'random':
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
        a string expressing what type of status effect, and a factor of severness of effect

        element: element of atk

        sp: sp atk requires

        ORDER IS EXTREMELY IMPORTANT
        '''
        if self.gui:
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
        multTarget = None
        targetLoseTurn = [0]
        absorb = [0]
        status = [0]
        element = ['none']
        sp = 0
        return [target, baseAtk, baseAcc, string,  mod, modString, magAtk,
                skipToFront, waitForHit, waitForNextTurn, multHit, multTarget,
                targetLoseTurn, absorb, status, element, sp]

    def luck(self):
        x = randint(1, 150)
        for y in range(1, self.stats['lck'] + 1):
            if y == x:
                return 2
            else:
                return 1

class Player(Character):

    def __init__(self, gui):
        super(Player, self).__init__()
        self.gui = gui
        self.curEquip = []
        self.avaEquip = []
        self.atk = None
        self.itemAtk = ''
        self.enemyNames = None
        self.charNames = None
        self.responce = None
        self.arenaInstance = None
	self.question = ''
        self.Race = Race()
        self.Class = None
        self.tF = True
        self.stats = {
                'hp': 1,
                'sp': 1,
                'fullHP': 1,
                'fullSP': 1,
                'atk': 1,
                'def': 1,
                'ma': 1,
                'md': 1,
                'spe': 1,
                'lck': 1,
                'exp': 0,
                'gol': 0,
                'elem': ['none']
                }

    def changeRC(self, Race = '', Class = ''):
        if Race:
            pass
        if Class:
            if Class == 'warrior':
                self.Class = Warrior(self.regAtk)
                self.berserk = self.Class.berserk
            elif Class == 'rogue':
                self.Class = Rogue(self.regAtk)
            elif Class == 'mage':
                self.Class = Mage(self.regAtk)
            self.special = self.Class.special
            self.upStats = self.Class.upStats
            self.atkList = self.Class.atkList
            self.setTarget = self.Class.setTarget
            self.atkDict = self.Class.atkDict
            self.Class.info = self.info
            self.makeSelf()
        
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

    def updateEquip(self):
        pass

    def generateNextExpForStat(self, stat):
        x = self.upStats[stat][0]
        return int(round((-.7 * (x**3)) + (108.3 * (x**2)) + (1403.85 * x) - 999.47))

    def askQuestion(self, question, enemyNames = [], charNames = [], arenaInstance = None):
        if enemyNames:
	    self.question = question
            self.enemyNames = enemyNames
            self.gui.updateEnemyList()
            self.charNames = charNames
            self.arenaInstance = arenaInstance
            self.invNames = []
            for x in self.inventory:
                self.invNames.append(x.name)
            if (self.arenaInstance.playerTarget != None and len(self.arenaInstance.playerTarget[9]) > 1 
                    and self.arenaInstance.playerTarget[9][2]):
                self.arenaInstance.decide()
            else:
	        Clock.schedule_once(self.askQuestion, .5)
	    return
	if self.question == '':
            self.arenaInstance.report(question)
	else:
	    self.arenaInstance.report(self.question)
	    self.question = ''
        if 'silent' not in self.status:
            self.statModifier({'sp': self.spRegen()})
            self.gui.updateSmallStats()
        self.gui.usr.permission = True
        self.gui.refocus()

    def checkEm(self, text):
        self.gui.usr.permission = False
        if text == 'run':
            self.arenaInstance.playerTarget = text
            self.arenaInstance.report('\n')
            self.arenaInstance.decide()
        elif self.tF:
            if text in self.atkList:
                self.atk = text
                if self.spHandle(text):
                    self.tF = False
                    if len(self.enemyNames) == 1 or text in self.setTarget:
                        try:
                            self.arenaInstance.playerTarget = self.atkDict[text](self.enemyNames[0])
                        except TypeError:
                            self.arenaInstance.playerTarget = self.atkDict[text]()
                        self.tF = True
                        self.arenaInstance.report('\n')
                        self.arenaInstance.decide()
                    else:
                        self.askQuestion('Who do you want to attack?')
                else:
                    self.arenaInstance.report('You don\'t have enough sp to do that!')
                    self.askQuestion('Who do you want to attack?')
            elif text in self.invNames:
                if len(self.enemyNames) == 1:
                    for x in self.inventory:
                        if text == x.name:
                            self.arenaInstance.playerTarget = x.convertToAttack(self, self.info['name'])
                            x.quantity -= 1
                            if not x.quantity:
                                self.inventory.remove(x)
                                self.gui.updateInventory()
                            x.makeDescrip()
                    self.tF = True
                    self.arenaInstance.report('\n')
                    self.arenaInstance.decide()
                else:
                    self.atk = 'inventory'
                    self.itemAtk = text
                    self.askQuestion('Who do you want to attack?')
            else:
                self.arenaInstance.report('Invalid battle command, try again.\n')
                self.askQuestion('What do you want to do?')
        elif text in self.enemyNames:
            if self.atk == 'inventory':
                for x in self.inventory:
                    if self.itemAtk == x.name:
                        self.arenaInstance.playerTarget = x.convertToAttack(self, self.info['name'])
                        x.quantity -= 1
                        if not x.quantity:
                            self.inventory.remove(x)
                            self.gui.updateInventory()
                        x.makeDescrip()
            else:
                self.arenaInstance.playerTarget = self.atkDict[self.atk](text)
            self.tF = True
            self.arenaInstance.report('\n')
            self.arenaInstance.decide()
        else:
            self.arenaInstance.report('Unknown enemy, try again.\n')
            self.askQuestion('Who do you want to attack?')
        self.gui.usr.permission = True

def createANPC(**kwargs):
    #Race = kwargs['race']
    Class = kwargs['Class']
    lvl = kwargs['lvl']
    name = kwargs['name']
    exp = kwargs['exp']
    gold = kwargs['gold']
    inventory = kwargs['inventory']
    aliance = kwargs['aliance']

    class ANPC(Character, Race, Class):

        def __init__(self, lvl):
            for x in self.__class__.__bases__:
                x.__init__(self)
            self.gui = None
            self.info = {'name' : name}
            self.inventory = inventory
            self.stats['gol'] = gold
            self.stats['exp'] = exp
            self.aliance = aliance
            for l in lvl:
                self.upStats[l][0] = lvl[l]
            self.makeSelf()

        def computerFunction(self, charNames, enemyNames):
            if 'silent' not in self.status:
                self.statModifier({'sp': self.spRegen()})
            if self.aliance == 'player':
                rand = randint(0, len(enemyNames) - 1)
                randAtk = randint(0, len(self.atkList) - 1)
                return self.atkDict[self.atkList[randAtk]](enemyNames[rand])
            elif self.aliance == 'enemy':
                rand = randint(0, len(charNames) - 1)
                randAtk = randint(0, len(self.atkList) - 1)
                print randAtk
                return self.atkDict[self.atkList[randAtk]](charNames[rand])

    return ANPC(lvl)

class Race(object):
    pass
