#! /usr/bin/python2
#coding=utf-8

"""
Yet to be named dungeonGame
by EncodedPixel
coded by タダノデーモン(tadanodaemon)

This program contains the Rogue class
"""

from charANPC import Character
from random import *

class Rogue(Character):
    
    def __init__(self, gui):
        super(Rogue, self).__init__(gui)
        self.stats = {
            'hp': 22,
            'sp': 13,
            'fullHP': 22,
            'fullSP': 13,
            'atk': 10,
            'def': 5,
            'ma': 10,
            'md': 5,
            'lck': 15,
            'spe': 15,
            'exp': 0,
            'gol': 0,
            'elem': ['none']
            }
        self.atkList = [
                'shank',
                'smokescreen',
                'backstab',
                'shade thrust'
                ]
        self.setTarget = [
                ]
        self.atkDict = {
                'shank': self.regAtk,
                'smokescreen': self.smokescreen,
                'backstab': self.backstab,
                'shade thrust': self.shadeThrust
                }

    def smokescreen(self, target):
        baseAtk = 0
        baseAcc = 90
        mod = {'acc': .7}
        modString = '%s\'s accuracy lowered.' %(target)
        string = '%s used smokescreen!' %(self.info['name'])
        magAtk = False
        skipToFront = [0]
        waitForHit = [0]
        waitForNextTurn = [0]
        multHit = [0]
        multTarget = [None]
        targetLoseTurn = [0]
        element = ['none']
        sp = 2
        return [target, baseAtk, baseAcc, string,  mod, modString, magAtk,
                skipToFront, waitForHit, waitForNextTurn, multHit, multTarget,
                targetLoseTurn, element, sp]
            
    def backstab(self, target):
        baseAtk = 7
        baseAcc = 90
        mod = {'def': .7}
        modString = target + ' defense lowered.'
        string = self.info['name'] + ' used backstab!'
        magAtk = False
        skipToFront = [0]
        waitForHit = [0]
        waitForNextTurn = [0]
        multHit = [0]
        multTarget = [None]
        targetLoseTurn = [0]
        element = ['none']
        sp = 3
        return [target, baseAtk, baseAcc, string,  mod, modString, magAtk,
                skipToFront, waitForHit, waitForNextTurn, multHit, multTarget,
                targetLoseTurn, element, sp]
            
    def shadeThrust(self, target):
        baseAtk = 7
        baseAcc = 70
        mod = {}
        modString = ''
        string = self.info['name'] + ' used shade thrust!'
        magAtk = True
        skipToFront = [0]
        waitForHit = [0]
        waitForNextTurn = [0]
        multHit = [0]
        multTarget = [None]
        targetLoseTurn = [0]
        element = ['dark']
        sp = 5
        return [target, baseAtk, baseAcc, string,  mod, modString, magAtk,
                skipToFront, waitForHit, waitForNextTurn, multHit, multTarget,
                targetLoseTurn, element, sp]
