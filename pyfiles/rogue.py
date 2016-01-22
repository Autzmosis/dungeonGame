#! /usr/bin/python2
#coding=utf-8

"""
Yet to be named dungeonGame
by EncodedPixel
coded by タダノデーモン(tadanodaemon)

This program contains the Rogue class
"""

from random import *

class Rogue(object):
    
    def __init__(self, atk):
	self.regAtk = atk
        self.special = ['random', self.dualBlitz, 'Dual Blitz']
        self.stats = {
            'hp': 1,
            'sp': 1,
            'fullHP': 1,
            'fullSP': 1,
            'atk': 1,
            'def': 1,
            'ma': 1,
            'md': 1,
            'lck': 1,
            'spe': 1,
            'exp': 0,
            'gol': 0,
            'elem': ['none']
            }
	self.upStats = {
                'fullHP': [1, -.45, 93.3, -70],
                'fullSP': [1, -.044, 9.1, 5],
                'atk': [1, -.011, 2.3, 11.5],
                'def': [1, -.009, 2, 5],
                'ma': [1, -.009, 2.05, 10],
                'md': [1, -.009, 2.1, 7.3],
                'lck': [1, -.007, 1.57, 13.03],
                'spe': [1, -.007, 1.58, 13.03],
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

    def dualBlitz(self, targetInfo):
        '''
        This is the rogue's special ability
        '''
	if targetInfo[1]:
        	targetInfo[3] += '\n-->%s\'s dual blitz activated!' %(self.info['name'])
        	targetInfo[10] = [1, 2, 'here is the second!']
        	targetInfo[16] = 0
        return targetInfo

    def smokescreen(self, target):
        baseAtk = 0
        baseAcc = 90
        string = '%s used smokescreen!' %(self.info['name'])
        mod = {'acc': .7}
        modString = '%s\'s accuracy lowered.' %(target)
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
        sp = 2
        return [target, baseAtk, baseAcc, string,  mod, modString, magAtk,
                skipToFront, waitForHit, waitForNextTurn, multHit, multTarget,
                targetLoseTurn, absorb, status, element, sp]
            
    def backstab(self, target):
        baseAtk = 85
        baseAcc = 90
        string = self.info['name'] + ' used backstab!'
        mod = {'def': .7}
        modString = '%s\'s defense lowered.' % target
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
        sp = 3
        return [target, baseAtk, baseAcc, string,  mod, modString, magAtk,
                skipToFront, waitForHit, waitForNextTurn, multHit, multTarget,
                targetLoseTurn, absorb, status, element, sp]
            
    def shadeThrust(self, target):
        baseAtk = 95
        baseAcc = 70
        string = self.info['name'] + ' used shade thrust!'
        mod = {}
        modString = ''
        magAtk = True
        skipToFront = [0]
        waitForHit = [0]
        waitForNextTurn = [0]
        multHit = [0]
        multTarget = None
        targetLoseTurn = [0]
        absorb = [0]
        status = [0]
        element = ['dark']
        sp = 5
        return [target, baseAtk, baseAcc, string,  mod, modString, magAtk,
                skipToFront, waitForHit, waitForNextTurn, multHit, multTarget,
                targetLoseTurn, absorb, status, element, sp]
