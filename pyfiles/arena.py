#! /usr/bin/python2
#coding=utf-8

"""
Yet to be named dungeonGame
by EncodedPixel
coded by タダノデーモン(tadanodaemon)

This program contains the Arena class, that controls the functionality
of all battles in the game

Right now, I will make it so that I can use it in the terminal
"""

from random import *
from kivy.clock import Clock
from items import makeItem
from collections import OrderedDict

#modules for dev use
from charANPC import makeANPC

class Arena(object):

    def __init__(self, screen, char = [], enemy = []):
        self.gui = screen
        self.char = char
        self.charLength = len(char)
        self.enemy = enemy
        self.enemyLength = len(enemy)
        self.charNames, self.enemyNames, self.order = [[],[],[]]
        self.allChar = self.char + self.enemy
        self.player = char[0]
        self.ran = False
        self.order = OrderedDict([])
        self.playerTarget = None
        self.triedToRun = None
        self.targetDictionary = {}
        self.nextDic = {}
        self.wait = {}
        self.loseTurn = {}
        self.originalStats = {}
        self.Reward = self.reward()
        self.statusDict = {}
        self.pressEnter = False
        self.cleanUp = False
	self.string = ''
        self.queue = []
        self.startQueue = True
        self.isDead = False
        for x in self.allChar:
            x.battleStats['eva'] = 100
            x.battleStats['acc'] = 100
        for c in self.char:
            self.charNames.append(c.info['name'])
            stats = {}
            stats.update(c.stats)
            self.originalStats[c] = stats
        for e in self.enemy:
            self.enemyNames.append(e.info['name'])
        self.gui.usr.permission = True

    def start(self, *args):
        if self.didWin():
            if not self.pressEnter:
                self.report('self.endArena')
                return
            self.distributeReward()
        elif self.isDead:
            if not self.pressEnter:
                self.report('self.endArena')
                return
            self.report('You lose')
        elif self.ran:
            if not self.pressEnter:
                self.report('self.endArena')
                return
            self.report('You coward')
        if self.pressEnter:
            self.report('Press Enter <<<')
            self.gui.pressEnter = True
            self.pressEnter = False
        else:
            while self.gui.snapshot:
                self.gui.snapshot.remove(self.gui.snapshot[0])
            self.pressEnter = True
            self.gui.usr.permission = True
            self.gui.keepinItCool()
            self.player.askQuestion(
                    'What do you want to do?',
                    enemyNames = self.enemyNames,
                    charNames = self.charNames,
                    arenaInstance = self
                    )

    def report(self, string):
        self.queue.append(string)
        if self.startQueue:
            Clock.schedule_interval(self.reportQueue, .2)
            self.startQueue = False

    def reportQueue(self, dt):
        print self.queue
        self.gui.prompt(self.queue[0])
        self.queue.remove(self.queue[0])
        if not self.queue:
            self.startQueue = True
            return False

    def attackFirst(self, List):
        speed = []
        order = []
        luckDic = {}
        for l in List:
            luckDic[l] = l.luck()
        for x in List:
            speed.append([luckDic[x] * x.stats['spe'], x ])
        speed.sort()
        for y in speed:
            for z in List:
                if y[1] == z:
                    order.append(z)
        order.reverse()
        return order

    def hit(self, attacker, baseAcc, defender):
        acc = (baseAcc/100.0) * uniform(.95, 1.05) * (attacker.battleStats['acc'] / defender.battleStats['eva'])
        if acc >= 1:
            return True
        else:
            x = int(round(random()*100))
            acc = int(round(acc * 100))
            for y in range(100 - acc, 100):
                if y == x:
                    return True
                else:
                    False

    def run(self):
        c = 0
        cspe = 0
        e = 0
        espe = 0
        for x in self.char:
            c += x.luck()
            cspe += x.stats['spe']
        for y in self.enemy:
            e += y.luck()
            espe += y.stats['spe']
        c /= self.charLength
        cspe /= self.charLength
        e /= self.enemyLength
        espe /= self.enemyLength
        c *= 1.0
        cspe *= 1.0
        chance = (c/e) * (cspe/espe)
        if chance >= 1:
            return True
        if chance < 1:
            return False

    def spHandle(self, character, sp, message):
        character.statModifier({'sp': sp})
        if character.info['name'] == self.player.info['name']:
            self.gui.snapshot.append((self.player.stats['hp'], self.player.stats['sp']))
            self.report('self.snapshot' + message)
        else:
            self.report(message)

    def elementalRPS(self, atkElement, defElement):
        rps = 1
        rpsString = ''
        for x in atkElement:
            for y in defElement:
                if x == 'none'and y in ('dark', 'light'):
                    rps *= .75
                if x == 'fire':
                    if y in ('dark', 'light'):
                        rps *= .75
                    if y == 'ice':
                        rps *= 2
                    if y == 'water':
                        rps *= .5
                if x == 'ice':
                    if y in ('dark', 'light'):
                        rps *= .75
                    if y == 'air':
                        rps *= 2
                    if y == 'fire':
                        rps *= .5
                if x == 'air':
                    if y in ('dark', 'light'):
                        rps *= .75
                    if y == 'earth':
                        rps *= 2
                    if y == 'ice':
                        rps *= .5
                if x == 'earth':
                    if y in ('dark', 'light'):
                        rps *= .75
                    if y == 'water':
                        rps *= 2
                    if y == 'air':
                        rps *= .5
                if x == 'water':
                    if y in ('dark', 'light'):
                        rps *= .75
                    if y == 'fire':
                        rps *= 2
                    if y == 'earth':
                        rps *= .5
                if x == 'dark':
                    if y == 'light':
                        rps *= 2
                    if y not in ('dark', 'light'):
                        rps *= 1.25
                if x == 'light':
                    if y == 'dark':
                        rps *= 2
                    if y not in ('dark', 'light'):
                        rps *= 1.25
        if rps >= 2:
            rpsString = 'What a blow!'
        elif rps <= .5:
            rpsString = 'Not even a scratch!'
        return rps, rpsString

    def damage(self, char1, info):
        magAtk = info[6]
        char2 = info[0]
        rps, rpsString = self.elementalRPS(info[15], char2.stats['elem'])
        if magAtk:
            defense = 'md'
            attack = 'ma'
        else:
            defense = 'def'
            attack = 'atk'
        baseAtk = (info[1] * char1.stats[attack]) / 100
        luck = char1.luck()
        mod = uniform(.9, 1) * luck * rps
        if luck == 2:
            self.report('That\'s gonna leave a mark!')
        adRatio = (char1.stats[attack] * 1.0) / (char2.stats[defense] * 2.0)
        if rpsString:
            self.report(rpsString)
        return int(round((((adRatio * mod) + baseAtk) * adRatio * luck))) * -1

    def gold(self):
        gold = 0
        for x in self.enemy:
            gold += x.stats['gol']
        gold / self.enemyLength
        luckList = []
        for z in self.char:
            luckList.append(z.luck())
        luck = randint(min(luckList), max(luckList))
        return int(round(gold * luck))

    def exp(self):
        exp = 0
        edef = 0
        eatk = 0
        ehp = 0
        emd = 0
        ema = 0
        for x in self.enemy:
            exp += x.stats['exp']
            edef += x.stats['def']
            eatk += x.stats['atk']
            emd += x.stats['md']
            ema += x.stats['ma']
            ehp += x.stats['hp']
        exp /= self.enemyLength
        edef /= self.enemyLength
        eatk /= self.enemyLength
        ehp /= self.enemyLength
        emd /= self.enemyLength
        ema /= self.enemyLength
        luckList = []
        cdef = 0
        catk = 0
        chp = 0
        cmd = 0
        cma = 0
        for y in self.char:
            luckList.append(y.luck())
            cdef += y.stats['def']
            catk += y.stats['atk']
            cmd += y.stats['md']
            cma += y.stats['ma']
            chp += y.stats['hp']
        cdef /= self.charLength
        catk /= self.charLength
        chp /= self.charLength
        cmd /= self.charLength
        cma /= self.charLength
        luck = randint(min(luckList), max(luckList))
        daRatio = (edef * 1.0) / (catk * 1.0)
        adRatio = (eatk * 1.0) / (cdef * 1.0)
        hpRatio = (ehp * 1.0) / (chp * 1.0)
        mdaRatio = (emd * 1.0) / (cma * 1.0)
        madRatio = (ema * 1.0) / (cmd * 1.0)
        #make a max and min exp, that player will get, and divide by some number to minimize this number
        print daRatio, adRatio, hpRatio, mdaRatio, madRatio, luck
        return int(round(exp * luck * daRatio * adRatio * hpRatio * mdaRatio * madRatio))

    def reward(self):
        dropItem = []
        for x in self.enemy:
            dropItem += x.inventory
        i = randint(0, len(dropItem) - 1)
        reward = [self.gold(), self.exp(), dropItem[i]]
        return reward

    def distributeReward(self): #need to do this after battle after temporary stat changes have been reversed
        numOfChar = len(self.char)
        reward = [self.Reward[0]/numOfChar, self.Reward[1]/numOfChar, self.Reward[2]]
        self.report('Recieved:\n-->%d gold\n-->%d exp\n-->%s' %(reward[0], reward[1], reward[2]))
        hp = 0
        for x in self.char:
            hp = x.stats['hp']
            x.stats.update(self.originalStats[x])
            x.stats['hp'] = hp
            x.statModifier({
                'gol': reward[0],
                'exp': reward[1]
                })
            if not x.inventory:
                item = makeItem(reward[2])
                x.inventory.append(item)
            else:
                for y in x.inventory:
                    if y.name == reward[2]:
                        y.quantity += 1
                        y.makeDescrip()
                    else:
                        item = Item(reward[2])
                        x.inventory.append(item)

    def didWin(self):
        if self.enemyNames == []:
            return True
        else:
            return False

    def changeStatus(self, targetInfo):
        target = targetInfo[0]
        status = targetInfo[14][1]
        severity = targetInfo[14][2]
        target.status.append(status)
        if status in ('poison', 'burn'):
            damage = int(round(target.stats['fullHP'] * .05 * severity * -1))
            self.statusDict[target.info['name'] + status] = damage
        elif status in ('frozen', 'blind', 'silent'):
            if status == 'blind':
                target.statModifier({'acc': .3})
            elif status == 'silent':
                #snapshot
                target.statModifier({'sp': .0})
            time = int(round(randint(2, 5) * severity))
            self.statusDict[target.info['name'] + status] = time

    def statusEffect(self, character):
        name = character.info['name']
        for x in character.status:
            if x in ('poison', 'burn'):
                damage = self.statusDict[name + x]
                self.report('%s is %sed.' %(name, x))
                self.report('%s took %d damage' %(name, damage * -1))
                #snapshot here
                character.statModifier({'hp': damage})
            elif x in ('frozen', 'blind', 'silent'):
                self.statusDict[name + x] -= 1
                if self.statusDict[name + x] == 0:
                    self.report('%s is no longer %s.' %(name, x))
                    character.status.remove(x)
                    del self.statusDict[name + x]

    def checkIfDead(self, character):
        if character.isDead():
            name = character.info['name']
            self.allChar.remove(character)
            if name in self.charNames:
                self.charNames.remove(name)
                if name == self.player.info['name']:
                    message = 'You died\n'
                    self.report(message)
                    return True
                self.report('%s died\n' %(name))
            else:
                self.enemyNames.remove(name)
                self.report('%s died\n' %(name))
                if self.didWin():
                    self.report('You Win')
                    return True
        return False

    def sendMod(self, character,  targetInfo):
        target = targetInfo[0]
        message = ''
        if targetInfo[1]:
            damage = self.damage(character, targetInfo)
            targetInfo[4]['hp'] = damage
            message = '%s did %d damage\n' %(character.info['name'], damage)
            target.statModifier(targetInfo[4])
            if target.info['name'] == self.player.info['name']:
                self.gui.snapshot.append((self.player.stats['hp'], self.player.stats['sp']))
                self.report('self.snapshot' + message)
            else:
                self.report(message)
            if targetInfo[13][0]:
                absorb = int(round(targetInfo[13][2] * damage * -1))
                abmessage = '%s regained %d %s!' %(character.info['name'], absorb, targetInfo[13][1])
                character.statModifier({targetInfo[13][1]: absorb})
                if character.info['name'] == self.player.info['name'] and targetInfo[13][1] in ('hp', 'sp'):
                    self.gui.snapshot.append((self.player.stats['hp'], self.player.stats['sp']))
                    self.report('self.snapshot' + abmessage)
                else:
                    self.report(abmessage)
        if targetInfo[14][0]:
            self.changeStatus(targetInfo)
        if targetInfo[5] != '' and target.stats['hp'] != 0:
            message = targetInfo[5] + '\n'
            if not targetInfo[1]:
                target.statModifier(targetInfo[4])
                if (target.info['name'] == self.player.info['name']
                        and ('hp' in targetInfo[4] or 'sp' in targetInfo[4])):
                    self.gui.snapshot.append((self.player.stats['hp'], self.player.stats['sp']))
                    self.report('self.snapshot' + message)
                else:
                    self.report(message)
            else:
                self.report(message)
        if self.checkIfDead(target):
            return True
        return False

    def multHit(self, character, targetInfo):
        times = targetInfo[10][1]
        c = 0
        targetInfo[10][0] = False
        targetInfo[10].append(1)
        while c != times:
            if targetInfo[0].stats['hp'] == 0:
                return False
            elif targetInfo[10][2] != None and c != 0:
                self.report(targetInfo[10][2])
            elif c != 0:
                self.report('Hit %d time(s)' %(c))
            if self.atkHandle(character, targetInfo):
                return True
            c += 1
        return False

    def multTarget(self, character, targetInfo):
        #user will type all for everyone, allies for teammates
        #and enemies for enemies
        targets = []
        if targetInfo[11] == 0:
            targets.extend(self.allChar)
        elif targetInfo[11] == 1:
            targets.extend(self.enemy)
        elif targetInfo[11] == 2:
            targets.extend(self.char)
        targetInfo[11] = None
        if targets == self.allChar:
            targets.remove(character)
        for x in targets:
            targetInfo[0] = x
            targetInfo[11] = 'true'
            if self.atkHandle(character, targetInfo):
                return True
        return False

    def decide(self):
        self.targetDictionary.clear()
        for x in self.allChar:
            if x in self.nextDic:
                self.targetDictionary[x] = self.nextDic[x]
            else:
                if x.info['name'] == self.player.info['name']:
                    self.targetDictionary[x] = self.playerTarget
                else:
                    self.targetDictionary[x] = x.computerFunction()
        self.skipToFront()

    def skipToFront(self):
        skip = []
        priorityOne = []
        priorityZero = []
        noPriority = []
        self.order.clear()
        if self.playerTarget == 'run' and self.run():
            self.ran = True
            self.report('Run successfull!\n')
            self.start()
            return
        elif self.playerTarget == 'run':
            self.ran = False
            self.report('Run failed!\n')
        for x in self.targetDictionary:
            if x.info['name'] == self.player.info['name'] and self.playerTarget == 'run':
                continue
            elif self.targetDictionary[x][7][0]:
                if self.targetDictionary[x][7][1]:
                    priorityOne.append(x)
                else:
                    priorityZero.append(x)
            else:
                noPriority.append(x)
        priorityZero = self.attackFirst(priorityZero)
        noPriority = self.attackFirst(noPriority)
        newOrder = priorityOne + priorityZero + noPriority
        for y in newOrder:
            self.order.update({y: self.targetDictionary[y]})
        self.atkControl()

    def atkControl(self):
        target = None
        for x in self.order:
            if x in self.loseTurn and x not in self.nextDic and x.stats['hp']:
                self.report(self.loseTurn[x])
            elif x.stats['hp']:
                targetInfo = self.order[x]
                for y in self.allChar:
                    if y.info['name'] == targetInfo[0]:
                        targetInfo[0] = y
                        target = y
                if self.atkHandle(x, targetInfo):
                    self.start()
                    return
        for w in self.wait:
            self.report('%s\'s attack failed' %(target.info['name']))
        for c in self.allChar:
            self.statusEffect(c)
        self.wait.clear()
        self.loseTurn.clear()
        self.start()
    
    def atkHandle(self, character, targetInfo):
        if 'frozen' in character.status:
            self.report('%s is incapable of moving due to ice.' %(character.info['name']))
            return False
        target = targetInfo[0]
        if len(targetInfo[9]) > 1 and not targetInfo[9][0] and targetInfo[9][2]:
            targetInfo[9][2] -= 1
            del self.nextDic[character]
        try: #make it so peeps in multihit don't report their atk string again
            targetInfo[10][3]
        except IndexError:
            if targetInfo[11] in (None, 'true'):
                self.spHandle(character, targetInfo[16] * -1, targetInfo[3])
        if targetInfo[8][0]: #wait for hit
            targetInfo[8][0] = False #turn indicater off
            targetInfo[3] = targetInfo[8][3]
            self.wait[character] = targetInfo
        elif targetInfo[9][0]: #wait for certain amount of turns
            if targetInfo[9][2] != 1:
                targetInfo[9][2] -= 1
                targetInfo[16] = 0
                self.report(targetInfo[9][3])
                if targetInfo[3] != targetInfo[9][3]:
                    targetInfo[3] = targetInfo[9][3]
            else:
                targetInfo[9][0] = False #turn indicater off
                targetInfo[3] = targetInfo[9][4]
            self.nextDic[character] = targetInfo
        elif targetInfo[10][0]: #multHit
            if self.multHit(character, targetInfo):
                return True
        elif targetInfo[11] in range(0,3): #mult target
            if self.multTarget(character, targetInfo):
                return True
        elif len(targetInfo[8]) == 4: #might be useless
            if not targetInfo[8][2]:
                return False
        elif (self.hit(character, targetInfo[2], target)
                and (target not in self.nextDic or self.nextDic[target][9][1])) or target == character: #target hit
            if target in self.wait:
                if self.wait[target][8][1]: #allows hit
                    if self.sendMod(x, targetInfo):
                        return True
                    if targetInfo[12][0]: #lose turn
                        self.loseTurn[target] = targetInfo[12][1]
                    if target.stats['hp'] != 0:
                        if target in self.loseTurn:
                            self.report(self.loseTurn[target])
                        elif self.atkHandle(target, self.wait[target]):
                            return True
                        del self.wait[target]
                else:
                    if self.atkHandle(target, self.wait[target]):
                        return True
                    del self.wait[target]
            else:
                if targetInfo[12][0]: #lose turn
                    self.loseTurn[target] = targetInfo[12][1]
                if self.sendMod(character, targetInfo):
                    return True
        else: #character missed
            self.report('%s missed!\n' %(character.info['name']))
        return False

def main(player, gameScreen): #this is here to test this class
    enemy1 = makeANPC(
            Class = 'rogue',
            lvl = {
                'fullHP': 1,
                'fullSP': 1,
                'atk': 1,
                'def': 1,
                'ma': 1,
                'md': 1,
                'spe': 1,
                'lck': 1
                },
            name = 'Test',
            gold = 100,
            exp = 100,
            inventory = ['herbs',],
	    allies = [], #Dont include self
	    enemies = [player]
            )
    enemy2 = makeANPC(
            Class = 'mage',
            lvl = {
                'fullHP': 1,
                'fullSP': 1,
                'atk': 1,
                'def': 1,
                'ma': 1,
                'md': 1,
                'spe': 1,
                'lck': 1
                },
            name = 'Test1',
            gold = 100,
            exp = 100,
            inventory = ['herbs',],
	    allies = [], #Dont include self
	    enemies = [player]
            )
    arena = Arena(gameScreen, char = [player], enemy = [enemy1])
    return arena
