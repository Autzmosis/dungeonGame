#! /usr/bin/python2
#coding=utf-8

'''
Yet to be named dungeon game
coded by タダノデーモン(tadanodaemon)

This file holds the item class  and equipment class
and all defined items
'''
def makeItem(name):

    itemDict = {
            'herbs': [
                'item',
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
                ]
            }

    class Item(object):

        def __init__(self, name):
            self.name = name
            self.descripComponents = itemDict[self.name][1]
            self.effect = itemDict[self.name][2]
            self.sellPrice = itemDict[self.name][3]
            self.buyPrice = itemDict[self.name][4]
            self.quantity = 1
            self.makeDescrip()

        def makeDescrip(self):
            first, last = self.descripComponents
            self.descrip = first + str(self.quantity) + last

        def transmutate(self, newName):
            return makeItem(newName)

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

    class Weapon(Equipment):

        def __init__(self, name):
            addedAtks = itemDict[self.name][5] #dict of atks and what they do similiar to effect but more nested
            self.atkList = []
            self.atkDict = {}
            for a in addedAtks:
                self.atkList.append(a)
                self.atkDict[a] == self.convertToAttack(addedAtks[a])
            self.upStats = itemDict[self.name][6]
            self.upExp = itemDict[self.name][7]
            self.exp = 0
            self.lvl = 1

        def levelUp(self):
            pass

    if itemDict[name][0] == 'item':
        return Item(name)
    elif itemDict[name][0] == 'equip':
        return Equipment(name)
    elif itemDict[name][0] == 'weapon':
        return Weapon(name)
