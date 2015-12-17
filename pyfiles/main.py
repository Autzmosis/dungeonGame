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
Config.set('graphics','fullscreen', 0)
Config.set('graphics','height', 480)
Config.set('graphics','width', 640)
Config.set('graphics','show_cursor', 1)
Config.set('graphics','resizable', 0)

#import necessary modules
from kivy.app import App
#from kivy.uix.label import Label
#from kivy.uix.boxlayout import BoxLayout
#from kivy.uix.floatlayout import FloatLayout
#from kivy.uix.relativelayout import RelativeLayout
#from kivy.uix.textinput import TextInput
from kivy.core.text import LabelBase
from kivy.uix.image import AsyncImage
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from threading import Thread
from time import sleep
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from kivy.graphics import *

LabelBase.register(name='Pixel',
                   fn_regular='../fonts/slkscr.ttf',
                   fn_bold='../fonts/slkscrb.ttf')

class SplashScreen(Screen):
    """
    This is the splash screen that will display the team name and logo,
    until we create the name and logo, my logo stays.
    """

    def __init__(self, **kwargs):
        super(SplashScreen, self).__init__(**kwargs)
        self.dc = 0 #double check
        with self.canvas: #set up blackscreen
            self.color = Color(0,0,0,1)
            self.rect = Rectangle(size = self.size)

    def on_pre_enter(self):
        """
        This method is executed when the screen is about to be transitioned
        too, or on window creation. It just fades to the screen.
        """
        trigfade = Clock.create_trigger(self.fade)
        trigfade()

    def fade(self, dt):
        """
        This does what the name says, it fades in to the current screen
        and fades out
        """
        if self.color.a == 1:
            anim = Animation(a = 0, duration = 5.) + Animation(a = 1,
                                                              duration = 5.)
            anim.start(self.color)
            anim.on_complete(Clock.schedule_interval(self.transit, 1/60))

    def transit(self, dt):
        """
        this allows the fade method to not only fade in, but also fade out
        and go to the next screen after animation is complete
        """
        if self.color.a == 0 or self.dc == 1: #here is where the dc comes in handy
            self.dc = 1
            if self.color.a == 1:
                self.manager.current = 'title'
                return False

class TitleScreen(Screen):
    """
    This is the title screen, it has one text input, so it needs to have access
    to it, to detect player input, just like every other screen, it has
    a fadein, fadeout, on_pre_enter, transit, and refocus_text method.
    """
    
    usr = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(TitleScreen, self).__init__(**kwargs)
        self.string = '' #this string is used to switch between screens
        with self.canvas:
            self.color = Color(0,0,0,1)
            self.rect = Rectangle(size = self.size)

    def fade(self, dt):
        if self.color.a == 1:
            anim = Animation(a = 0, duration = 3.)
            anim.start(self.color)
        
    def __on_enter__(self, usrinput, hint, app):
        """
        this function is called when player presses enter, it validates the
        text and does something, depending on what was typed.
        """
        for x in range(0, len(usrinput.text) + 1):
            if usrinput.text[x:x+8].lower() == 'new game':
                usrinput.text = ''
                self.fadeOut('chooseclass')
                break
            elif usrinput.text[x:x+8].lower() == 'continue':
                usrinput.text = ''
                self.fadeOut('gamescreen')
                self.parent.get_screen('gamescreen').image.source = '../media/rogue.png'
                self.parent.get_screen('gamescreen').label.text = 'rogue' + self.parent.get_screen('gamescreen').label.text
                break
            elif x == len(usrinput.text):
                usrinput.text = ''
                hint.text = 'Please type either \'new game\' or \'continue\'.'
                trigger = Clock.create_trigger(self.refocus_text)
                trigger()

    def fadeOut(self, screen):
        self.string = screen
        if self.color.a == 0:
            anim = Animation(a = 1, duration = 3.)
            anim.start(self.color)
            anim.on_complete(Clock.schedule_interval(self.transit, 1/60))

    def transit(self, dt):
        if self.color.a == 1:
            self.manager.current = self.string
            return False

    def refocus_text(self, dt):
        self.usr.focus = True

    def on_pre_enter(self):
        trigger = Clock.create_trigger(self.refocus_text)
        trigger()
        trigfade = Clock.create_trigger(self.fade)
        trigfade()

