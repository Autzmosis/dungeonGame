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
Config.set('graphics','resizable', 0)
Config.set('input', 'mouse', 'none')

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
from charANPC import Player
from arena import *
from textRecognition import TextRecognition

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

    def responce(self, kwargs):
        """
        this function is called when player presses enter, it validates the
        text and does something, depending on what was typed.
        """
        strings = kwargs['string']
        if not self.c:
            if ('new' and 'game') in strings:
                if data.count():
                    self.hint.text = 'Looks, like you\'ve done this before. Are you sure you want to restart?'
                    self.c = 1
                else:
                    self.hint.text = 'Your story is about to begin.'
                    self.self.fadeOut('chooseclass')
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
        self.c = 0
        for string in strings:
            if string in ('yes', 'yeah', 'ye', 'y', 'sure', 'ya', 'yup'):
                self.hint.text = 'Your story is about to begin.'
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

class ChooseClass(FadeScreen):
    
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
        self.c = 0 #used so i can ask player their name
        self.info = {}

    def responce(self, kwargs):
        """
        this function is used for text recognition features
        """
        strings = kwargs['string']
        image = kwargs['image']
        if self.c == 0:
            self.c = 1
            self.hint.text = 'By the way, what might your name be?'
            if 'rogue' in strings:
                self.info['class'] = 'rogue'
                self.info['image'] = image[0].source
            elif 'warrior' in strings:
                self.info['class'] = 'warrior'
                self.info['image'] = image[1].source
            elif 'mage' in strings:
                self.info['class'] = 'mage'
                self.info['image'] = image[2].source
            else:
                self.c = 0
                self.hint.text = 'Please choose one of the classes above.'
        else:
            self.getName(strings)
        self.refocus()

    def getName(self, strings):
        if strings:
            self.info['name'] = strings[0]
            self.hint.text = 'Cool, let\'s get going then.'
            self.setupPlayer()
            self.fadeOut('gamescreen')
            self.c = 0
            self.refocus()
        else:
            self.hint.text = 'Unresponsive, are we? Well it takes two to tango!'
            self.refocus()

    def setupPlayer(self):
        global player
	player = Player(self.manager.get_screen('gamescreen'))
	player.changeRC(Class = self.info['class'])
        player.info = self.info
        player.updateBase()

    def on_pre_enter(self):
        self.refocus()
        self.trigFadeIn()
        self.hint.text = 'Type name of class and press enter'

