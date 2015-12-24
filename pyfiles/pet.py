#! /usr/bin/python2
#coding=utf-8

"""
Yet to be named dungeonGame
by EncodedPixel
coded by タダノデーモン(tadanodaemon)

This program contains the basic Pet class for all pets
"""

from charANPC import *

class Pet(ANPC):

    def __init__(self, data):
        super(Pet, self).__init__()
        self.aliance = 'player'
        self.info = {'name': 'pet'}
        pass

    def grow(self):
        pass

    