class ChooseClass(Screen):
    
    """
    This class allows the player to choose there character for the
    first time, thus it needs text recognition capabilities. Just
    like every other screen, it has a fadein, fadeout, on_pre_enter,
    transit, and refocus_text method.
    """
    usr = ObjectProperty(None)
    rogue = ObjectProperty(None)
    mage = ObjectProperty(None)
    warrior = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ChooseClass, self).__init__(**kwargs)
        self.string = ''
        with self.canvas:
            self.color = Color(0,0,0,1)
            self.rect = Rectangle(size = self.size)

    def fade(self, dt):
        if self.color.a == 1:
            anim = Animation(a = 0, duration = 3.)
            anim.start(self.color)
        if self.color.a == 0:
            anim = Animation(a = 1, duration = 3.)
            anim.start(self.color)
        
    def lightUp(self, dt):
        """
        this lights up the class box of the class
        the user is typing. Still working on it
        """
        for x in range(0, len(self.usr.text) + 1):
            if self.usr.text[x:x+5].lower() == 'rogue':
                self.rogue.color = (1,1,0,1)
            elif self.usr.text[x:x+7].lower() == 'warrior':
                self.warrior.color = (1,1,0,1)
            elif self.usr.text[x:x+4].lower() == 'mage':
                self.mage.color = (1,1,0,1)

    def __on_enter__(self, usrinput, app, hint, image=()):
        """
        this function is used for text recognition features
        """
        for x in range(0, len(usrinput.text) + 1):
            if usrinput.text[x:x+5].lower() == 'rogue':
                self.parent.get_screen('gamescreen').image.source = image[0].source
                self.parent.get_screen('gamescreen').label.text = 'rogue' + self.parent.get_screen('gamescreen').label.text
                usrinput.text = ''
                Clock.unschedule(self.lightUp)
                self.fadeOut('gamescreen')
                break
            elif usrinput.text[x:x+7].lower() == 'warrior':
                self.parent.get_screen('gamescreen').image.source = image[1].source
                self.parent.get_screen('gamescreen').label.text = 'warrior' + self.parent.get_screen('gamescreen').label.text
                usrinput.text = ''
                Clock.unschedule(self.lightUp)
                self.fadeOut('gamescreen')
                break
            elif usrinput.text[x:x+4].lower() == 'mage':
                self.parent.get_screen('gamescreen').image.source = image[2].source
                self.parent.get_screen('gamescreen').label.text = 'mage' + self.parent.get_screen('gamescreen').label.text
                usrinput.text = ''
                Clock.unschedule(self.lightUp)
                self.fadeOut('gamescreen')
                break
            elif x == len(usrinput.text):
                usrinput.text = ''
                hint.text = 'Please choose one of the classes above'
                trigger = Clock.create_trigger(self.refocus_text)
                trigger()

    def fadeOut(self, screen):
        self.string = screen
        if self.color.a == 0:
            anim = Animation(a = 1, duration = 3.)
            anim.start(self.color)
            anim.on_complete(Clock.schedule_interval(self.transit, 1/60))

    def transit(self, dt):
        if self.color.a == 1:
            self.manager.current = self.string
            return False

    def refocus_text(self, dt):
        self.usr.focus = True

    def on_pre_enter(self):
        trigger = Clock.create_trigger(self.refocus_text)
        trigger()
        trigfade = Clock.create_trigger(self.fade)
        trigfade()
        Clock.schedule_interval(self.lightUp, 1/60)

