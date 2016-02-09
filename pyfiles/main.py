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
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.listview import ListItemButton, ListView
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.core.text import LabelBase
from kivy.properties import ObjectProperty, ListProperty
from kivy.clock import Clock
from threading import Thread
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from kivy.graphics import *
from kivy.storage.jsonstore import JsonStore
from kivy.core.audio import SoundLoader
from charANPC import makePlayer
from arena import *
from textRecognition import TextRecognition
from time import time, sleep
from random import random, randint

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
        if not isinstance(self, GameScreen) or not self.usr.mode:
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

    def responce(self, inputs):
        """
        this function is used for text recognition features
        """
        strings = inputs
        if self.c == 0:
            self.c = 1
            self.hint.text = 'By the way, what might your name be?'
            if 'rogue' in strings:
                self.info['class'] = 'rogue'
            elif 'warrior' in strings:
                self.info['class'] = 'warrior'
            elif 'mage' in strings:
                self.info['class'] = 'mage'
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
        player = makePlayer(
			gui = self.manager.get_screen('gamescreen'),
			Class = self.info['class'],
			name = self.info['name'],
			expGol = [0, 0],
			statsUp = {},
			inventoryNames = [],
			#equipmentNames = [],
			#weaponNames = [],
			#armourNames = []
			)
        player.makeSelf()

    def on_pre_enter(self):
        self.refocus()
        self.trigFadeIn()
        self.hint.text = 'Type name of class and press enter'
        app.startWatch()

