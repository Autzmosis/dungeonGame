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

kivy.require('1.9.0')

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
from kivy.uix.gridlayout import GridLayout
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.listview import ListItemButton, ListView
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.core.text import LabelBase
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
    hint = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(TitleScreen, self).__init__(**kwargs)
        self.string = '' #this string is used to switch between screens
        self.c = 0 #This is heroe to ask the user for confirmation
        with self.canvas:
            self.color = Color(0,0,0,1)
            self.rect = Rectangle(size = self.size)

    def fade(self, dt):
        if self.color.a == 1:
            anim = Animation(a = 0, duration = 3.)
            anim.start(self.color)
        
    def __on_enter__(self, usrinput, hint):
        """
        this function is called when player presses enter, it validates the
        text and does something, depending on what was typed.
        """
        if not self.c:
            for x in range(0, len(usrinput.text) + 1):
                if usrinput.text[x:x+8].lower() == 'new game':
                    usrinput.text = ''
                    if data.count() != 0:
                        hint.text = 'Looks, like there you\'ve done this before. Are you sure you want to restart?'
                        self.c = 1
                        trigger = Clock.create_trigger(self.refocus_text)
                        trigger()
                    else:
                        hint.text = 'Your story is about to begin.'
                        self.fadeOut('chooseclass')
                    break
                elif usrinput.text[x:x+8].lower() == 'continue':
                    if data.count() == 0:
                        hint.text = 'You must begin before you can continue!\nType \'new game\' and press enter.'
                        usrinput.text = ''
                        trigger = Clock.create_trigger(self.refocus_text)
                        trigger()
                    else:
                        usrinput.text = ''
                        hint.text = 'Welcome back!'
                        self.fadeOut('gamescreen')
                    break
                elif x == len(usrinput.text):
                    usrinput.text = ''
                    hint.text = 'Please type either \'new game\' or \'continue\'.'
                    trigger = Clock.create_trigger(self.refocus_text)
                    trigger()
                    break
        else:
            self.confirmRestart(usrinput, hint)
            trigger = Clock.create_trigger(self.refocus_text)
            trigger()

    def confirmRestart(self, usr, hint):
        if usr.text in ('yes', 'yeah', 'ye', 'y', 'sure'):
            usr.text = ''
            self.c = 0
            hint.text = 'Your story is about to begin.'
            self.fadeOut('chooseclass')
        elif usr.text in ('no', 'nah', 'nope'):
            self.c = 0
            usr.text = ''
            hint.text = 'Type \'new game\' or \'continue\' and press enter.'
        else:
            hint.text = 'You mind answering my yes or no question?!'
            usr.text = ''

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
        self.hint.text = 'Type \'new game\' or \'continue\' and press enter.'

class ChooseClass(Screen):
    
    """
    This class allows the player to choose there character for the
    first time, thus it needs text recognition capabilities. Just
    like every other screen, it has a fadein, fadeout, on_pre_enter,
    transit, and refocus_text method.
    """
    usr = ObjectProperty(None)
    hint = ObjectProperty(None)
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
            hint.text = 'Cool, let\'s get going then.'
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
        self.hint.text = 'Type name of class and press enter'

