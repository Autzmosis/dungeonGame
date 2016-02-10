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
from items import makeItem

class Character(object):

    def __init__(self):
        self.inventory = []
        self.status = []
        self.battleStats = {'eva': 100, 'acc': 100}

    def makeSelf(self):
        for x in self.upStats:
            self.upgradeStat(x, True)
        for y in self.classUpStats:
            self.upgradeStat(y, 'class')

    def upgradeStat(self, stat, keyword = False):
        if keyword != 'class':
            if not keyword:
                self.upStats[stat][0] += 1
            x, a, b, c = self.upStats[stat]
        else:
            x = self.classLvlHist[self.info['class']]
            a, b, c = self.classUpStats[stat]
        self.stats[stat] += int(round((a * (x**2)) + (b * x) + c))
        if stat in ('fullHP', 'fullSP'):
            self.stats['hp'] = self.stats['fullHP']
            self.stats['sp'] = self.stats['fullSP']

    def spHandle(self, atk):
        try:
            if self.atkDict[atk]['sp'] > self.stats['sp']:
                return False
            else:
                return True
        except TypeError:
            if self.atkDict[atk]['sp'] > self.stats['sp']:
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

    def luck(self):
        x = self.upStats['lck'][0]
        topLimit = int(round(5 * ((-.0005 * (x ** 3)) + (.01 * (x ** 2)) + (2 * x) + 5)))
        r = randint(1, topLimit)
        for y in range(1, self.stats['lck'] + 1):
            if y == r:
                return 2
            else:
                return 1