class GameScreen(Screen):
    """
    This is the GameScreen class. This class needs a lot more functionality
    than the other screens, so there are more than a few different methods
    here. Consider this advanced text recognition and config functionality
    """

    textinput = ObjectProperty(None)
    usr = ObjectProperty(None)
    image = ObjectProperty(None)
    label = ObjectProperty(None)
    box = []
    c = 0

    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.original = self.label.text #used to remember what was there before
        self.originalsource = self.image.source #back to screen was typed
        with self.canvas:
            self.color = Color(0,0,0,1)
            self.rect = Rectangle(size = self.size)
        self.string = ''

    def fade(self, dt):
        if self.color.a == 1:
            anim = Animation(a = 0, duration = 2.)
            anim.start(self.color)
            self.color.a == 0
        
    def on_enter(self):
        trigger = Clock.create_trigger(self.refocus_text)
        trigger()
        trigfade = Clock.create_trigger(self.fade)
        trigfade()
        Clock.schedule_once(self.welcome, 2)

    def __on_enter__(self, app):
        """
        this method validates text and sends to prompt
        """
        self.usr.readonly = True
        if self.usr.text.lower() == 'exit':
            app.get_running_app().stop()
        elif self.usr.text.lower() == 'back to start':
            self.usr.text = ''
            self.textinput.text = ''
            self.usr.readonly = False
            self.label.text = self.original
            self.image.source = self.originalsource
            self.fadeOut('title')
        elif self.usr.text != '':
            self.textinput.text += '\n>_ ' + self.usr.text
            self.usr.text = ''
            sleep(.25)
            thread = Thread(None, self.prompt, 'thread',
                            args=['I be test prompt.'])
            thread.daemon = True
            thread.start()
            self.usr.readonly = False
            trigger = Clock.create_trigger(self.refocus_text)
            trigger()
        else:
            trigger = Clock.create_trigger(self.refocus_text)
            trigger()
            self.usr.readonly = False
            return False

    def fadeOut(self, screen):
        self.string = screen
        if self.color.a == 0:
            anim = Animation(a = 1, duration = 3.)
            anim.start(self.color)
            anim.on_complete(Clock.schedule_interval(self.transit, 1/60))

    def transit(self, dt):
        if self.color.a == 1:
            self.manager.current = self.string
            return False
        
    def welcome(self, dt):
        """
        This is here because it is the first string sent to prompt, and 
        does not rely on user pressing enter
        """
        x = 'Welcome to the world of Dungeons and Towns!'
        thread = Thread(None, self.prompt, 'thread', args=[x])
        thread.daemon = True
        thread.start()

    def refocus_text(self, dt):
        self.usr.focus = True
    
    def prompt(self, string, **kwargs):
        """
        this breaks up typed string into a box and packages each letter
        for shipping to the screen :]
        """
        self.box = []
        for x in string:
           self.box.append(x) 
        if self.textinput.text == '':
            self.textinput.text += '>>> '
            Clock.schedule_interval(self.prompt_send, 1/10)
        else:
            self.textinput.text += '\n>>> '
            Clock.schedule_interval(self.prompt_send, 1/10)
            
    def prompt_send(self, dt):
        """
        this ships each given letter to the screen
        """
        self.textinput.text += self.box[self.c]
        self.c += 1
        if self.c == len(self.box):
            self.c = 0
            return False

class DungeonGame(App):
    """
    this is the actual instance of the app, doesn't do much
    but set up the screens and screenmanager
    """

    def __init__(self, **kwargs):
        super(DungeonGame, self).__init__(**kwargs)
        
    def build(self):
        self.title = 'Dungeons and Towns'
        sm = ScreenManager()
        sm.add_widget(SplashScreen(name = 'splash'))
        sm.add_widget(TitleScreen(name = 'title'))
        sm.add_widget(ChooseClass(name = 'chooseclass'))
        sm.add_widget(GameScreen(name = 'gamescreen'))
        return sm

if __name__ == '__main__': DungeonGame().run()
