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
        self.mode = ''
        self.keyWords = {
                'verbs': (
                    'look',
                    'enter',
                    (
                        'take',
                        'pickup',
                        'pick'
                        ),
                    (
                        'run',
                        'walk',
                        'skip',
                        'jog',
                        'go',
                        'move'
                        ),
                    'open',
                    'attack',
                    'kill',
                    'ignore',
                    'talk',
                    'read',
                    'follow',
                    'help',
                    (
                        'examine',
                        'inspect'
                        ),
                    'save',
                    'quit'
                    ),
                'directions': (
                    'north',
                    'south',
                    'east',
                    'west',
                    'northeast',
                    'northwest',
                    'southeast',
                    'southwest'
                    ),
                'directors': (
                    'at',
                    'to',
                    'towards',
                    'under',
                    'on top',
                    'down',
                    'up',
                    'around'
                    ),
                'question': (
                    'who',
                    'what',
                    'when',
                    'where',
                    'why',
                    'how'
                    ),
                'connectors': (
                    'and',
                    ),
                'pointers': (
                    'the',
                    'a'
                    ),
                'misc': (
                    'fuck',
                    'shit',
                    'damn',
                    'hell',
                    'bitch',
                    'goddamn',
                    'faggot',
                    'nigga',
                    (
                        'hello',
                        'hi'
                        )
                    )
                }

    def inputHandler(self, **kwargs):
        kwargs['screen'].refocus()
        string = kwargs['string']
        inputs = string.lower().split()
        screen = kwargs['screen']
        screenName = screen.name
        function = screen.responce
        if 'gamescreen' == screenName:
            self.gameScreenInputHandler(screen, inputs, function)
        else:
            function(inputs)

    def gameScreenInputHandler(self, screen, inputs, function):
        if 'battle' == self.mode:
            if screen.pressEnter:
		if screen.usr.permission:
		    screen.usr.permission = False
                screen.pressEnter = False
                screen.arena.start()
            elif inputs != []:
                screen.goCheckEm(inputs)
        else:
            function(inputs)

    def searchKWDB(self, word):
        for kW in self.keyWords:
            for v in self.keyWords[kW]:
                if word == v:
                    return True
                elif isinstance(v, tuple) and word in v:
                    return True
        return False

    def makeKWSentence(self, inputs):
        kWSentence = []
        #isObject = False
        #lastWord = ''
        for i in inputs:
            #if isObject:
            #    kWSentence.append(i)
            #    isObject = False
            #    continue
            #elif i in self.keyWords['pointers']:
            #    isObject = True
            #    continue
            if self.searchKWDB(i):
                kWSentence.append(i)
            #    lastWord = i
        return kWSentence