class GameScreen(FadeScreen):
    """
    This is the GameScreen class. This class needs a lot more functionality
    than the other screens, so there are more than a few different methods
    here. Consider this advanced text recognition and config functionality
    """

    textinput = ObjectProperty(None)
    usr = ObjectProperty(None)
    image = ObjectProperty(None)
    main = ObjectProperty(None)
    supp = ObjectProperty(None)
    actionList = ObjectProperty(None)
    objective = ObjectProperty(None)
    playerLabel = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.data = data #for player access
        self.box = []
        self.c = 0
        self.queue = []
        self.isReady = True
        self.startQueue = True
        self.stop = False
        self.cleanUp = False
        self.pressEnter = False
        self.snapshot = []
        self.csave = True
        self.quitting = False

    def on_enter(self):
        global player
        if not app.beginTime:
            app.startWatch()
        self.textinput.text = ''
        self.refocus()
        self.trigFadeIn()
        Clock.schedule_once(self.welcome, 2.5)
        self.morph()
        if player is None:
            self.setupPlayer()
        if player.info['name'] in ('dev', 'paul'): #dev and paul get handicap
            player.stats['exp'] += 512
        #self.image.source = player.info['image']
        #self.updateSmallStats()
        #self.updateAtkList()
        #self.updateInventory()
        #self.updateEquipment()
        #self.updatePlayerInfo()

    def setupPlayer(self):
        global player
	playerInfo = self.data.get('player')
	gui = self
	Class = playerInfo['info']['class']
	name = playerInfo['info']['name']
	expGol = [playerInfo['stats']['exp'], playerInfo['stats']['gol']]
        inventoryNames = playerInfo['inventory']
        #weaponNames = playerInfo['weapon']
        #armourNames = playerInfo['armour']
        #equipmentNames = playerInfo['equipment']
        statsUp = playerInfo['stats']
        classLvlHist = playerInfo['classLvlHist']
	player = makePlayer(
			gui = gui,
			Class = Class,
			name = name,
			expGol = expGol,
			inventoryNames = inventoryNames,
			#weaponNames = weaponNames,
			#armourNames = armourNames,
			#equipmentNames = equipmentNames,
			statsUp = statsUp,
                        classLvlHist = classLvlHist
			)

    def fadeToTitle(self, dt = 0):
        self.fadeOut('title')

    def responce(self, inputs):
        """
        this method validates text and sends to prompt
        just for testing out crap
        """
        self.usr.readonly = True
        strings = inputs
        if 'exit' in strings:
            app.get_running_app().stop()
        elif 'save' in strings:
            self.save()
            if 'quit' in strings:
                self.quitting = True
                Clock.schedule_once(self.fadeToTitle, 6)
        elif ('back' and 'to' and 'start') in strings:
            self.textinput.text = ''
            self.usr.text = ''
            self.fadeOut('title')
        elif 'battle' in strings:
            self.refocus()
            app.textRec.mode = 'battle'
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

    def save(self, *args):
        if self.csave:
            time = app.stopWatch()
            m, s = divmod(int(round(time)), 60)
            h, m = divmod(m, 60)
            displayedTime = '%02d:%02d:%02d' %(h, m, s)
            data.put('game', time = time)
            player.updateBase()
            self.prompt('Total Play Time: %s<<<' %(displayedTime))
            self.prompt('Saving data...')
            self.csave = False
            Clock.schedule_once(self.save, 3)
        else:
            self.prompt('Data saved successfully!')
            self.csave = True
            if self.quitting:
                self.prompt('Goodbye %s!' %(player.info['name']))
        
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
        if not typing.get_pos():
            typing.play()
        else:
            typing.volume = .5
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
                typing.stop()
                return
            elif string == '\n>>> Press Enter <<<':
                self.usr.permission = False
            tF = False
            if 'self.snapshot' in string:
                tF = True
                string = string[:5] + string[18:]
            if string[:4] == '>>> ':
                self.textinput.text += '>>> '
                string = string[4:]
            elif string[:5] == '\n>>> ':
                self.textinput.text += '\n>>> '
                string = string[5:]
            print string
            for x in string:
                self.box.append(x)
            if tF:
                self.box.append('self.snapshot')
            self.isReady = False
            self.startQueue = True
            Clock.schedule_interval(self.promptSend, .04)
        else:
            self.queue.append(string)
            if self.startQueue:
                self.startQueue = False
                self.cleanUp = False
                Clock.schedule_interval(self.promptQueue, .025)

    def promptQueue(self, dt):
        if self.isReady:
            if self.queue:
                self.prompt(self.queue[0])
                self.queue.remove(self.queue[0])
            elif self.stop:
                self.stop = False
            else:
                self.stop = True
        elif self.cleanUp:
            self.cleanUp = False
            self.startQueue = True
            typing.stop()
            return False
            
    def promptSend(self, dt):
        """
        this ships each given letter to the screen
        """
        if len(self.box):
            if self.box[self.c] == 'self.snapshot':
                self.updateSmallStats()
            else:
                self.textinput.text += self.box[self.c]
            self.c += 1
        if self.c == len(self.box):
            typing.volume = 0
            self.c = 0
            self.isReady = True
            self.box = []
            self.usr.readonly = False
            return False

    def keepinItCool(self):
        self.textinput.text = ''
        self.cleanUp = True
        self.usr.readonly = False
        if not self.usr.battleMode:
            app.textRec.mode = ''

    def startArena(self): #later this will take all enmies and allies who will fight
        self.arena = main(player, self)
        self.arena.start()

    def morph(self, dt = 0):
        if self.objective.opacity:
            self.objective.fade()
            Animation(y = -25, duration = .25).start(self.main)
            Animation(x = 121, duration =.25).start(self.main)
            Animation(height = 225, duration = .25).start(self.textinput)
            Animation(width = 520, duration = .25).start(self.main)
            self.supp.fade()
        else:
            self.objective.fade()
            Animation(y = 1, duration = .25).start(self.main)
            Animation(x = 1, duration =.25).start(self.main)
            Animation(height = 200, duration = .25).start(self.textinput)
            Animation(width = 640, duration = .25).start(self.main)
            self.supp.fade()
        Clock.schedule_once(self.morph, 2)

    def endArena(self):
        self.usr.permission = True
        self.usr.battleMode = False
        self.usr.enemBox.fade()
        self.keepinItCool()
        player.stats['sp'] = player.stats['fullSP']
        self.updateSmallStats()
        self.updateInventory()
        self.updatePlayerInfo()
        self.updateEquipment()

    def goCheckEm(self, string):
        try:
            text = '%s %s' %(string[0], string[1])
        except IndexError:
            text = string[0]
        player.checkEm(text)

    def veryRandom(self, randup = 0):
        try:
            randomList = []
            c = 0
            rand = int(round(random() * 100))
            if randup:
                while randup > 1:
                    randup = randup * .5 * random()
                some = int(random() * 100)
                randest = int(randup * randint(1, some)) * int(random() * 100)
                while randest >= 100:
                    randest /= 2
                    randest *= (random() * 5)
                if not (0 < randest < 100):
                    randest = self.veryRandom(randup = randest)
                return int(randest)
            else:
                while c != rand:
                    randomList.append(random())
                    c += 1
                if randomList == []:
                    while c < 11:
                        randomList.append(random())
                        c += 1
                for r in randomList:
                    ranLen = len(randomList) - 1
                    if ranLen > 1:
                        rander = randint(1, ranLen)
                        randomList[rander] = r
                randit = randomList[randint(1, ranLen - 1)]
                return int(self.veryRandom(randup = randit))
        except ValueError:
            return self.veryRandom()
        
    def updateEnemyList(self):
        enemies = []
        for x in player.enemyNames:
            enemies.append(x)
        if enemies == []:
            enemies.append('None')
        self.usr.enemyList.adapter.update(enemies)

    def updateSmallStats(self):
        if self.snapshot:
            newHP = self.snapshot[0][0]
            newSP = self.snapshot[0][1]
            self.snapshot.remove(self.snapshot[0])
        else:
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
            special = player.special[0]
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
        if isinstance(self, FadeTranLabel):
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