class GameScreen(Screen):
    """
    This is the GameScreen class. This class needs a lot more functionality
    than the other screens, so there are more than a few different methods
    here. Consider this advanced text recognition and config functionality
    """

    textinput = ObjectProperty(None)
    usr = ObjectProperty(None)
    image = ObjectProperty(None)
    objective = ObjectProperty(None)
    playerLabel = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        with self.canvas:
            self.color = Color(0,0,0,1)
            self.rect = Rectangle(size = self.size)
        self.string = ''
        self.trigger = Clock.create_trigger(self.refocus_text)
        self.data = data
        self.box = []
        self.c = 0
        self.queue = []
        self.isReady = True
        self.startQueue = True
        self.stop = False
        self.cleanUp = False

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
        self.updateEquipment()
        self.updatePlayerInfo()

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
        just for testing out crap
        """
        self.usr.readonly = True
        if self.usr.text.lower() == 'exit':
            app.get_running_app().stop()
        elif self.usr.text.lower() == 'back to start':
            self.usr.text = ''
            self.textinput.text = ''
            self.usr.readonly = False
            self.fadeOut('title')
        elif self.usr.text.lower() == 'battle':
            self.usr.text = ''
            self.trigger()
            self.usr.readonly = False
            arena = main(player, self)
            arena.start()
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
        for shipping to the screen :)
        """
        if string[:4] not in ('>>> ', '\n>_ ', '\n>>>'):
            if self.textinput.text == '' and self.isReady:
                string = '>>> ' + string
            elif string[:2]  == '>_':
                string = '\n>_ ' + string[2:]
            elif string != '\n':
                string = '\n>>> ' + string
        if self.isReady:
            for x in string:
                self.box.append(x)
            self.isReady = False
            self.startQueue = True
            Clock.schedule_interval(self.promptSend, 1/10)
        else:
            self.queue.append(string)
            if self.startQueue:
                self.startQueue = False
                Clock.schedule_interval(self.promptQueue, 1/10)

    def promptQueue(self, dt):
        if self.isReady:
            if not self.stop and self.queue != []:
                self.prompt(self.queue[0])
                self.queue.remove(self.queue[0])
            elif self.stop:
                self.stop = False
            else:
                self.stop = True
        if self.cleanUp:
            self.cleanUp = False
            self.startQueue = True
            return False
            
    def promptSend(self, dt):
        """
        this ships each given letter to the screen
        """
        if len(self.box) != 0:
            self.textinput.text += self.box[self.c]
            self.c += 1
        if self.c == len(self.box):
            self.c = 0
            self.isReady = True
            self.box = []
            return False

    def keepinItCool(self):
        self.textinput.text = ''

    def updateSmallStats(self):
        newHP = player.stats['hp']
        newSP = player.stats['sp']
        hp = player.stats['fullHP']
        sp = player.stats['fullSP']
        name = player.info['name']
        self.playerLabel.text = '[b]%s[/b]:\nhp: %d/%d\nsp: %d/%d' %(name, newHP, hp, newSP, sp)

    def updateAtkList(self):
        atkList = []
        for x in player.atkList:
            atkList.append(x)
        if len(atkList) < 5:
            for x in range(0, 5 - len(atkList)):
                atkList.append('-----')
        self.usr.atkList.adapter.update(atkList)

    def updateInventory(self):
        inv = []
        for x in player.inventory:
            inv.append(x)
        if inv == []:
            inv.append('None')
        self.usr.inventory.adapter.update(inv)

    def updateEquipment(self):
        avaEquip = []
        for x in player.avaEquip:
            avaEquip.append(x)
        if avaEquip == []:
            avaEquip.append('None')
        self.usr.equipment.equipTop.adapter.update(avaEquip)
        curEquip = []
        for x in player.curEquip:
            curEquip.append(x)
        if curEquip == []:
            curEquip.append('None')
        self.usr.equipment.equipBot.adapter.update(curEquip)

    def updatePlayerInfo(self):
        stats = player.stats
        pic = player.info['image']
        #make algorithm for cost for each stat
        statName = ['Health', 'Skill Points', 'Attack', 'Defense',
                'Magic Attack', 'Magic Defense', 'Luck', 'Speed']
        special = player.special[2]
        name = player.info['name']
        self.usr.playerInfo.pic.source = pic
        self.usr.playerInfo.info.text = name + '\n' + special
        self.usr.playerInfo.upStats.adapter.update(statName)
        for s in stats:
            self.usr.playerInfo.current.text += ('\n' + s)
        #for c in costs:
        #    self.usr.playerInfo.current.text += ('\n' + c)

    def updateObjective(self, text):
        self.objective.text = ' !-> %s' %(text)

class Description(Label):
    
    def __init__(self, **kwargs):
        super(Description, self).__init__(**kwargs)
        self.text = 'None'
        with self.canvas:
            Color(0,0,0,1)
            self.rect = Rectangle(size = self.size, pos = self.pos)
        self.bind(pos = self.updateRect)
        self.bind(size = self.updateRect)
        self.viewable = False

    def updateRect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def fade(self):
        if not self.viewable:
            anim = Animation(opacity = 1, duration = .5)
            anim.start(self)
            self.viewable = True
        else:
            anim = Animation(opacity = 0, duration = .5)
            anim.start(self)
            self.viewable = False

class PlayerInfo(BoxLayout):

    info = ObjectProperty(None)
    upStats = ObjectProperty(None)
    current = ObjectProperty(None)
    cost = ObjectProperty(None)
    pic = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(PlayerInfo, self).__init__(**kwargs)
        self.viewable = False

    def fade(self):
        if not self.viewable:
            anim = Animation(opacity = 1, duration = .5)
            anim.start(self)
            self.viewable = True
        else:
            anim = Animation(opacity = 0, duration = .5)
            anim.start(self)
            self.viewable = False

class Equipment(BoxLayout):

    equipTop = ObjectProperty(None)
    equipBot = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Equipment, self).__init__(**kwargs)
        self.viewable = False

    def fade(self):
        if not self.viewable:
            anim = Animation(opacity = 1, duration = .5)
            anim.start(self)
            self.viewable = True
        else:
            anim = Animation(opacity = 0, duration = .5)
            anim.start(self)
            self.viewable = False