class GameScreen(FadeScreen):
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
        self.data = data
        self.box = []
        self.c = 0
        self.queue = []
        self.isReady = True
        self.startQueue = True
        self.stop = False
        self.cleanUp = False
        self.pressEnter = False
	self.modQueue = []

    def on_enter(self):
        global player
        self.refocus()
        self.trigFadeIn()
        Clock.schedule_once(self.welcome, 2.5)
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
	player = Player(self)
        player.updateSelf()
	player.changeRC(Class = data.get('player')['info']['class'])

    def responce(self, kwargs):
        """
        this method validates text and sends to prompt
        just for testing out crap
        """
        self.usr.readonly = True
        strings = kwargs['string']
        if 'exit' in strings:
            app.get_running_app().stop()
        elif ('back' and 'to' and 'start') in strings:
            self.textinput.text = ''
            self.usr.text = ''
            app.textRec.modes.remove('gamescreen')
            self.fadeOut('title')
        elif 'battle' in strings:
            self.refocus()
            app.textRec.modes.append('battle')
            self.usr.battleMode = True
            self.usr.enemBox.fade()
            self.startArena()
        elif strings:
            self.textinput.text += '\n>_ ' + self.usr.text
            sleep(.25)
            thread = Thread(None, self.prompt, 'thread',
                            args=['I be test prompt.'])
            thread.daemon = True
            thread.start()
            self.refocus()
        else:
            self.refocus()
        self.usr.readonly = False
        
    def welcome(self, dt):
        """
        This is here because it is the first string sent to prompt, and 
        does not rely on user pressing enter
        """
        x = 'Welcome to the world of Dungeons and Towns!'
        thread = Thread(None, self.prompt, 'thread', args=[x])
        thread.daemon = True
        thread.start()

    def prompt(self, string, **kwargs):
        """
        this breaks up typed string into a box and packages each letter
        for shipping to the screen :)
        """
        self.usr.readonly = True
        mod = None
	if 'mod' in kwargs:
	    mod = kwargs['mod']
        #if not typing.get_pos():
        #    typing.play()
        #else:
        #    typing.volume = .5
        if string[:4] not in ('>>> ', '\n>_ ', '\n>>>') and string != 'self.endArena':
            if self.textinput.text == '' and self.isReady:
                string = '>>> ' + string
            elif string[:2]  == '>_':
                string = '\n>_ ' + string[2:]
            elif string != '\n':
                string = '\n>>> ' + string
        if self.isReady:
            if string == 'self.endArena':
                self.endArena()
                return
            for x in string:
                self.box.append(x)
            self.isReady = False
            self.startQueue = True
            Clock.schedule_interval(self.promptSend, .025)
        else:
            self.queue.append([string, mod])
            if self.startQueue:
                self.startQueue = False
                self.cleanUp = False
                Clock.schedule_interval(self.promptQueue, .025)

    def promptQueue(self, dt):
        if self.isReady:
            if not self.stop and self.queue != []:
                if self.queue[0][1]:
		    self.modQueue.append(self.queue[0][1])
                self.prompt(self.queue[0][0])
                self.queue.remove(self.queue[0])
            elif self.stop:
                self.stop = False
            else:
                self.stop = True
        elif self.cleanUp:
            self.cleanUp = False
            self.startQueue = True
            return False
            
    def promptSend(self, dt):
        """
        this ships each given letter to the screen
        """
        if len(self.box):
            self.textinput.text += self.box[self.c]
            self.c += 1
        if self.c == len(self.box):
        #    typing.volume = 0
            #if not self.queue:
                #typing.stop()
            self.c = 0
            self.isReady = True
            self.box = []
	    if self.modQueue and self.modQueue[0]:
		character = self.modQueue[0][0]
		mod = self.modQueue[0][1]
	    	character.statModifier(mod)
	    	self.modQueue.remove(self.modQueue[0])
            self.usr.readonly = False
            return False

    def keepinItCool(self):
        self.textinput.text = ''
        self.cleanUp = True
        self.usr.readonly = False
        if not self.usr.battleMode:
            app.textRec.modes.remove('battle')

    def startArena(self): #later this will take all enmies and allies who will fight
        self.arena = main(player, self)
        self.arena.start()

    def endArena(self):
        self.usr.permission = True
        self.usr.battleMode = False
        self.usr.enemBox.fade()
        self.keepinItCool()
        player.stats['hp'] = player.stats['fullHP']
        self.updateSmallStats()
        self.updateInventory()

    def goCheckEm(self, string):
        try:
            text = '%s %s' %(string[0], string[1])
        except IndexError:
            text = string[0]
        player.checkEm(text, self.usr.tF)

    def updateEnemyList(self):
        enemies = []
        for x in player.enemyNames:
            enemies.append(x)
        if enemies == []:
            enemies.append('None')
        self.usr.enemyList.adapter.update(enemies)

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
        if not player.inventory:
            inv.append('none')
        else:
            for x in player.inventory:
                inv.append(x.name)
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

    def updatePlayerInfo(self, quick = False):
        stats = []
        costs = []
        lvls = []
        realStatName = []
        statName = ['Health', 'Skill Points', 'Attack', 'Defense',
                'Magic Attack', 'Magic Defense', 'Luck', 'Speed']
        for s in statName:
            realStatName.append(self.usr.translateDict[s])
        for x in realStatName:
            costs.append(str(player.generateNextExpForStat(x)))
            stats.append(str(player.stats[x]))
            lvls.append(str(player.upStats[x][0]))
        self.usr.playerInfo.current.adapter.update(stats)
        self.usr.playerInfo.lvl.adapter.update(lvls)
        self.usr.playerInfo.cost.adapter.update(costs)
        if not quick:
            pic = player.info['image']
            special = player.special[2]
            name = player.info['name']
            Class = player.info['class']
            element = player.stats['elem'][0]
            exp = str(player.stats['exp'])
            self.usr.playerInfo.pic.source = pic
            self.usr.playerInfo.info.text = '%s\nClass: %s\nElement: %s\nExp: %s' %(name, Class, element, exp)
            self.usr.playerInfo.special.text = special + '\nDescription'
            self.usr.playerInfo.upStats.adapter.update(statName)

    def updateObjective(self, text):
        self.objective.text = ' !-> %s' %(text)

