#! /usr/bin/python2
#coding=utf-8

"""
Yet to be named dungeonGame
by EncodedPixel
coded by タダノデーモン(tadanodaemon)

This program will contain all the class used for Text Recognition
"""

class TextRecognition(object):

    def __init__(self):
        self.modes = []
        self.function = None

    def inputHandler(self, **kwargs):
        string = kwargs['string']
        inputs = string.lower().split()
        kwargs['string'] = inputs
        if 'screen' in kwargs:
            self.function = kwargs['screen'].responce
        if 'gamescreen' in self.modes:
            self.gameScreenInputHandler(kwargs)
        elif 'battlescreen' in self.modes:
            self.battleScreenInputHandler(kwargs)
        else:
            self.function(kwargs)

    def gameScreenInputHandler(self, kwargs):
        if 'upStat' in self.modes:
            kwargs['screen'].usr.confirmUpgradeStat(kwargs['string'])
        elif 'story' in self.modes:
            pass
        elif 'dungeon' in self.modes:
            pass
        else:
            self.function(kwargs)

    def battleScreenInputHandler(self, kwargs):
        pass
