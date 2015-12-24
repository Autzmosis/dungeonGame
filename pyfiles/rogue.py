#! /usr/bin/python2
#coding=utf-8

"""
Yet to be named dungeonGame
by EncodedPixel
coded by タダノデーモン(tadanodaemon)

This program contains the Rogue class
"""

from charANPC import Character

class Rogue(Character):
    
    def __init__(self, data):
        super(Rogue, self).__init__(data)
        self.stats = {
            'hp': 22,
            'sp': 13,
            'atk': 10,
            'def': 5,
            'ma': 10,
            'md': 5,
            'lck': 15,
            'spe': 15,
            'exp': 0,
            'gol': 0
            }
        self.atkList = [
                'shank',
                'smokescreen',
                'backstab',
                'throw'
                ]
        self.atkDict = {
                'check': self.atkListCheck,
                'shank': self.regAtk,
                'smokescreen': self.smokescreen,
                'backstab': self.backstab,
                'throw': self.throw
                }

    def smokescreen(self):
        baseAtk = 0
        baseAcc = 90
        mod = {'acc': .7}
        modString = 'accuracy lowered.'
        string = self.info['name'] + ' used smokescreen'
        return [baseAtk, baseAcc, string, mod, modString]
            
    def backstab(self):
        baseAtk = 7
        baseAcc = 90
        mod = {'def': .7}
        modString = 'defense lowered'
        string = self.info['name'] + ' used backstab'
        return [baseAtk, baseAcc, string, mod, modString, False]
            
    def throw(self):
        baseAtk = 5
        baseAcc = 90
        mod = {}
        modString = ''
        string = self.info['name'] + ' used throw'
        return [baseAtk, baseAcc, string, mod, modString, False]