class TransformPart(object):

    def __init__(self, **kwargs):
        self.originalSize = 854
        self.desiredSize = 427
        self.shrink = Animation(width = self.desiredSize, duration = .25)
        self.grow = Animation(width = self.originalSize, duration = .25)

    def transform(self):
        if self.width != self.desiredSize:
            self.shrink.start(self)
        else:
            self.grow.start(self)

class FadeTranPart(FadePart, TransformPart):

    def __init__(self, **kwargs):
        for base in FadeTranPart.__bases__:
            base.__init__(self)

    def fadeTran(self):
        self.fade()
        self.transform()

class FadeLabel(Label, FadePart):

    def __init__(self, **kwargs):
        super(FadeLabel, self).__init__(**kwargs)

class FadeTranLabel(Label, FadeTranPart):

    def __init__(self, **kwargs):
        super(FadeTranLabel, self).__init__(**kwargs)

class FadeBox(BoxLayout, FadePart):

    def __init__(self, **kwargs):
        super(FadeBox, self).__init__(**kwargs)

class SlideBox(BoxLayout, SlidePart):

    def __init__(self, **kwargs):
        super(SlideBox, self).__init__(**kwargs)

class TransformBox(BoxLayout, TransformPart):

    def __init__(self, **kwargs):
        super(TransformBox, self).__init__(**kwargs)

class FadeTranBox(BoxLayout, FadeTranPart):

    def __init__(self, **kwargs):
        super(FadeTranBox, self).__init__(**kwargs)

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

class Inventory(FadeTranBox):

    inventory = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Inventory, self).__init__(**kwargs)

class AtkList(FadeTranBox):

    atkList = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(AtkList, self).__init__(**kwargs)

class EnemyList(FadeTranBox):

    enemyList = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(EnemyList, self).__init__(**kwargs)

