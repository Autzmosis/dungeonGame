#! /usr/bin/python2
#coding=utf-8

"""
Yet to be named dungeonGame
by EncodedPixel
coded by タダノデーモン(tadanodaemon)

This program conatins the Mage class
"""

from charANPC import Character

class Mage(Character):

    def __init__(self, data):
        super(Mage, self).__init__(data)
        self.stats = {
                'hp': 19,
                'sp': 16,
                'atk': 5,
                'def': 10,
                'ma': 15,
                'md': 15,
                'lck': 5,
                'spe': 10,
                'exp': 0,
                'gol': 0
                }
        self.atkList = [
                'knock',
                'magic blast',
                'summon',
                'cure'
                ]
        self.atkDict = {
                'check': self.atkListCheck,
                'knock': self.regAtk,
                'magic blast': self.magicBlast,
                'summon': self.summon,
                'cure': self.cure
                }

    def magicBlast(self):
        baseAtk = 7
        baseAcc = 90
        string = self.info['name'] + ' used magic blast'
        mod = {}
        modString = ''
        return [baseAtk, baseAcc, string, mod, modString, True]
            
    def summon(self):
        baseAtk = 5
        baseAcc = 90
        string = self.info['name'] + ' used summon'
        mod = {}
        modString = ''
        magAtk = True
        return [baseAtk, baseAcc, string, mod, modString, magAtk]
            
    def cure(self):
        baseAtk = 5
        baseAcc = 90
        string = self.info['name'] + ' used cure'
        mod = {}
        modString = ''
        return [baseAtk, baseAcc, string, mod, modString, False]
