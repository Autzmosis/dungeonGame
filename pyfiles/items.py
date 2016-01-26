#! /usr/bin/python2
#coding=utf-8

'''
Yet to be named dungeon game
coded by タダノデーモン(tadanodaemon)

This file holds the item class  and equipment class
and all defined items
'''

class Item(object):

    def __init__(self, name):
        self.name = name
        self.itemDict = {
                'herbs': [
                    ['[b]Genetically Enhanced\nHerbs[/b]\nQuantity: ',
                        '\n\nThe natives method\nof healing (scoff)\nwounds. Heals\nup to 20 hp.'
                        ],
                    {
                        'mod': {'hp': 20},
                        'string': ' ate some herbs!',
                        'modString': ' regained a little hp!'
                        },
                    10, #sell price
                    15, #buy price
                    False, #is this equipment
                    'a list of numbers for levelup' #will only be used in equipment
                    ]
                }
        self.descripComponents = self.itemDict[self.name][0]
        self.effect = self.itemDict[self.name][1]
        self.sellPrice = self.itemDict[self.name][2]
        self.buyPrice = self.itemDict[self.name][3]
        self.quantity = 1
        if self.itemDict[self.name][4]:
            self.upStats = self.itemDict[self.name][5]
            self.upExp = self.itemDict[self.name][6]
            self.exp = [self.itemDict[self.name][7], self.itemDict[self.name][8]]
            self.lvl = 1
        self.makeDescrip()

    def makeDescrip(self):
        first, last = self.descripComponents
        self.descrip = first + str(self.quantity) + last

    def transmutate(self, newName):
        self.__init__(newName)

    def convertToAttack(self, character, target):
        name = character.info['name']
        baseAtk = self.effect.pop('baseAtk', 0)
        baseAcc = self.effect.pop('baseAcc', 100)
        string = name + self.effect['string'] #needs to be set in item definition
        mod = self.effect.pop('mod', {})
        modString = name + self.effect['modString'] #needs to be set in item definition
        magAtk = self.effect.pop('magAtk', False)
        skipToFront = self.effect.pop('skipToFront', [0])
        waitForHit = self.effect.pop('waitForHit', [0])
        waitForNextTurn = self.effect.pop('waitForNextTurn', [0])
        multHit = self.effect.pop('multiHit', [0])
        multTarget = self.effect.pop('multTarget', None)
        targetLoseTurn = self.effect.pop('targetLoseTurn', [0])
        absorb = self.effect.pop('absorb', [0])
        status = self.effect.pop('status', [0])
        element = self.effect.pop('element', ['none'])
        sp = 0
        return [target, baseAtk, baseAcc, string,  mod, modString, magAtk,
                skipToFront, waitForHit, waitForNextTurn, multHit, multTarget,
                targetLoseTurn, absorb, status, element, sp]

class Equipment(Item):

    def enableEffect(self, character):
        pass

    def disableEffect(self, character):
        pass

    def levelUp(self):
        pass
