#! /usr/bin/python2
#coding=utf-8

"""
Yet to be named dungeonGame
by EncodedPixel
coded by タダノデーモン(tadanodaemon)

This file holds the script used to add story to the game
"""

from kivy.storage.jsonstore import JsonStore
data = JsonStore('data.json')

class addStory(object):
    '''
    This class is used for adding story to the game

    Syntax for the story is a key based dictionary, these keys are hexadacimal numbers
    that will be used to track progress. Starting point is 1, so if scenario 1 had 3
    possible options then there would be 11, 12, and 13. If 13 had 2 options then it would
    be 131, and 132. This will continue until there is a string of 16 characters

    basic syntax: {key
    '''

    def __init__(self):
        self.File = raw_input("Which story would you like to edit?\n\n").lower()
        self.data = JsonStore(self.File + '.json')
        self.start = 1 #default start code
        if self.data.count(): #If file has been started
            print '\nLooking for where you left off...\n'
            keys = self.data.keys()
            leftOff = int(keys[len(keys) - 1])
            print ('It seems like you left off at event number'
                    ' %d, so let\'s move on to number %d.'
                    % (leftOff, leftOff + 1)
                    )
            self.start = leftOff
        self.addToDBLoop(self.start)

    def addToDBLoop(self, number):
        event = raw_input('What is event number %d?\n' % number).lower()
        optionsStr = raw_input(('What are the available options for player?\n'
            'If none just type \'none\'.\n')).lower().split()
        c = 0
        options = {}
        for o in optionsStr:
            c += 1
            options[o] = str(number) + str(c)
        self.data.put(str(number), event = event, options = options)

if __name__ == '__main__':
    addStory = addStory()
