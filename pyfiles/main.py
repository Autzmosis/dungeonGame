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
from kivy.uix.boxlayout import BoxLayout
#from kivy.uix.floatlayout import FloatLayout
#from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput
from kivy.core.text import LabelBase
#from kivy.uix.image import AsyncImage
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from threading import Thread
from time import sleep
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from kivy.graphics import *
from kivy.storage.jsonstore import JsonStore
from kivy.core.audio import SoundLoader
from rogue import Rogue
from mage import Mage
from warrior import Warrior
from arena import *

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
    c = 0

    def __init__(self, **kwargs):
        super(ChooseClass, self).__init__(**kwargs)
        self.string = ''
        self.c = 0 #used so i can ask player their name
        self.info = {}
        self.trigger = Clock.create_trigger(self.refocus_text)
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

    def __on_enter__(self, usrinput, hint, image=()):
        """
        this function is used for text recognition features
        """
        if self.c == 0:
            for x in range(0, len(usrinput.text) + 1):
                if usrinput.text[x:x+5].lower() == 'rogue':
                    self.info['class'] = 'rogue'
                    self.info['image'] = image[0].source
                    usrinput.text = ''
                    hint.text = 'By the way, what might your name be?'
                    self.c = 1
                    self.trigger()
                    break
                elif usrinput.text[x:x+7].lower() == 'warrior':
                    self.info['class'] = 'warrior'
                    self.info['image'] = image[1].source
                    usrinput.text = ''
                    hint.text = 'By the way, what might your name be?'
                    self.c = 1
                    self.trigger()
                    break
                elif usrinput.text[x:x+4].lower() == 'mage':
                    self.info['class'] = 'mage'
                    self.info['image'] = image[2].source
                    usrinput.text = ''
                    hint.text = 'By the way, what might your name be?'
                    self.c = 1
                    self.trigger()
                    break
                elif x == len(usrinput.text):
                    usrinput.text = ''
                    hint.text = 'Please choose one of the classes above.'
                    self.trigger()
        else:
            self.getName(usrinput, hint)

    def getName(self, usrinput, hint):
        if usrinput.text != '':
            self.info['name'] = usrinput.text
            usrinput.text = ''
            hint.text = 'Type name of class and press enter'
            self.setupPlayer()
            self.fadeOut('gamescreen')
            self.c = 0
            self.trigger()
        else:
            hint.text = 'Unresponsive, are we? Well it takes two to tango!'
            self.trigger()

    def setupPlayer(self):
        if self.info['class'] == 'rogue':
            player = Rogue(self.manager.get_screen('gamescreen'))
        elif self.info['class'] == 'warrior':
            player = Warrior(self.manager.get_screen('gamescreen'))
        elif self.info['class'] == 'mage':
            player = Mage(self.manager.get_screen('gamescreen'))
        player.info = self.info
        player.updateBase()

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
    atkList = ObjectProperty(None)
    inventory = ObjectProperty(None)
    box = []
    c = 0

    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        with self.canvas:
            self.color = Color(0,0,0,1)
            self.rect = Rectangle(size = self.size)
        self.string = ''
        self.trigger = Clock.create_trigger(self.refocus_text)
        self.data = data
        self.original = [self.atkList.text, self.inventory.text]

    def fade(self, dt):
        if self.color.a == 1:
            anim = Animation(a = 0, duration = 2.)
            anim.start(self.color)
            self.color.a == 0
        
    def on_enter(self):
        global player
        self.trigger()
        trigfade = Clock.create_trigger(self.fade)
        trigfade()
        Clock.schedule_once(self.welcome, 2)
        if player is None:
            self.setupPlayer()
        self.image.source = player.info['image']
        self.updateSmallStats()
        self.updateAtkList()
        self.updateInventory()

    def setupPlayer(self):
        global player
        if data.get('player')['info']['class'] == 'rogue':
            player = Rogue(self)
        elif data.get('player')['info']['class'] == 'mage':
            player = Mage(self)
        elif data.get('player')['info']['class'] == 'warrior':
            player = Warrior(self)
        player.updateSelf()

    def __on_enter__(self, *largs, **kwargs):
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
            self.atkList.text = self.original[0]
            self.inventory.text = self.original[1]
            self.fadeOut('title')
        elif self.usr.text.lower() == 'battle':
            self.usr.text = ''
            self.trigger()
            main(player, self)
        elif self.usr.text.lower() == 'sammy is a fag':
            self.textinput.text += '\n>_ ' + self.usr.text
            self.usr.text = ''
            sleep(.25)
            self.prompt('I know right!')
            self.usr.readonly = False
            self.trigger()
        elif self.usr.text.lower() == 'but richard is cool right':
            self.textinput.text += '\n>_ ' + self.usr.text
            self.usr.text = ''
            sleep(.25)
            self.prompt('no, he is a fag too.')
            self.usr.readonly = False
            self.trigger()
        elif self.usr.text.lower() == 'what':
            self.textinput.text += '\n>_ ' + self.usr.text
            self.usr.text = ''
            sleep(.25)
            self.prompt('i meant what i said!')
            self.usr.readonly = False
            self.trigger()
        elif self.usr.text.lower() == 'what about paul':
            self.textinput.text += '\n>_ ' + self.usr.text
            self.usr.text = ''
            sleep(.25)
            self.prompt('he\'s even worse!')
            self.usr.readonly = False
            self.trigger()
        elif self.usr.text.lower() != '':
            self.textinput.text += '\n>_ ' + self.usr.text
            self.usr.text = ''
            sleep(.25)
            thread = Thread(None, self.prompt, 'thread',
                            args=['I be test prompt.'])
            thread.daemon = True
            thread.start()
            self.usr.readonly = False
            self.trigger()
        else:
            self.trigger()
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
        self.usr.readonly = False
    
    def prompt(self, string, **kwargs):
        """
        this breaks up typed string into a box and packages each letter
        for shipping to the screen :]
        """
        self.box = []
        substring = ''
        if string[:2] == '>_':
            substring = string[2:]
        if substring != '':
            for x in substring:
                self.box.append(x)
        else:
            for x in string:
                self.box.append(x) 
        if self.textinput.text == '':
            self.textinput.text += '>>> '
            self.prompt_send('dt')
        elif string  == '\n':
            self.textinput.text += '\n'
        elif string[:2]  == '>_':
            self.textinput.text += '\n>_ '
            self.prompt_send('dt')
        else:
            self.textinput.text += '\n>>> '
            self.prompt_send('dt')
            
    def prompt_send(self, dt):
        """
        this ships each given letter to the screen
        """
        sleep(.03)
        self.textinput.text += self.box[self.c]
        self.c += 1
        if self.c == len(self.box):
            self.c = 0
            return False
        else:
            self.prompt_send('dt')

    def updateSmallStats(self):
        newHP = player.stats['hp']
        newSP = player.stats['sp']
        hp = player.stats['fullHP']
        sp = player.stats['fullSP']
        name = player.info['name']
        self.label.text = '[b]%s[/b]:\nhp: %d/%d\nsp: %d/%d' %(name, newHP, hp, newSP, sp)

    def updateAtkList(self):
        for x in player.atkList:
            self.atkList.text = self.atkList.text + x + '\n'

    def updateInventory(self):
        inv = data.get('player')['inventory']
        if inv != {}:
            for x in inv:
                self.inventory.text = self.inventory.text + x + '\n'
        else:
            self.inventory.text = self.inventory.text + 'None'

    def updateObjective(self):
        pass

class UsrInput(TextInput):

    textinput = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(UsrInput, self).__init__(**kwargs)
        self.permission = False
        self.storyMode = False
        self.tF = True

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        global player
        keyNum, keyStr = keycode
        if keyStr in ('up', 'down'):
            if keyStr == 'up':
                self.textinput.focus = True
                self.textinput.do_cursor_movement(
                        'cursor_pgup',
                        control = False,
                        alt = False
                        )
                self.textinput.focus = False
                self.focus = True
            if keyStr == 'down':
                self.textinput.focus = True
                self.textinput.do_cursor_movement(
                        'cursor_pgdown',
                        control = False,
                        alt = False
                        )
                self.textinput.focus = False
                self.focus = True
        elif keyStr in ('1', '2', '3', '4', '5') and self.permission:
            player.checkEm(int(keyStr) - 1, self.tF)
        elif keyStr == 'enter' and self.storyMode:
            pass
        else:
            super(UsrInput, self).keyboard_on_key_down(window, keycode, text, modifiers)

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

if __name__ == '__main__':
    player = None
    data = JsonStore('data.json')
    audio = SoundLoader()
    app = DungeonGame()
    app.run()