class FadePart(object):

    def __init__(self, **kwargs):
        self.fadeIn = Animation(opacity = 1, duration = .25)
        self.fadeOut = Animation(opacity = 0, duration = .25)
        self.opacity = 0

    def fade(self):
        if not self.opacity:
            self.fadeIn.start(self)
        else:
            self.fadeOut.start(self)

class SlidePart(object):

    def __init__(self, **kwargs):
        self.desiredPosition = 1
        self.originalPosition = -180
        if isinstance(self, MixedLabel):
            self.desiredPosition = 410
            self.originalPosition = 460
            self.slideIn = Animation(y = self.desiredPosition, duration = .25)
            self.slideOut = Animation(y = self.originalPosition, duration = .25)
        else:
            self.slideIn = Animation(x = self.desiredPosition, duration = .25)
            self.slideOut = Animation(x = self.originalPosition, duration = .25)
    
    def slide(self):
        if self.x == self.originalPosition or self.y == self.originalPosition:
            self.slideIn.start(self)
        else:
            self.slideOut.start(self)

class MixedPart(FadePart, SlidePart):

    def __init__(self, **kwargs):
        for base in MixedPart.__bases__:
            base.__init__(self)

    def fadeSlide(self):
        self.fade()
        self.slide()

class FadeLabel(Label, FadePart):
    
    fadeinput = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(FadeLabel, self).__init__(**kwargs)

    def fade(self):
        if not self.opacity and self.fadeinput:
            self.fadeOut.start(self.fadeinput)
        elif self.fadeinput:
            self.fadeIn.start(self.fadeinput)
        super(FadeLabel, self).fade()

class FadeBox(BoxLayout, FadePart):

    def __init__(self, **kwargs):
        super(FadeBox, self).__init__(**kwargs)

class SlideBox(BoxLayout, SlidePart):

    def __init__(self, **kwargs):
        super(SlideBox, self).__init__(**kwargs)

class MixedBox(BoxLayout, MixedPart):

    def __init__(self, **kwargs):
        super(MixedBox, self).__init__(**kwargs)

class MixedLabel(Label, MixedPart):

    def __init__(self, **kwargs):
        super(MixedLabel, self).__init__(**kwargs)

class PlayerInfo(FadeBox):

    info = ObjectProperty(None)
    upStats = ObjectProperty(None)
    current = ObjectProperty(None)
    cost = ObjectProperty(None)
    pic = ObjectProperty(None)
    whole = ObjectProperty(None)
    lvl = ObjectProperty(None)
    special = ObjectProperty(None)
    hint = ObjectProperty(None)
    upStatUsr = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(PlayerInfo, self).__init__(**kwargs)

    def fade(self):
        if not self.opacity:
            self.fadeOut.start(self.whole)
        else:
            self.fadeIn.start(self.whole)
        super(PlayerInfo, self).fade()

class Equipment(FadeBox):

    equipTop = ObjectProperty(None)
    equipBot = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Equipment, self).__init__(**kwargs)

class Inventory(MixedBox):

    inventory = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Inventory, self).__init__(**kwargs)

class AtkList(MixedBox):

    atkList = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(AtkList, self).__init__(**kwargs)

class EnemyList(MixedBox):

    enemyList = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(EnemyList, self).__init__(**kwargs)