class Container(FadeTranBox):

    def __init__(self, **kwargs):
        super(Container, self).__init__(**kwargs)
        self.converter = lambda row_index, rec: {
                'text': rec['name'],
                'size_hint_y': None,
                'height': 20,
                'deselected_color': [.5,.5,.5,1],
                'selected_color': [0,0,1,.2],
                'font_name': 'Pixel',
                'font_size': 15
                }
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
        self.lastHotKey = []
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

    def allowHotKey(self, dt):
        self.permission = True

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        global player
        keyNum, keyStr = keycode
        self.ctrl = (keyStr == 'ctrl') or ('ctrl' in modifiers)
        if self.readonly:
            if self.mode and (keyStr in ('up', 'down', 'enter') or self.ctrl):
                self.readonly = False
            else:
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
                    self.textinput.focus = False
                self.focus = True
        elif keyStr in ('0', '1', '2', '3', '4', '5') and self.battleMode and self.permission:
            self.permission = False
            try:
                if keyStr == '0':
                    player.checkEm('run')
                elif player.tF:
                    if self.ctrl:
                        player.checkEm(player.invNames[int(keyStr) - 1])
                    else:
                        player.checkEm(player.atkList[int(keyStr) - 1])
                else:
                    player.checkEm(player.enemyNames[int(keyStr) - 1])
                Clock.schedule_once(self.allowHotKey, .25)
            except IndexError:
                player.arenaInstance.report('Hotkey unavailable.')
                return
        elif keyStr == 'i' and self.ctrl and self.permission:
            if self.memoryStat:
                app.textRec.mode = 'upStat'
                self.playerInfo.upStatUsr.focus = True
                self.playerInfo.hint.text = 'Do you want to keep these changes?'
                self.lastHotKey = [window, keycode, text, modifiers]
                return
            self.permission = False
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
            Clock.schedule_once(self.allowHotKey, .25)
        elif keyStr == 'a' and self.ctrl and self.permission:
            if self.memoryStat:
                app.textRec.mode = 'upStat'
                self.playerInfo.upStatUsr.focus = True
                self.playerInfo.hint.text = 'Do you want to keep these changes?'
                self.lastHotKey = [window, keycode, text, modifiers]
                return
            self.permission = False
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
            Clock.schedule_once(self.allowHotKey, .25)
        elif keyStr == 'e' and self.ctrl and self.permission:
            if self.memoryStat:
                app.textRec.mode = 'upStat'
                self.playerInfo.upStatUsr.focus = True
                self.playerInfo.hint.text = 'Do you want to keep these changes?'
                self.lastHotKey = [window, keycode, text, modifiers]
                return
            self.permission = False
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
            Clock.schedule_once(self.allowHotKey, .25)
        elif keyStr == 'u' and self.ctrl and not self.battleMode and self.permission:
            if self.memoryStat:
                app.textRec.mode = 'upStat'
                self.playerInfo.upStatUsr.focus = True
                self.playerInfo.hint.text = 'Do you want to keep these changes?'
                self.lastHotKey = [window, keycode, text, modifiers]
                return
            self.permission = False
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
            Clock.schedule_once(self.allowHotKey, .25)
        elif keyStr == 's' and self.mode == 'playerInfo' and self.ctrl:
            if self.memoryStat:
                if 'upStat' != app.textRec.mode:
                    app.textRec.mode = 'upStat'
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
        elif 'ctrl' not in modifiers and 'lctrl' not in modifiers and 'rctrl' not in modifiers:
            if keyStr not in ('0', '1', '2', '3', '4', '5') or not self.battleMode:
                super(UsrInput, self).keyboard_on_key_down(window, keycode, text, modifiers)

    def selectItem(self, *containers, **kwargs):
        string = kwargs.pop('string', '')
        self.readonly = True
        if not string:
            self.readonly = False
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
                app.textRec.mode = ''
                self.focus = True
                break
            elif answer in ('no', 'nah', 'nope', 'n'):
                for s in self.memoryStat:
                    player.upStats[s][0] -= self.memoryStat[s]
                    player.upgradeStat(s, True)
                self.screen.updatePlayerInfo()
                self.memoryStat.clear()
                self.playerInfo.hint.text = 'Upgrade has been reversed.'
                app.textRec.mode = ''
                self.selectPlayerInfo()
                self.focus = True
                break
        if not strings:
            self.playerInfo.hint.text = 'That was a yes or no question!!'
            self.playerInfo.upStatUsr.focus = True
        elif self.lastHotKey:
            window, keycode, text, modifiers = self.lastHotKey
            self.lastHotKey = []
            self.keyboard_on_key_down(window, keycode, text, modifiers)

class Menu(FadeScreen):
    pass

class DungeonGame(App):
    """
    this is the actual instance of the app, doesn't do much
    but set up the screens and screenmanager
    """

    def __init__(self, **kwargs):
        super(DungeonGame, self).__init__(**kwargs)
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
        sm.add_widget(ChooseClass(name = 'chooseclass'))
        sm.add_widget(GameScreen(name = 'gamescreen'))
        sm.add_widget(Menu(name = 'menu'))
        return sm

if __name__ == '__main__':
    player = None
    data = JsonStore('data.json')
    audio = SoundLoader()
    typing = audio.load('../audio/typingSound.wav')
    typing.loop = True
    app = DungeonGame()
    app.run()