def makePlayer(**kwargs):
    gui = kwargs['gui']
    Classes = {
            'rogue': makeClass('rogue'),
            'warrior': makeClass('warrior'),
            'mage': makeClass('mage')
            }
    #Species = kwargs['Species']
    Class = kwargs['Class']
    image = '../images/' + Class + '.png'
    name = kwargs['name']
    info = {
            'name': name,
            'image': image,
            'class': Class
            #'species': Species
            }
    classLvlHist = kwargs.pop('classLvlHist', {})
    Class = Classes[Class]
    exp, gol = kwargs['expGol']
    statsUp = kwargs['statsUp']
    inventoryNames = kwargs['inventoryNames']
    #equipmentNames = kwargs['equipmentNames']
    #weaponNames = kwargs['weaponNames']
    #armourNames = kwargs['armourNames']

    class Player(Character, makeSpecies('name'), Class):

        def __init__(self, **kwargs):
            for base in Player.__bases__:
                base.__init__(self)
            self.gui = gui
            self.curEquip = []
            self.avaEquip = []
            self.itemAtk = ''
            self.enemyNames = None
            self.charNames = None
            self.responce = None
            self.arenaInstance = None
	    self.question = ''
            self.tF = True
            self.info = info
            if not classLvlHist:
                self.classLvlHist = {
                        self.info['class']: 1
                            }
            else:
                self.classLvlHist = classLvlHist
            self.stats = {
                    'hp': 12,
                    'sp': 5,
                    'fullHP': 12,
                    'fullSP': 5,
                    'atk': 5,
                    'def': 5,
                    'ma': 5,
                    'md': 5,
                    'spe': 5,
                    'lck': 5,
                    'exp': exp,
                    'gol': gol,
                    'elem': ['none']
                    }
	    self.upStats = {
                    'fullHP': [1, -.0002, .5, 45],
                    'fullSP': [1, -.0002, .02, 5],
                    'atk': [1, -.0001, .03, 2],
                    'def': [1, -.0001, .03, 2],
                    'ma': [1, -.0001, .03, 2],
                    'md': [1, -.0001, .03, 2],
                    'lck': [1, -.00015, .02, 2],
                    'spe': [1, -.00015, .02, 2],
		    }
            for s in statsUp:
                self.stats[s] = statsUp[s][0]
                if s in self.upStats:
                    self.upStats[s][0] = statsUp[s][1]
            self.inventory = []
            self.weapon = []
            self.armour = []
            self.equipment = []
            for i in inventoryNames:
                item = makeItem(i)
                item.quantity = inventoryNames[i]
                item.makeDescrip()
                self.inventory.append(item)
            #for w in weaponNames:
                #item = makeItem(w)
                #item.makeDescrip()
                #self.weapon.append(item)
            #for a in armourNames:
                #item = makeItem(w)
                #item.makeDescrip()
                #self.armour.append(item)
            #for e in equipmentNames:
                #item = makeItem(e)
                #item.quantity = equipmentNames[e]
                #item.makeDescrip()
                #self.equipment.append(item)
            self.updateBase()

        def updateBase(self):
            statsUp = {}
            for s in self.stats:
                if s in self.upStats:
                    statsUp[s] = [self.stats[s], self.upStats[s][0]]
                else:
                    statsUp[s] = [self.stats[s], None]
            inventoryNames = {}
            #weaponNames = {}
            #armourNames = {}
            #eqipmentNames = {}
            for i in self.inventory:
                inventoryNames[i.name] = i.quantity
            #for w in self.weapon:
            #    weaponNames.append(w.name)
            #for a in armour:
            #    armourNames.append(a.name)
            #for e in equipment:
            #    equipmentNames[e.name] = e.quantity
            self.gui.data.put('player',
                    stats = statsUp,
                    classLvlHist = self.classLvlHist,
		    curEquip = self.curEquip,
		    avaEquip = self.avaEquip,
                    info = self.info,
                    inventory = inventoryNames,
                    #weapon = weaponNames,
                    #armour = armourNames,
                    #equipment = eqipmentNames
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
                if (self.arenaInstance.playerTarget != None and
                        isinstance(self.arenaInstance.playerTarget, list) and
                        len(self.arenaInstance.playerTarget[9]) > 1 and
                        self.arenaInstance.playerTarget[9][2]):
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
                            if text not in self.setTarget:
                                self.arenaInstance.playerTarget = self.makeAtk(text, self.enemyNames[0])
                            else:
                                self.arenaInstance.playerTarget = self.makeAtk(text)
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
                    self.arenaInstance.playerTarget = self.makeAtk(self.atk, text)
                self.tF = True
                self.arenaInstance.report('\n')
                self.arenaInstance.decide()
            else:
                self.arenaInstance.report('Unknown enemy, try again.\n')
                self.askQuestion('Who do you want to attack?')
            self.gui.usr.permission = True

    return Player()

def makeANPC(**kwargs):
    Classes = {
            'rogue': makeClass('rogue'),
            'warrior': makeClass('warrior'),
            'mage': makeClass('mage')
            }
    #Species = kwargs['species']
    classLvlHist = kwargs.pop('classLvlHist', {})
    Class = Classes[kwargs['Class']]
    lvl = kwargs['lvl']
    name = kwargs['name']
    exp = kwargs['exp']
    gold = kwargs['gold']
    inventory = kwargs['inventory']
    enemies = kwargs['enemies']
    allies = kwargs['allies']

    class ANPC(Character, makeSpecies('name'), Class):

        def __init__(self):
            for base in ANPC.__bases__:
                base.__init__(self)
            self.gui = None
            self.info = {
                    'name' : name,
                    'class': kwargs['Class']
                    }
            self.inventory = inventory
            if not classLvlHist:
                self.classLvlHist = {
                        self.info['class']: 1
                            }
            else:
                self.classLvlHist = classLvlHist
            self.stats = {
                    'hp': 12,
                    'sp': 5,
                    'fullHP': 12,
                    'fullSP': 5,
                    'atk': 5,
                    'def': 5,
                    'ma': 5,
                    'md': 5,
                    'spe': 5,
                    'lck': 5,
                    'exp': exp,
                    'gol': gold,
                    'elem': ['none']
                    }
	    self.upStats = {
                    'fullHP': [1, -.0002, .5, 45],
                    'fullSP': [1, -.0002, .02, 5],
                    'atk': [1, -.0001, .03, 2],
                    'def': [1, -.0001, .03, 2],
                    'ma': [1, -.0001, .03, 2],
                    'md': [1, -.0001, .03, 2],
                    'lck': [1, -.00015, .02, 2],
                    'spe': [1, -.00015, .02, 2],
		    }
            self.enemies = enemies
            self.enemyNames = []
            self.allies = allies
            self.allyNames = []
            for e in enemies:
                self.enemyNames.append(e.info['name'])
            for a in allies:
                self.allyNames.append(a.info['name'])
            for l in lvl:
                self.upStats[l][0] = lvl[l]
            self.makeSelf()

        def computerFunction(self):
            if 'silent' not in self.status:
                self.statModifier({'sp': self.spRegen()})
            return self.random(self.enemyNames)

        def random(self, array):
            randTarget = array[randint(0, len(array) - 1)]
            randAtk = self.atkList[randint(0, len(self.atkList) - 1)]
            if randAtk in self.setTarget:
                return self.makeAtk(randAtk)
            else:
                return self.makeAtk(randAtk, randTarget)

    return ANPC()

def makeSpecies(name):

    class Species(object):
        pass

    return Species

def makeClass(name, trigger = False):
    '''
    This function makes every class used in battle, it can also be
    used to change the class of a character.
    '''

    '''
    Below is the regular attack for all characters.
        
    The syntax for setting up attacks is:

    [target, baseAtk, baseAcc, atkString, mod, modString, magAtk(t/f),
    skipToFront[(t/f), priority(0/1)], waitForHit[(t/f), (t/f), (t/f), string],
    waitforNextTurn[(t/f), (t/f), #, string], multHit[(t/f), (#/#algorithm), string], 
    multTarget(who#), targetLoseTurn[(t/f), string], absorb[(t/f), string, #],
    status[(t/f), string, #], element, sp]

    all variables are defined below:

    target: contains target name, can be individual or all (this will only be useful
    when an atk has a set target)
        
    baseAtk: the base atk damage of attack
    default -> 0
        
    baseAcc: the base accuracy of attack expressed in percent value
    No Default, must be entered
        
    atkString: string that will be reported when atk is done
    No Default, must be entered
        
    mod: dictionary of mods set up: {<stat(s) being modded>:<mod number value>}
    default -> {}
        
    modString: string that will be reported when mod is done
    default -> ''
        
    magAtk: boolean that expresses whethe or not the atk i physical or magical
    default -> False
        
    skipToFront: list containg a boolen that expresses whether or not an atk will
    allow character to go first, and priority of that atk to go, either one or zero
    default -> [0]

    waitForHit: list that contains a boolean that expresses wether or not the atk 
    will wait for character to be hit before execution, a boolean that
    expresses whether or not the character will recieve the damage or not,
    a boolean expressing whether or not there will be a counter attack, 
    and a string that will be shown upon hit
    default -> [0]

    waitForNextTurn: list that contains a boolean that expresses whether or not 
    atk will wait for next turn to be executed, a boolean that expresses
    whether or not the character will be hit during wait or not, and number
    that expresses how many turns atk will wait, a string for what will be
    expressed upon wait, and a string that will be expressed after wait
    default -> [0]

    multHit: list that contains a boolean that indicates the atk to have mult hit
    capability or not, a number describing the number of times the atk will
    hit or letting the move algorithm decide, and a string that is to be printed
    or a nothing, meaning the string will be generic
    default -> [0]

    multTarget: contains a number (or None) that expresses whether or not, an atk
    hits mult targets, and if so who. 0 is for all char except person who launched
    the attack, 1 is for all enemies, and 2 is for all allies of character
    default -> None

    targetLoseTurn: contains a boolean that expresses whether or not the target will lose
    their turn upon execution and a string that also expresses this
    default -> [0]

    absorb: list that contains a boolean that determines if the atk is absorbing something,
    a string for which stat to be added to, and a number that expresses the factor of
    absorbtion
    default -> [0]

    status: list that contains a bool expressing whether or not the attack has a status atkDict[atk],
    a string expressing what type of status atkDict[atk], and a factor of severness of atkDict[atk]
    default -> [0]

    element: element of atk
    default -> ['none']

    sp: sp atk requires
    default -> 0

    ORDER IS EXTREMELY IMPORTANT
    '''
    regAtk = {
            'baseAtk': 60,
            'baseAcc': 95,
            'atkString': 'name used atkName on targetName',
            'sp': 0
            }

    classDict = {
            'rogue': {
                'special': ['Dual Blitz', 'ifDmg', 'random', {
                    3: '\n--> name \'s dual blitz activated!',
                    10: [1, 2, 'here is the second!'],
                    16: 0
                    }
                    ],
                'upStats': {
                    'lck': [-.00015, .02, 2],
                    'spe': [-.00015, .02, 2],
                    },
                'atkList': ['shank', 'smokescreen', 'backstab', 'shade thrust'],
                'atks': {
                    'shank': regAtk,
                    'smokescreen': {
                        'baseAcc': 90,
                        'atkString': 'name used smokescreen!',
                        'mod': {'acc': .7},
                        'modString': 'targetName \'s accuracy lowered.',
                        'sp': 2
                        },
                    'backstab': {
                        'baseAtk': 85,
                        'baseAcc': 90,
                        'atkString': 'name used backstab!',
                        'mod': {'def': .7},
                        'modString': 'targetName \'s defense lowered.',
                        'sp': 3
                        },
                    'shade thrust': {
                        'baseAtk': 95,
                        'baseAcc': 70,
                        'atkString': 'name used shade thrust!',
                        'magAtk' : True,
                        'element': ['dark'],
                        'sp': 5
                        }
                    }
                },
            'warrior': {
                'special': ['Berserk', 'ifDmg', 'random', {
                    3: '\n--> name just went berserk!',
                    'statMod': {'atk': 1.5, 'def': .5},
                    'berserk': True
                    }
                    ],
                'upStats': {
                    'fullHP': [-.0002, .5, 45],
                    'def': [-.0001, .03, 2],
                    },
                'setTarget': ['parry', 'warcry'],
                'atkList': ['slash', 'sheild bash', 'parry', 'warcry'],
                'atks': {
                    'slash': regAtk,
                    'sheild bash': {
                        'baseAtk': 85,
                        'baseAcc': 90,
                        'atkString': 'name used sheild bash!',
                        'mod': {'atk': .9},
                        'modString': 'targetName \'s attack lowered.',
                        'sp': 3
                        },
                    'parry': {
                        'target': 'name',
                        'baseAcc': 100,
                        'atkString': 'name used parry!',
                        'waitForHit': [1, 0, 0, 'name parried the attack!'],
                        'sp': 1
                        },
                    'warcry': {
                        'target': 'name',
                        'baseAcc': 95,
                        'atkString': 'name used warcry!',
                        'mod': {'atk': 1.5, 'def': .75},
                        'modString': 'name \'s attack rose and defense lowered!',
                        'sp': 2
                        }
                    }
                },
            'mage': {
                'special': ['Ciphon', 'random', 'ifDmg', {
                    3: '\n--> name \'s ciphon was activated',
                    13: [1, 'sp', .5]
                    }
                    ],
                'upStats': {
                    'ma': [-.0001, .03, 2],
                    'md': [-.0001, .03, 2],
                    },
                'setTarget': ['cure'],
                'atkList': ['knock', 'magic blast', 'summon', 'cure'],
                'atks': {
                    'knock': regAtk,
                    'magic blast': {
                        'baseAtk': 75,
                        'baseAcc': 90,
                        'atkString': 'name used magic blast!',
                        'magAtk': True,
                        'sp': 3
                        },
                    'summon': [
                        {
                            'name': 'pug',
                            'baseAcc': 100,
                            'atkString': 'name summoned a pug!\n--> Pug used Look Ugly!',
                            'mod': {'def': .7},
                            'modString': 'targetName \'s defense lowered.',
                            'sp': 2
                            },
                        ],
                    'cure': {
                        'target': 'name',
                        'baseAcc': 100,
                        'atkString': 'name used cure!',
                        'mod': {'hp': 5},
                        'modString': 'name regained some health!',
                        'sp': 2
                        }
                    }
                },
            }

    special = classDict[name]['special']
    upStats = classDict[name]['upStats']
    atks = classDict[name]['atks']
    atkList = classDict[name]['atkList']
    setTarget = classDict[name].pop('setTarget', [])
    berserk = False
    if name == 'warrior':
        berserk = True

    class Class(object):

        def __init__(self):
            self.classUpStats = upStats
            self.special = special
            self.atkDict = atks
            self.setTarget = setTarget
            self.atkList = atkList
            if berserk:
                self.berserk = False

        def makeAtk(self, atk, targetName = ''):
            if isinstance(self.atkDict[atk], list):
                rand = randint(0, len(self.atkDict[atk]) - 1)
                atkInfo = self.atkDict[atk][rand]
            else:
                atkInfo = self.atkDict[atk]
            target = atkInfo.pop('target', targetName)
            baseAtk = atkInfo.pop('baseAtk', 0)
            baseAcc = atkInfo['baseAcc']
            string = atkInfo['atkString']
            mod = atkInfo.pop('mod', {})
            modString = atkInfo.pop('modString', '')
            magAtk = atkInfo.pop('magAtk', False)
            skipToFront = atkInfo.pop('skipToFront', [0])
            waitForHit = atkInfo.pop('waitForHit', [0])
            waitForNextTurn = atkInfo.pop('waitForNextTurn', [0])
            multHit = atkInfo.pop('multiHit', [0])
            multTarget = atkInfo.pop('multTarget', None)
            targetLoseTurn = atkInfo.pop('targetLoseTurn', [0])
            absorb = atkInfo.pop('absorb', [0])
            status = atkInfo.pop('status', [0])
            element = atkInfo.pop('element', ['none'])
            sp = atkInfo['sp']
            targetInfo = [targetName, baseAtk, baseAcc, string,  mod, modString, magAtk,
                    skipToFront, waitForHit, waitForNextTurn, multHit, multTarget,
                    targetLoseTurn, absorb, status, element, sp]
            if 'ifDmg' in self.special:
                if 'random' in self.special:
                    rand = random() / self.luck()
                    if rand < .1:
                        for x in self.special[3]:
                            if x == 3:
                                targetInfo[x] += self.special[3][x]
                            elif x in range(1, len(targetInfo) + 1):
                                targetInfo[x] = self.special[3][x]
                            if x == 'statMod':
                                self.statModifier(self.special[3][x])
                            if x == 'berserk':
                                self.berserk = True
            targetInfo = self.checkForString(targetInfo, targetName, atk)
            return targetInfo

        def checkForString(self, Set, targetName, atk):
            for i, t in enumerate(Set):
                if isinstance(t, str):
                    Set[i] = self.makeString(t, targetName, atk)
                elif isinstance(t, list):
                    Set[i] = self.checkForString(t, targetName, atk)
            return Set

        def makeString(self, string, targetName, atk):
            spltStr = string.split()
            for i, x in enumerate(spltStr):
                if x == 'name':
                    spltStr[i] = self.info['name']
                elif x == 'atkName':
                    spltStr[i] = atk
                elif x == 'targetName':
                    spltStr[i] = targetName
            while '\'s' in spltStr:
                spltStr[spltStr.index('\'s') - 1] += '\'s'
                spltStr.remove('\'s')
            string = ''
            for s in spltStr:
                if self.info['class'] == 'mage':
                    print s
                string += (s + ' ')
            string = string[:len(string) - 1]
            return string

        def changeClass(self, name):
            classDict = makeClass(name, True)
            self.special = classDict['special']
            self.classUpStats = classDict['upStats']
            self.atkDict = classDict['atks']
            self.atkList = classDict['atkList']
            self.setTarget = classDict.pop('setTarget', [])
            if name == 'warrior':
                self.berserk = True
            self.info['class'] = name
            if self.info['class'] not in self.classLvlHist:
                self.classLvlHist[self.info['class']] = 1

        def lvlUp(self):
            self.classLvlHist[self.info['class']] += 1
            for x in classUpStats:
                self.upgradeStat(x, 'class')

    if trigger:
        return classDict[name]
    return Class