class Container(GridLayout):
    
    def __init__(self, **kwargs):
        super(Container, self).__init__(**kwargs)
        self.converter = lambda row_index, rec: {
                'text': rec['name'],
                'size_hint_y': None,
                'height': 15,
                'deselected_color': [.5,.5,.5,0],
                'selected_color': [0,0,1,.2],
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
        self.data = []
        for x in lis:
                self.data.append({'name': x, 'is_selected': False})

class UsrInput(TextInput):

    textinput = ObjectProperty(None)
    inventory = ObjectProperty(None)
    atkList = ObjectProperty(None)
    enemyList = ObjectProperty(None)
    invBox = ObjectProperty(None)
    atkBox = ObjectProperty(None)
    enemBox = ObjectProperty(None)
    descrip = ObjectProperty(None)
    equipment = ObjectProperty(None)
    playerInfo = ObjectProperty(None)
    screen = ObjectProperty(None)
    smallStats = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(UsrInput, self).__init__(**kwargs)
        self.permission = True
        self.mode = ''
        self.battleMode = False
        self.tF = True
        self.ctrl = False
        self.current = {}
        self.pressedNum = False
        self.memoryStat = {}
        self.stopInput = False
        self.translateDict = {
                'Health': 'fullHP',
                'Skill Points': 'fullSP',
                'Attack': 'atk',
                'Defense': 'def',
                'Magic Attack': 'ma',
                'Magic Defense': 'md',
                'Luck': 'lck',
                'Speed': 'spe'
                }

    def fadeInvAtk(self):
        self.invBox.fade()
        self.atkBox.fade()

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if self.readonly:
            self.text = ''
            return
        global player
        keyNum, keyStr = keycode
        self.ctrl = (keyStr == 'ctrl') or ('ctrl' in modifiers)
        if not self.ctrl and self.mode == 'playerInfo':
            self.playerInfo.upStatUsr.focus = True
            self.playerInfo.upStatUsr.keyboard_on_key_down(window, keycode, text, modifiers)
            self.focus = True
            if keyStr not in ('up', 'down'):
                return
        if keyStr in ('up', 'down'):
            if self.mode == 'inventory':
                self.selectItem(self.inventory, string = keyStr)
            elif self.mode == 'atkList':
                self.selectItem(self.atkList, string = keyStr)
            elif self.mode == 'enemy':
                self.selectItem(self.enemyList, string = keyStr)
            elif self.mode == 'playerInfo':
                if self.ctrl and keyStr == 'up':
                    self.upgradeStat()
                    self.selectPlayerInfo()
                else:
                    self.selectPlayerInfo(string = keyStr)
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
        elif keyStr in ('0', '1', '2', '3', '4', '5') and self.battleMode and self.permission:
            if keyStr == '0':
                player.checkEm('run', self.tF)
            else:
                player.checkEm(int(keyStr) - 1, self.tF)
        elif keyStr == 'i' and self.ctrl and self.permission:
            self.ctrl = False
            if self.mode != 'inventory':
                check = True
                if self.mode in ('enemy', 'avaEquip', 'curEquip', 'atkList', 'playerInfo'):
                    if self.mode == 'atkList':
                        self.selectItem(self.atkList)
                    elif self.mode == 'avaEquip':
                        self.equipment.fade()
                        self.selectItem(self.equipment.equipTop)
                        self.fadeInvAtk()
                    elif self.mode == 'curEquip':
                        self.equipment.fade()
                        self.selectItem(self.equipment.equipBot)
                        self.fadeInvAtk()
                    check = False
                    if self.mode == 'enemy':
                        self.selectItem(self.enemyList)
                        check = True
                    elif self.mode == 'playerInfo':
                        self.playerInfo.fade()
                        self.selectPlayerInfo()
                        check = True
                if check:
                    self.descrip.fade()
                self.mode = 'inventory'
                self.selectItem(self.inventory, string = 'begin')
            else:
                self.descrip.fade()
                self.selectItem(self.inventory)
                self.mode = ''
                self.text = ''
        elif keyStr == 'a' and self.ctrl and self.permission:
            self.ctrl = False
            if self.mode != 'atkList':
                check = True
                if self.mode in ('enemy', 'avaEquip', 'curEquip', 'inventory', 'playerInfo'):
                    if self.mode == 'inventory':
                        self.selectItem(self.inventory)
                    elif self.mode == 'avaEquip':
                        self.equipment.fade()
                        self.selectItem(self.equipment.equipTop)
                        self.fadeInvAtk()
                    elif self.mode == 'curEquip':
                        self.equipment.fade()
                        self.selectItem(self.equipment.equipBot)
                        self.fadeInvAtk()
                    check = False
                    if self.mode == 'enemy':
                        self.selectItem(self.enemyList)
                        check = True
                    elif self.mode == 'playerInfo':
                        self.playerInfo.fade()
                        self.selectPlayerInfo()
                        check = True
                if check:
                    self.descrip.fade()
                self.mode = 'atkList'
                self.selectItem(self.atkList, string = 'begin')
            else:
                self.descrip.fade()
                self.selectItem(self.atkList)
                self.mode = ''
                self.text = ''
        elif keyStr == 'e' and self.ctrl and self.permission:
            self.ctrl = False
            if self.mode not in ('avaEquip', 'curEquip', 'enemy'):
                check = True
                if self.mode in ('atkList', 'inventory', 'playerInfo'):
                    if self.mode == 'inventory':
                        self.selectItem(self.inventory)
                    elif self.mode == 'atkList':
                        self.selectItem(self.atkList)
                    check = False
                    if self.mode == 'playerInfo':
                        self.playerInfo.fade()
                        self.selectPlayerInfo()
                        check = True
                if self.battleMode:
                    self.mode = 'enemy'
                    self.selectItem(self.enemyList, string = 'begin')
                    if not check:
                        self.descrip.fade()
                else:
                    self.mode = 'avaEquip'
                    self.fadeInvAtk()
                    self.equipment.fade()
                    self.selectItem(self.equipment.equipTop, string = 'begin')
                    if check:
                        self.descrip.fade()
                self.ctrl = False
            else:
                if self.mode == 'avaEquip':
                    self.selectItem(self.equipment.equipTop)
                elif self.mode == 'curEquip':
                    self.selectItem(self.equipment.equipBot)
                if self.mode == 'enemy':
                    self.selectItem(self.enemyList)
                else:
                    self.equipment.fade()
                    self.fadeInvAtk()
                    self.descrip.fade()
                self.mode = ''
                self.text = ''
        elif keyStr == 'u' and self.ctrl and not self.battleMode and self.permission:
            self.ctrl = False
            if self.mode != 'playerInfo':
                check = False
                if self.mode in ('avaEquip', 'curEquip','inventory', 'atkList'):
                    if self.mode == 'inventory':
                        self.selectItem(self.inventory)
                    elif self.mode == 'atkList':
                        self.selectItem(self.atkList)
                    elif self.mode == 'avaEquip':
                        self.equipment.fade()
                        self.fadeInvAtk()
                        self.selectItem(self.equipment.equipTop)
                    elif self.mode == 'curEquip':
                        self.equipment.fade()
                        self.fadeInvAtk()
                        self.selectItem(self.equipment.equipBot)
                    check = True
                self.mode = 'playerInfo'
                self.playerInfo.fade()
                self.selectPlayerInfo(string = 'begin')
                self.playerInfo.hint.text = 'Select which stat you want to upgrade.'
                if check:
                    self.descrip.fade()
            else:
                self.playerInfo.fade()
                self.selectPlayerInfo()
                self.mode = ''
                self.text = ''
        elif keyStr == 's' and self.mode == 'playerInfo' and self.ctrl:
            if self.memoryStat:
                app.textRec.modes.append('upStat')
                self.playerInfo.upStatUsr.focus = True
                self.playerInfo.hint.text = 'Do you want to keep these changes?'
            else:
                self.playerInfo.hint.text = 'Changes have not been done.'
        elif keyStr == 'enter' and self.mode:
            if self.mode == 'inventory':
                self.selectItem(self.inventory)
                self.descrip.fade()
            elif self.mode == 'atkList':
                self.selectItem(self.atkList)
                self.descrip.fade()
            elif self.mode == 'enemy':
                self.selectItem(self.enemyList)
            elif self.mode in ('avaEquip', 'curEquip'):
                if self.mode == 'avaEquip':
                    self.selectItem(self.equipment.equipTop)
                elif self.mode == 'curEquip':
                    self.selectItem(self.equipment.equipBot)
                else:
                    self.equipment.fade()
                    self.descrip.fade()
            self.mode = ''
            super(UsrInput, self).keyboard_on_key_down(window, keycode, text, modifiers)
        elif keyStr not in ('lctrl', 'rctrl', 'ctrl'):
            self.ctrl = False
            if keyStr not in ('0', '1', '2', '3', '4', '5') or not self.battleMode:
                super(UsrInput, self).keyboard_on_key_down(window, keycode, text, modifiers)

    def selectItem(self, *containers, **kwargs):
        string = kwargs.pop('string', '')
        for container in containers:
            if container not in self.current:
                self.current[container] = 0
            data = len(container.adapter.data) -1
            move = True
            current = self.current[container]
            if string == 'begin':
                current = 0
            elif string == 'down':
                current += 1
                if current > data:
                    current -= 1
                    move = False
            elif string == 'up':
                current -= 1
                if current < 0:
                    current += 1
                    move = False
            self.current[container] = current
            view = container.adapter.get_view(current)
            self.updateDescription(view.text)
            if move:
                container.adapter.handle_selection(view)
                if current == 0:
                    self.scroll(1, container)
                elif self.current >= len(container.adapter.data) - 8:
                    self.scroll(0, container)
                else:
                    pos = 1 - (self.current * 1.3  /len(container.adapter.data))
                    self.scroll(pos, container)
                if string != '':
                    if self.mode != 'playerInfo':
                        self.text = view.text
                    else:
                        self.currentStat = self.playerInfo.upStats.adapter.get_view(current)

    def selectPlayerInfo(self, string = ''):
        self.selectItem(
                self.playerInfo.upStats, 
                self.playerInfo.current, 
                self.playerInfo.lvl,
                self.playerInfo.cost, 
                string = string)

    def scroll(self, pos, container):
        scrlview = container.list_view.container.parent
        scrlview.scroll_y = pos

    def updateDescription(self, text):
        global player
        if self.text in ('None', '-----'):
            self.descrip.text = 'None'
        elif self.mode != 'playerInfo':
            if self.mode == 'atkList':
                self.descrip.text = 'None'
                #for x in player.atkList:
                #    if text == x:
                #        self.descrip.text = player.atkList[text]
            else:
                for x in player.inventory:
                    if text == x.name:
                        self.descrip.text = x.descrip

    def upgradeStat(self):
        x = self.current[self.playerInfo.upStats]
        statView = self.playerInfo.upStats.adapter.get_view(x)
        stat = self.translateDict[statView.text]
        requiredExp = player.generateNextExpForStat(stat)
        if player.stats['exp'] >= requiredExp:
            player.stats['exp'] -= requiredExp
            player.upgradeStat(stat)
            try:
                self.memoryStat[stat] += 1
            except KeyError:
                self.memoryStat[stat] = 1
            self.screen.updatePlayerInfo()
        else:
            self.playerInfo.hint.text = 'You don\'t have enough exp for that!'
            self.selectPlayerInfo()

    def confirmUpgradeStat(self, strings):
        self.playerInfo.upStatUsr.text = ''
        for answer in strings:
            if answer in ('yes', 'yeah', 'ye', 'y', 'sure', 'ya', 'yup'):
                self.screen.updateSmallStats()
                self.count = 1
                self.playerInfo.hint.text = 'Stats have been upgraded.'
                self.memoryStat.clear()
                app.textRec.modes.remove('upStat')
                self.focus = True
                break
            elif answer in ('no', 'nah', 'nope', 'n'):
                for s in self.memoryStat:
                    player.upStats[s][0] -= self.memoryStat[s]
                    player.upgradeStat(s, True)
                self.screen.updatePlayerInfo()
                self.memoryStat.clear()
                self.playerInfo.hint.text = 'Upgrade has been reversed.'
                app.textRec.modes.remove('upStat')
                self.selectPlayerInfo()
                self.focus = True
                break
        if not strings:
            self.playerInfo.hint.text = 'That was a yes or no question!!'
            self.playerInfo.upStatUsr.focus = True

class DungeonGame(App):
    """
    this is the actual instance of the app, doesn't do much
    but set up the screens and screenmanager
    """

    def __init__(self, **kwargs):
        super(DungeonGame, self).__init__(**kwargs)
        self.textRec = TextRecognition()
        
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
    #audio = SoundLoader()
    #typing = audio.load('../audio/typingSound.wav')
    #typing.loop = True
    #typing.play()
    app = DungeonGame()
    app.run()
