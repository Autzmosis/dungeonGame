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
        kwargs['screen'].refocus()
        string = kwargs['string']
        inputs = string.lower().split()
        kwargs['string'] = inputs
        screenName = kwargs['screen'].name
        screenName = kwargs['screen'].name
        self.function = kwargs['screen'].responce
        if 'gamescreen' == screenName:
            self.gameScreenInputHandler(kwargs)
        else:
            self.function(kwargs)

    def gameScreenInputHandler(self, kwargs):
        if 'upStat' in self.modes:
            kwargs['screen'].usr.confirmUpgradeStat(kwargs['string'])
        elif 'battle' in self.modes:
            if kwargs['screen'].pressEnter:
		if kwargs['screen'].usr.permission:
		    kwargs['screen'].usr.permission = False
		    print 'Oh no bro'
                kwargs['screen'].pressEnter = False
                kwargs['screen'].arena.start()
            elif kwargs['string']:
                kwargs['screen'].goCheckEm(kwargs['string'])
        elif 'story' in self.modes:
            pass
        elif 'dungeon' in self.modes:
            pass
        else:
            self.function(kwargs)
