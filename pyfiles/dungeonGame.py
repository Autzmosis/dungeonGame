#! /usr/bin/python3.4

"""
Yet to be named dungeonGame
coded by Daemonic

This program is the gui file for the program. All gui elements will be found
here.
"""

from tkinter import *
from tkinter import ttk
import time
from threading import Thread

class dungeonGame(object):
    
    def __init__(self, master):
        self.master = master

        self.wnframe = Frame(self.master, height = 480, width = 640,
                             bg ='black')

        self.ssbackground = PhotoImage(file = '../media/ssbackground.png')
        self.backlabel = Label(self.wnframe, image = self.ssbackground)
        self.backlabel.image = self.ssbackground #reference for background

        self.title = Label(self.wnframe, background = 'black',
                           foreground = 'white', text = 'DUNGEONS AND TOWNS',
                           font = ('FreeMono', 36, 'underline'), height = 0)

        self.hint = StringVar()
        self.entryhint = Label(self.wnframe, textvariable = self.hint,
                               font = ('FreeMono', 14), foreground = 'white',
                               background = 'black')
        self.entry = Entry(self.wnframe, width = 15, foreground = 'white',
                           background = 'black', insertbackground = 'white')

        self.warrior = PhotoImage(file = '../media/gem5.png')
        self.rogue = PhotoImage(file = '../media/gem6.png')
        self.mage = PhotoImage(file = '../media/gem7.png')
        
        self.charac = PhotoImage(file = '../media/boy.png')
        self.pet = PhotoImage(file = '../media/cat.png')
        self.background = PhotoImage(file = '../media/flippybackground.png')


        self.titlecc = Label(self.wnframe, background = 'black',
                             foreground = 'white', text = 'CHOOSE YOUR CLASS',
                             font = ('FreeMono', 22, 'underline'))

        self.frame = Frame(self.wnframe, bg = 'black')
        self.roframe = Frame(self.frame, bg = 'white', relief = SOLID,
                             borderwidth = 2, highlightthickness = 2,
                             width = 180, height = 250)
        self.waframe = Frame(self.frame, bg = 'white', relief = SOLID,
                             borderwidth = 2, highlightthickness = 2,
                             width = 180, height = 250)
        self.maframe = Frame(self.frame, bg = 'white', relief = SOLID,
                             borderwidth = 2, highlightthickness = 2,
                             width = 180, height = 250)

        self.rotext = 'Rogue'
        self.watext = 'Warrior'
        self.matext = 'Mage'

        self.rotext2 = ('Born with nothing\nand skilled in\nthe art of deciet,\n'
                        'seeks nothing, but\nwealth.')
        self.watext2 = ('Child of a king\nand bored of the\ncomfortable life,\n'
                        'journeys to seek\nglory in battle.')
        self.matext2 = ('Child prodigy,\nfeared by the\nignorant, journeys\n'
                        'in search of \npurpose in life.')

        self.rolabel = Label(self.roframe, text = self.rotext,
                             font = ('FreeMono', 16, 'underline'),
                             image = self.rogue, compound = TOP,
                             foreground = 'black', background = 'white')
        self.walabel = Label(self.waframe, text = self.watext,
                             font = ('FreeMono', 16, 'underline'),
                             image = self.warrior, compound = TOP,
                             foreground = 'black', background = 'white')
        self.malabel = Label(self.maframe, text = self.matext,
                             font = ('FreeMono', 16, 'underline'),
                             image = self.mage, compound = TOP,
                             foreground = 'black', background = 'white')

        self.rolabel2 = Label(self.roframe, text = self.rotext2,
                              font = ('FreeMono', 11), foreground = 'black',
                              background = 'white')
        self.walabel2 = Label(self.waframe, text = self.watext2,
                              font = ('FreeMono', 11), foreground = 'black',
                              background = 'white')
        self.malabel2 = Label(self.maframe, text = self.matext2,
                              font = ('FreeMono', 11), foreground = 'black',
                              background = 'white')

        self.hintcc = StringVar()
        self.hintcc.set('Type the name of the class you want and press enter.')
        self.entryhintcc = Label(self.wnframe, textvariable = self.hintcc,
                                 font = ('FreeMono', 11), foreground = 'white',
                                 background = 'black')
        self.entrycc = Entry(self.wnframe, width = 10, foreground = 'white',
                             background = 'black', insertbackground = 'white')

        self.infoframe = Frame(self.wnframe, width = 180, bg ='black')
        self.chartext = StringVar()
        self.chartext.set(':\nHP: -/-      SP: -/-\nEXP: -/-')
        self.petext = 'Abilities for pet:\nWill be written\n here.'
        self.atklist = 'Attack List:\nSmokescreen\nBackstab\nThrow'
        self.inventory = 'Recent Items:\nPotion\nSomething\nSomething else'
        self.charlabel = ttk.Label(self.infoframe, image = self.charac,
                                   textvariable = self.chartext,
                                   compound = 'top', justify = CENTER,
                                   background = 'black', foreground = 'white')
        self.petlabel = ttk.Label(self.infoframe, image = self.pet,
                                  text = self.petext, justify = CENTER,
                                  compound = 'top', background = 'black',
                                  foreground = 'white')
        self.atklabel = ttk.Label(self.infoframe, text = self.atklist,
                                  justify = CENTER, background = 'black',
                                  foreground = 'white')
        self.invlabel = ttk.Label(self.infoframe, text = self.inventory,
                                  justify = CENTER, background = 'black',
                                  foreground = 'white')

        self.backioframe = Frame(self.wnframe, width = 460, bg ='black')
        self.backframe = Frame(self.backioframe, height = 200, width = 460,
                               bg = 'black')
        self.labelback = ttk.Label(self.backframe, image = self.background,
                                   text = 'Background', compound = 'center',
                                   background ='black')
        self.text = Text(self.backioframe, height = 15, background = 'black',
                         foreground = 'white', highlightthickness=0)
        self.entrygp = Entry(self.backioframe, bg = 'black',
                             foreground = 'white', insertbackground = 'white',
                             disabledbackground = 'black')


        self.original = ''
        
        self.wnframe.pack(fill = BOTH, expand = True)
        self.wnframe.pack_propagate(False)
        
        self.backlabel.place(x = 0, y = 0, relwidth = 1, relheight = 1)
        
        self.startScreen()

    def startScreen(self):
        for child in self.wnframe.winfo_children():
            child.pack_forget()
            
        self.master.update_idletasks()
        self.entry.delete(0, END)
        
        self.title.pack(pady = 100)
        
        self.hint.set('Type, \'new game\' or \'continue\' and press enter.')
        self.entryhint.pack(pady = 5)
        self.entry.pack()
        self.entry.bind('<Return>', self.transitionsscc)

    def transitionsscc(self, event):
        self.original = str(self.chartext.get())
        if self.entry.get() == 'new game':
            self.chooseClass()
        elif self.entry.get() == 'continue':
            self.chartext.set('Rogue' + str(self.chartext.get()))
            self.gamePlay()
        else:
            self.hint.set('Please type either \'new game\' or \'continue\'.')
            self.entry.delete(0, END)

    def chooseClass(self):
        for child in self.wnframe.winfo_children():
            child.pack_forget()
            
        self.master.update_idletasks()
        self.entrycc.delete(0, END)

        self.titlecc.pack(pady = 30)

        self.frame.pack(pady = 20)

        self.roframe.pack(side = LEFT)
        self.waframe.pack(padx = 20, side = LEFT)
        self.maframe.pack(side = LEFT)

        self.roframe.pack_propagate(False)
        self.waframe.pack_propagate(False)
        self.maframe.pack_propagate(False)

        self.rolabel.pack(pady = 10)
        self.walabel.pack(pady = 10)
        self.malabel.pack(pady = 10)

        self.rolabel2.pack(pady = 5)
        self.walabel2.pack(pady = 5)
        self.malabel2.pack(pady = 5)

        self.entryhintcc.pack(pady = 5)
        self.entrycc.pack()
        self.entrycc.bind('<Return>', self.transitionccgp)

    def transitionccgp(self, event):
        choice = ('rogue', 'Rogue', 'warrior', 'Warrior', 'mage', 'Mage')
        c = 0
        for x in choice:
            if self.entrycc.get() == x:
                word = x[0].upper() + x[1:]
                self.chartext.set(word + str(self.chartext.get()))
                self.gamePlay()
            elif c == 5: #after check, notify user
                self.hintcc.set('Please type one of the class names.')
                self.entrycc.delete(0, END)
            c += 1

    def gamePlay(self):
        for child in self.wnframe.winfo_children():
            child.pack_forget()
            
        self.master.update_idletasks()

        self.entrygp.config(state = 'normal')
        self.text.config(state = 'normal')
        self.text.delete('1.0', 'end')
        self.text.config(state = 'disabled')
        self.entrygp.delete(0, END)
        
        self.infoframe.pack(side = LEFT, fill = BOTH, expand = True)
        self.infoframe.pack_propagate(False)
        self.charlabel.pack(padx = 35, fill = BOTH, expand = True)
        self.petlabel.pack(padx = 35, fill = BOTH, expand = True)
        self.atklabel.pack(padx = 35, fill = BOTH, expand = True)
        self.invlabel.pack(padx = 35, fill = BOTH, expand = True)

        self.backioframe.pack(side = LEFT, fill = BOTH, expand = True)
        self.backioframe.pack_propagate(False)
        self.backframe.pack(fill = BOTH, expand = True)
        self.labelback.config(font = ('Arial', 18))
        self.labelback.pack(fill = BOTH, expand = True)

        self.text.pack(pady = 3, fill = BOTH, expand = True)
        self.entrygp.pack(pady=1, fill = BOTH, expand = True)

        thread = Thread(None, self.prompt, 'thread',
                        ('Welcome to the world of dungeons and towns!', 0))
        thread.daemon = True
        thread.start()
        self.text.config(state = 'disabled')

        self.entrygp.bind('<Return>', self.usrinput)
            
    def usrinput(self, event):
        if self.entrygp.get() == '':
            return 0
        elif self.entrygp.get() == 'refresh()':
            self.entrygp.config(state = 'disabled')
            self.gamePlay()
        elif self.entrygp.get() == 'startScreen()':
            self.chartext.set(self.original)
            self.startScreen()
        else:
            self.text.config(state = 'normal')
            self.text.insert(END, '\n>>> ' + self.entrygp.get())
            self.text.config(state = 'disabled')
            self.entrygp.delete(0, END)
            x = 'This is a test prompt, watch me go.'
            #self.dictionaryCheck(self.entrygp.get(),
            #name of dictionary to check)
            self.prompt(x, 1)
    
    def prompt(self, string, state):
        self.entrygp.config(state = 'disabled')
        self.text.config(state = 'normal')
        length = len(string)
        for y in range(0, length):
            if state == 0 and y == 0:
                self.text.insert(END, '>>> ' + string[y])
                state = 1
            elif y == 0:
                self.text.insert(END, '\n' + '>>> ')
                self.text.insert(END, string[y])
            else:
                self.text.insert(END, string[y])
            time.sleep(.05)
            self.text.yview(END)
            self.master.update_idletasks()
        self.text.config(state = 'disabled')
        self.entrygp.config(state = 'normal')

    def displayAtkList(self, character_class):
        pass

    def displayInventory(self, itemlist):
        pass

    def dictionaryCheck(self, responce, dictionary):
        pass

    def Arena(self, character, enemy):
        pass

    

def main():
    root = Tk()
    root.wm_title('dungeonGame basic GUI')
    run = dungeonGame(root)
    root.mainloop()

if __name__ == '__main__': main()
