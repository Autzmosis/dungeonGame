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
from rogue import *
from mage import *
from warrior import *
from pet import *
from dungeonOneEnemies import *

class Arena(object):

    def __init__(self, player, gameScreen, char = [], enemy = []):
        self.gui = gameScreen
        self.char = char
        self.enemy = enemy
        self.charNames, self.enemyNames, self.order = [[],[],[]]
        self.allChar = self.char + self.enemy
        self.player = player
        self.ran = False
        self.order = []
        self.Reward = self.reward()
        self.playerTarget = None
        self.triedToRun = None
        #self.wait = {}
        for x in self.allChar:
            x.battleStats['eva'] = 100
            x.battleStats['acc'] = 100
        for c in self.char:
            self.charNames.append(c.info['name'])
        for e in self.enemy:
            self.enemyNames.append(e.info['name'])
        self.mainLoop()

    def start(self):
        if self.didWin():
            for x in self.Reward:
                self.report(str(x))
            self.gui.usr.bind(on_text_validate = self.gui.__on_enter__)
        elif self.player.stats['hp'] == 0:
            self.report('You lose')
            self.gui.usr.bind(on_text_validate = self.gui.__on_enter__)
        elif self.ran:
            self.report('You coward')
            self.gui.usr.bind(on_text_validate = self.gui.__on_enter__)
        else:
            sleep(1)
            self.mainLoop()

    def attackFirst(self):
        speed = []
        order = []
        for x in self.allChar:
            speed.append(str(x.luck() * x.stats['spe']) + x.info['name'])
        speed.sort()
        for y in speed:
            for z in self.allChar:
                if y == str(z.luck() * z.stats['spe']) + z.info['name']:
                    order.append(z)
        order.reverse()
        self.order = order

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

    def damage(self, char1, baseAtk,  char2, magAtk):
        if magAtk:
            defense = 'md'
            attack = 'ma'
        else:
            defense = 'def'
            attack = 'atk'
        mod = uniform(.9, 1) * char1.luck()
        adRatio = (char1.stats[attack] * 1.0) / (char2.stats[defense] * 2.0)
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
        return int(round(exp * luck * daRatio * adRatio * hpRatio * mdaRatio * madRatio))

    def reward(self):
        dropItem = []
        for x in self.enemy:
            dropItem += x.inventory
        i = randint(0, len(dropItem) - 1)
        item = dropItem[i]
        reward = [str(self.gold()) + ' gold', str(self.exp()) + ' exp', item]
        return reward

    def distributeReward(self): #need to do this after battle after temporary stat changes have been reversed
        pass

    def report(self, string):
        self.gui.prompt(string)
        sleep(.1)

    def didWin(self):
        if self.enemyNames == []:
            return True
        else:
            return False

    def atkPhase(self, atker, target, contender):
        string = ''
        self.report(target[1][2] + ' on ' + contender.info['name'] + '!') #report attack string
        if self.hit(atker, target[1][1], contender):
            if target[1][3] == {}: #checking if its a mod or not
                damage = self.damage(atker, target[1][0], contender, target[1][5])
                target[1][3]['hp'] = damage
                contender.statModifier(statMod = target[1][3])
                self.report('%d damage done!\n' %(damage))
                if contender.isDead():
                    for a in self.allChar:
                        if a.info['name'] == contender.info['name']:
                            self.allChar.remove(a)
                    for v in self.enemyNames:
                        if contender.info['name'] == v:
                            self.enemyNames.remove(v)
                    for l in self.charNames:
                        if contender.info['name'] == l:
                            self.charNames.remove(l)
                    if contender.info['name'] == self.player.info['name']:
                        self.report('U died')
                        return True
                    elif self.didWin():
                        self.report('You win')
                        return True
                    else:
                        self.report('%s died\n' %(contender.info['name']))
                return False
            else:
                if target[1][0] == 0: #means damage done is 0
                    contender.statModifier(statMod = target[1][3])
                    self.report('%s\'s %s\n' %(contender.info['name'], target[1][4]))
                    return False
                else:
                    damage = self.damage(atker, target[1][0], contender, target[1][5])
                    target[1][3]['hp'] = damage
                    contender.statModifier(statMod = target[1][3])
                    self.report('%d damage done!' %(damage))
                    self.report('%s\'s %s\n' %(contender.info['name'], target[1][4]))
                    if contender.isDead():
                        for a in self.allChar:
                            if a.info['name'] == contender.info['name']:
                                self.order.remove(a)
                        for v in self.enemyNames:
                            if contender.info['name'] == v:
                                self.enemyNames.remove(v)
                        for l in self.charNames:
                            if contender.info['name'] == l:
                                self.charNames.remove(l)
                        if contender.info['name'] == self.player.info['name']:
                            self.report('U died')
                            return True
                        elif self.didWin():
                            self.report('You win', .5)
                            return True
                        else:
                            self.report('%s died\n' %(contender.info['name']))
                    return False
        else:
            self.report('%s dogded!\n' %(contender.info['name']))
            return False

    def mainLoop(self):
        self.triedToRun = False
        self.player.target(self.enemyNames, self)#this is where you let the player choose there atk and who to use it on
        
    def contMainLoop(self):
        if self.playerTarget == 'run' and self.run():
            self.ran = True
            self.report('Run successfull')
            self.start()
            return 0
        elif self.playerTarget == 'run':
            self.triedToRun = True
            self.report('Run failed')
        enemy = None
        for y in self.allChar:
            if y.info['name'] == self.playerTarget[0]:
                enemy = y
        self.attackFirst()
        if self.triedToRun:
            for b in self.order:
                if b.info['name'] == self.player.info['name']:
                    self.order.remove(b)
        for x in self.order:
            if x.info['name'] == self.player.info['name']:
                if self.atkPhase(x, self.playerTarget, enemy):
                    self.start()
                    return 0
            elif x.stats['hp'] != 0:
                target = x.computerFunction(self.charNames, self.enemyNames)
                contender = None
                for c in self.allChar:
                    if c.info['name'] == target[0]:
                        contender = c
                if self.atkPhase(x, target, contender):
                    self.start()
                    return 0
        self.start()
        return 0

def main(player, gameScreen):
    pet = Pet(gameScreen)
    enemy1 = enemyOne(gameScreen)
    enemy2 = enemyTwo(gameScreen)
    enemy3 = enemyThree(gameScreen)
    arena = Arena(player, gameScreen, char = [player, pet], enemy = [enemy1, enemy2, enemy3])

if __name__ == '__main__': main('mage')
