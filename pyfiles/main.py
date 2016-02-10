#! /usr/bin/python2
#coding=utf-8

"""
Yet to be named dungeonGame
by EncodedPixel
coded by タダノデーモン(tadanodaemon)

This file holds all of the GUI information for the game. By all of the info,
i mean the functionality information for the GUI(what happens when user presses
enter, etc). For the positioning of the GUI, see dungeongame.kv
"""

import kivy
kivy.require('1.9.1')

#set up window
from kivy.config import Config
Config.set('graphics','fullscreen', 1)
Config.set('graphics','height', 480)
Config.set('graphics','width', 640)
Config.set('graphics','resizable', 0)
Config.set('input', 'mouse', 'none')

#import necessary modules
from kivy.app import App
from kivy.core.text import LabelBase
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from kivy.graphics import *
from kivy.storage.jsonstore import JsonStore
from kivy.core.audio import SoundLoader
from textRecognition import TextRecognition
from time import time

LabelBase.register(name='Pixel',
                   fn_regular='../fonts/slkscr.ttf',
                   fn_bold='../fonts/slkscrb.ttf')

class FadeScreen(Screen):

    def __init__(self, **kwargs):
        super(FadeScreen, self).__init__(**kwargs)
        self.opacity = 0
        self.inAndOut = Animation(opacity = 1, duration = 2.5) + Animation(
                opacity = 0,
                duration = 2.5)
        self.In = Animation(opacity = 1, duration = 2.)
        self.Out = Animation(opacity = 0, duration = 2.)
        self.trigSplashFade = Clock.create_trigger(self.splashFade)
        self.refocus = Clock.create_trigger(self.refocus_text)
        self.trigFadeIn = Clock.create_trigger(self.fadeIn)
        self.dc = 0 #double check
        self.string = '' #this string is used to switch between screens

    def splashFade(self, dt):
        """
        This does what the name says, it fades in to the current screen
        and fades out
        """
        if not self.opacity:
            self.inAndOut.start(self)
            self.inAndOut.on_complete(Clock.schedule_interval(self.splashTransit, 1/60))

    def fadeIn(self, dt):
        if not self.opacity:
            self.In.start(self)

    def fadeOut(self, screen):
        self.string = screen
        if self.opacity:
            self.Out.start(self)
            self.Out.on_complete(Clock.schedule_interval(self.regTransit, 1/60))

    def regTransit(self, dt):
        if not self.opacity:
            self.manager.current = self.string
            return False
        
    def splashTransit(self, dt):
        """
        this allows the fade method to not only fade in, but also fade out
        and go to the next screen after animation is complete
        """
        if self.opacity or self.dc: #here is where the dc comes in handy
            self.dc = 1
            if not self.opacity:
                self.manager.current = 'title'
                self.dc = 0
                return False

    def refocus_text(self, dt):
        self.usr.focus = True
        self.usr.text = ''
        self.usr.readonly = False

class SplashScreen(FadeScreen):
    """
    This is the splash screen that will display the team name and logo,
    until we create the name and logo, my logo stays.
    """

    def __init__(self, **kwargs):
        super(SplashScreen, self).__init__(**kwargs)

    def on_pre_enter(self):
        """
        This method is executed when the screen is about to be transitioned
        too, or on window creation. It just fades to the screen.
        """
        self.trigSplashFade()


class TitleScreen(FadeScreen):
    """
    This is the title screen, it has one text input, so it needs to have access
    to it, to detect player input, just like every other screen, it has
    a fadein, fadeout, on_pre_enter, transit, and refocus_text method.
    """
    
    usr = ObjectProperty(None)
    hint = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(TitleScreen, self).__init__(**kwargs)
        self.c = 0 #This is here to ask the user for confirmation

    def responce(self, inputs):
        """
        this function is called when player presses enter, it validates the
        text and does something, depending on what was typed.
        """
        strings = inputs
        if not self.c:
            if ('new' and 'game') in strings:
                if data.count():
                    self.hint.text = 'Looks, like you\'ve done this before. Are you sure you want to restart?'
                    self.c = 1
                else:
                    self.hint.text = 'Your story is about to begin.'
                    self.fadeOut('chooseclass')
            elif 'continue' in strings:
                if not data.count():
                    self.hint.text = 'You must begin before you can continue!\nType \'new game\' and press enter.'
                else:
                    self.hint.text = 'Welcome back!'
                    self.fadeOut('gamescreen')
            else:
                self.hint.text = 'Please type either \'new game\' or \'continue\'.'
        else:
            self.confirmRestart(strings)
        self.refocus()

    def confirmRestart(self, strings):
        global data
        self.c = 0
        for string in strings:
            if string in ('yes', 'yeah', 'ye', 'y', 'sure', 'ya', 'yup'):
                self.hint.text = 'Your story is about to begin.'
                if data.exists('game'):
                    data.delete('game')
                self.fadeOut('chooseclass')
                return
            elif string in ('no', 'nah', 'nope', 'n'):
                self.hint.text = 'Type \'new game\' or \'continue\' and press enter.'
                return
        self.c = 1
        self.hint.text = 'You mind answering my yes or no question?!'

    def on_pre_enter(self):
        self.refocus()
        self.trigFadeIn()
        self.hint.text = 'Type \'new game\' or \'continue\' and press enter.'

class Void(App):
    """
    this is the actual instance of the app, doesn't do much
    but set up the screens and screenmanager
    """

    def __init__(self, **kwargs):
        super(Void, self).__init__(**kwargs)
        self.textRec = TextRecognition()
        self.beginTime = 0

    def startWatch(self):
        self.beginTime = time()

    def stopWatch(self):
        global data
        totalTime = time() - self.beginTime
        if data.exists('game'):
            totalTime += data.get('game')['time']
        return totalTime

    def build(self):
        self.title = 'Dungeons and Towns'
        sm = ScreenManager()
        #sm.add_widget(SplashScreen(name = 'splash'))
        sm.add_widget(TitleScreen(name = 'title'))
        return sm

if __name__ == '__main__':
    player = None
    data = JsonStore('data.json')
    audio = SoundLoader()
    typing = audio.load('../audio/typingSound.wav')
    typing.loop = True
    app = Void()
    app.run()
