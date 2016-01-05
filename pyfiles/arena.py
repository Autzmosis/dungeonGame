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
from time import sleep

#modules for dev use
from rogue import *
from mage import *
from warrior import *
from dungeonOneEnemies import *

class Arena(object):

    def __init__(self, gameScreen, char = [], enemy = []):
        self.gui = gameScreen
        self.char = char
        self.enemy = enemy
        self.charNames, self.enemyNames, self.order = [[],[],[]]
        self.allChar = self.char + self.enemy
        self.player = char[0]
        self.ran = False
        self.order = {}
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
        self.gui.usr.bind(on_text_validate = self.player.askQuestion)

    def start(self, *args):
        if self.didWin():
            self.distributeReward()
            self.gui.usr.unbind(on_text_validate = self.player.askQuestion)
            self.gui.usr.permission = False
            print self.player.stats
        elif self.player.stats['hp'] == 0:
            self.report('You lose')
            self.gui.usr.unbind(on_text_validate = self.player.askQuestion)
            self.gui.usr.permission = False
        elif self.ran:
            self.report('You coward')
            self.gui.usr.unbind(on_text_validate = self.player.askQuestion)
            self.gui.usr.permission = False
        elif self.pressEnter:
            self.gui.usr.bind(on_text_validate = self.start)
            self.report('\n')
            self.report('Press Enter <<<')
            self.pressEnter = False
            self.cleanUp = True
        else:
            sleep(.5)
            if self.cleanUp:
                self.gui.usr.unbind(on_text_validate = self.start)
                self.cleanUp = False
            self.pressEnter = True
            self.player.askQuestion(
                    'What do you want to do?',
                    enemyNames = self.enemyNames,
                    charNames = self.charNames,
                    arenaInstance = self
                    )

    def attackFirst(self, List):
        speed = []
        order = []
        for x in List:
            speed.append(str(x.luck() * x.stats['spe']) + x.info['name'])
        speed.sort()
        for y in speed:
            for z in List:
                if y == str(z.luck() * z.stats['spe']) + z.info['name']:
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
        c *= 1.0
        cspe *= 1.0
        chance = (c/e) * (cspe/espe)
        if chance >= 1:
            return True
        if chance < 1:
            return False

    def spHandle(self, character, sp):
        character.statModifier({'sp': sp})

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
        if rpsString != '':
            self.report(rpsString)
        return int(round((((adRatio * mod) + baseAtk) * adRatio))) * -1

    def gold(self):
        gold = 0
        for x in self.enemy:
            gold += x.stats['gol']
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
        item = dropItem[i]
        reward = [self.gold(), self.exp(), item]
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
            x.inventory.append(reward[2])

    def report(self, string):
        self.gui.prompt(string)
        sleep(.1)

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
                    self.report('You died')
                    return True
            else:
                self.enemyNames.remove(name)
                if self.didWin():
                    self.report('You Win')
                    return True
            self.report('%s died' %(character.info['name']))
        return False

    def sendMod(self, character,  targetInfo):
        target = targetInfo[0]
        if targetInfo[1] != 0:
            damage = self.damage(character, targetInfo)
            if targetInfo[13][0]:
                character.statModifier({targetInfo[13][1]: int(round(targetInfo[13][2] * damage * -1))})
            targetInfo[4]['hp'] = damage
            self.report('%d damage done' %(damage))
        if targetInfo[4] != {}:
            target.statModifier(targetInfo[4])
        if targetInfo[5] != '' and target.stats['hp'] != 0:
            self.report(targetInfo[5])
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
                self.report('\n')
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
        if targetInfo[11] == 0:
            targets = self.allChar
        elif targetInfo[11] == 1:
            targets = self.enemy
        elif targetInfo[11] == 2:
            targets = self.char
        targetInfo[11] = None
        if targets == self.allChar:
            targets.remove(character)
        for x in targets:
            targetInfo[0] = x
            if self.atkHandler(character, targetInfo):
                return True
        return False

    def decide(self):
        for x in self.allChar:
            if x in self.nextDic:
                self.targetDictionary[x] = self.nextDic[x]
            else:
                if x.info['name'] == self.player.info['name']:
                    self.targetDictionary[x] = x.checkSpecial(self.playerTarget)
                else:
                    self.targetDictionary[x] = x.computerFunction(self.charNames, self.enemyNames)
        self.nextDic.clear()
        self.skipToFront()

    def skipToFront(self):
        skip = []
        priorityOne = []
        priorityZero = []
        noPriority = []
        if self.playerTarget == 'run' and self.run():
            self.ran = True
            self.report('Run successfull!')
            self.start()
            return
        elif self.playerTarget == 'run':
            self.ran = False
            self.report('Run failed!')
        for x in self.targetDictionary:
            if self.targetDictionary[x][7][0]:
                if self.targetDictionary[x][7][1]:
                    priorityOne.append(x)
                else:
                    priorityZero.append(x)
            else:
                noPriority.append(x)
        priorityZero = self.attackFirst(priorityZero)
        noPriority = self.attackFirst(noPriority)
        newOrder = priorityOne + priorityZero + noPriority
        for x in self.targetDictionary:
            for y in newOrder:
                if x == y:
                    self.order[y] = self.targetDictionary[x]
        self.atkControl()

    def atkControl(self):
        target = None
        for x in self.order:
            if x in self.loseTurn and x not in self.nextDic:
                #this is where you print a string saying that x lost turn
                self.report(self.loseTurn[x])
            elif x.stats['hp'] != 0:
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
        try: #make it so peeps in multihit don't report their atk string again
            targetInfo[10][3]
        except IndexError:
            self.report('\n')
            self.report(targetInfo[3])
        self.spHandle(character, targetInfo[16] * -1)
        if targetInfo[8][0]: #wait for hit
            targetInfo[8][0] = False #turn indicater off
            targetInfo[3] = targetInfo[8][3]
            self.wait[character] = targetInfo
        elif targetInfo[9][0]: #wait for certain amount of turns
            if targetInfo[9][2] != 1:
                targetInfo[9][2] -= 1
                self.report(targetInfo[9][3])
                targetInfo[3] = targetInfo[9][3]
            else:
                targetInfo[9][0] = False #turn indicater off
                targetInfo[3] = targetInfo[9][4]
            self.nextDic[character] = targetInfo
        elif targetInfo[12][0]: #lose turn
            self.loseTurn[target] = targetInfo[12][1]
        elif targetInfo[10][0]: #multHit
            if self.multHit(character, targetInfo):
                return True
        elif targetInfo[11] in range(0,3): #mult target
            if self.multTarget(character, targetInfo):
                return True
        elif len(targetInfo[8]) == 4:
            if not targetInfo[8][2]:
                return False
        elif self.hit(character, targetInfo[2], target) or target == character: #target hit
            if target in self.wait:
                if self.wait[target][8][1]: #allows hit
                    if self.sendMod(x, targetInfo):
                        return True
                    if target.stats['hp'] != 0:
                        if self.atkHandle(target, self.wait[target]):
                            return True
                        del self.wait[target]
                else:
                    if self.atkHandle(target, self.wait[target]):
                        return True
                    del self.wait[target]
            elif self.sendMod(character, targetInfo):
                return True
        else: #target dodged
            self.report('%s dodged!' %(target.info['name']))
        return False

def main(player, gameScreen): #this is here to test this class
    enemy1 = enemyOne(gameScreen)
    enemy2 = enemyTwo(gameScreen)
    enemy3 = enemyThree(gameScreen)
    arena = Arena(gameScreen, char = [player], enemy = [enemy1, enemy2, enemy3])
    return arena