class Container(GridLayout):
    
    def __init__(self, **kwargs):
        super(Container, self).__init__(**kwargs)
        self.converter = lambda row_index, rec: {
                'text': rec['name'],
                'size_hint_y': None,
                'height': 15,
                'deselected_color': [0,0,0,1],
                'selected_color': [0,0,.5,1],
                'font_name': 'Pixel'}
        self.adapter = Adapter(
                data = [],
                args_converter = self.converter,
                cls = ListItemButton,
                selection_mode = 'single',
                allow_empty_selection = True)
        self.list_view = ListView(adapter = self.adapter)
        self.add_widget(self.list_view)

class Adapter(ListAdapter):
    
    def update(self, lis):
        for x in lis:
            self.data.append({'name': x, 'is_selected': False})

class UsrInput(TextInput):

    textinput = ObjectProperty(None)
    inventory = ObjectProperty(None)
    atkList = ObjectProperty(None)
    descrip = ObjectProperty(None)
    equipment = ObjectProperty(None)
    playerInfo = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(UsrInput, self).__init__(**kwargs)
        self.permission = False
        self.mode = ''
        self.tF = True
        self.ctrl = False
        self.current = 0
        self.bind(text = self.checkIfNum)
        self.pressedNum = False

    def checkIfNum(self, *args):
        if self.pressedNum:
            self.text = ''
            self.pressedNum = False

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        global player
        keyNum, keyStr = keycode
        if not self.ctrl:
            self.ctrl = keyStr in ('lctrl', 'rctrl', 'ctrl')
        if keyStr in ('up', 'down'):
            if self.mode == 'inventory':
                self.selectItem(self.inventory, string = keyStr)
            elif self.mode == 'atkList':
                self.selectItem(self.atkList, string = keyStr)
            elif self.mode == 'playerInfo':
                self.selectItem(self.playerInfo.upStats, string = keyStr)
            elif self.mode == 'avaEquip':
                if self.ctrl:
                    self.ctrl = False
                    self.selectItem(self.equipment.equipTop)
                    self.mode = 'curEquip'
                    self.selectItem(self.equipment.equipBot, string = 'begin')
                else:
                    self.selectItem(self.equipment.equipTop, string = keyStr)
            elif self.mode == 'curEquip':
                if self.ctrl:
                    self.ctrl = False
                    self.selectItem(self.equipment.equipBot)
                    self.mode = 'avaEquip'
                    self.selectItem(self.equipment.equipTop, string = 'begin')
                else:
                    self.selectItem(self.equipment.equipBot, string = keyStr)
            else:
                self.textinput.focus = True
                if keyStr == 'up':
                    self.textinput.scroll_y = max(0, self.textinput.scroll_y - self.textinput.line_height)
                    self.textinput.focus = False
                elif keyStr == 'down':
                    maxy = self.textinput.minimum_height - self.textinput.height
                    self.textinput.scroll_y = max(0, min(maxy, self.textinput.scroll_y + self.textinput.line_height))
                self.focus = True
        elif keyStr in ('0', '1', '2', '3', '4', '5') and self.permission:
            if keyStr == '0':
                self.pressedNum = True
                player.checkEm('run', self.tF)
            else:
                self.pressedNum = True
                player.checkEm(int(keyStr) - 1, self.tF)
        elif keyStr == 'i' and self.ctrl:
            if self.mode != 'inventory':
                check = True
                if self.mode in ('avaEquip', 'curEquip','atkList', 'playerInfo'):
                    if self.mode == 'atkList':
                        self.selectItem(self.atkList)
                    elif self.mode == 'playerInfo':
                        self.playerInfo.fade()
                        self.selectItem(self.playerInfo.upStats)
                    elif self.mode == 'avaEquip':
                        self.equipment.fade()
                        self.selectItem(self.equipmment.equipTop)
                    elif self.mode == 'curEquip':
                        self.equipment.fade()
                        self.selectItem(self.equipmment.equipBot)
                    check = False
                self.mode = 'inventory'
                self.selectItem(self.inventory, 'begin')
                if check:
                    self.descrip.fade()
            else:
                self.descrip.fade()
                self.selectItem(self.inventory)
                self.mode = ''
                self.text = ''
        elif keyStr == 'a' and self.ctrl:
            if self.mode != 'atkList':
                check = True
                if self.mode in ('avaEquip', 'curEquip','inventory', 'playerInfo'):
                    if self.mode == 'inventory':
                        self.selectItem(self.inventory)
                    elif self.mode == 'playerInfo':
                        self.playerInfo.fade()
                        self.selectItem(self.playerInfo.upStats)
                    elif self.mode == 'avaEquip':
                        self.equipment.fade()
                        self.selectItem(self.equipmment.equipTop)
                    elif self.mode == 'curEquip':
                        self.equipment.fade()
                        self.selectItem(self.equipmment.equipBot)
                    check = False
                self.mode = 'atkList'
                self.selectItem(self.atkList, 'begin')
                if check:
                    self.descrip.fade()
            else:
                self.descrip.fade()
                self.selectItem(self.atkList)
                self.mode = ''
                self.text = ''
        elif keyStr == 'e' and self.ctrl:
            if self.mode not in ('avaEquip', 'curEquip'):
                check = True
                if self.mode in ('atkList', 'inventory', 'playerInfo'):
                    if self.mode == 'inventory':
                        self.selectItem(self.inventory)
                    elif self.mode == 'atkList':
                        self.selectItem(self.atkList)
                    elif self.mode == 'playerInfo':
                        self.playerInfo.fade()
                        self.selectItem(self.playerInfo.upStats)
                    check = False
                self.mode = 'avaEquip'
                self.equipment.fade()
                self.selectItem(self.equipment.equipTop, 'begin')
                if check:
                    self.descrip.fade()
                self.ctrl = False
            else:
                self.descrip.fade()
                if self.mode == 'avaEquip':
                    self.selectItem(self.equipment.equipTop)
                elif self.mode == 'curEquip':
                    self.selectItem(self.equipment.equipBot)
                self.equipment.fade()
                self.mode = ''
                self.text = ''
        elif keyStr == 'u' and self.ctrl:
            if self.mode != 'playerInfo':
                check = True
                if self.mode in ('avaEquip', 'curEquip','inventory', 'atkList'):
                    if self.mode == 'inventory':
                        self.selectItem(self.inventory)
                    elif self.mode == 'atkList':
                        self.selectItem(self.atkList)
                    elif self.mode == 'avaEquip':
                        self.equipment.fade()
                        self.selectItem(self.equipmment.equipTop)
                    elif self.mode == 'curEquip':
                        self.equipment.fade()
                        self.selectItem(self.equipmment.equipBot)
                    check = False
                self.mode = 'playerInfo'
                self.playerInfo.fade()
                self.selectItem(self.playerInfo.upStats, 'begin')
                if not check:
                    self.descrip.fade()
            else:
                self.playerInfo.fade()
                self.selectItem(self.playerInfo.upStats)
                self.mode = ''
                self.text = ''
        elif keyStr == 'enter' and self.mode != '':
            if self.mode == 'inventory':
                self.selectItem(self.inventory)
                self.mode = ''
                self.descrip.fade()
            elif self.mode == 'atkList' and self.permission:
                self.selectItem(self.atkList)
                self.mode = ''
                self.descrip.fade()
            if self.mode in ('avaEquip', 'curEquip'):
                if self.mode == 'avaEquip':
                    self.selectItem(self.equipment.equipTop)
                elif self.mode == 'curEquip':
                    self.selectItem(self.equipment.equipBot)
                self.mode = ''
                self.equipment.fade()
                self.descrip.fade()
            super(UsrInput, self).keyboard_on_key_down(window, keycode, text, modifiers)
        elif keyStr not in ('lctrl', 'rctrl', 'ctrl'):
            self.ctrl = False
            if keyStr in ('0', '1', '2', '3', '4', '5'):
                print keyStr
            else:
                super(UsrInput, self).keyboard_on_key_down(window, keycode, text, modifiers)

    def selectItem(self, container, string = ''):
        data = len(container.adapter.data) -1
        move = True
        if string == 'begin':
            self.current = 0
        elif string == 'down':
            self.current += 1
            if self.current > data:
                self.current -= 1
                move = False
        elif string == 'up':
            self.current -= 1
            if self.current < 0:
                self.current += 1
                move = False
        if move:
            view = container.adapter.get_view(self.current)
            container.adapter.handle_selection(view)
            if self.current == 0:
                self.scroll(1, container)
            elif self.current >= len(container.adapter.data) - 8:
                self.scroll(0, container)
            else:
                pos = 1 - (self.current * 1.3  /len(container.adapter.data))
                self.scroll(pos, container)
            if string != '':
                self.text = view.text
                self.updateDescription()

    def scroll(self, pos, container):
        scrlview = container.list_view.container.parent
        scrlview.scroll_y = pos

    def updateDescription(self):
        if self.text in ('None', '-----'):
            self.descrip.text = 'None'
        else:
            if self.mode == 'inventory':
                pass
            elif self.mode == 'atkList':
                pass

class Menu(Screen):
    pass

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
