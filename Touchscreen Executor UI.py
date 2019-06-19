## Import Function ##
from tkinter import N
from tkinter import S
from tkinter import W
from tkinter import E
from tkinter import END
from tkinter import BROWSE
from tkinter import VERTICAL
import tkinter as tk
import os
import Protocols as pr
from Protocols import ImageButton
from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'systemandmulti')
#Config.set('graphics', 'fullscreen', '1')
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from win32api import GetSystemMetrics
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.uix.vkeyboard import VKeyboard
from functools import partial
import random


## TKinter-Object ##

class Touchscreen_UI():
    def __init__(self):
        self.main_path = os.getcwd()
        self.protocol_path = self.main_path + "\\Protocols\\"

        self.protocol_list = list()
        for file in os.listdir(self.protocol_path):
            if file.endswith(".py"):
                self.protocol_list.append(file)

        self.protocol_list = [protocol.replace('.py','') for protocol in self.protocol_list]

        self.main_run = tk.Tk()

        self.protocol_title = tk.Label(self.main_run, text='TouchCog Launcher v0-0-1')
        self.protocol_title.grid(row=0,column=1)

        self.author_title = tk.Label(self.main_run, text='Daniel Palmer,PhD')
        self.author_title.grid(row=1,column=1)

        self.protocol_listbox = tk.Listbox(self.main_run, selectmode=BROWSE)
        for protocol in self.protocol_list:
            self.protocol_listbox.insert(END, protocol)
        self.protocol_listbox.grid(row=2,column=0, sticky=(N,W,E,S))
        self.protocol_listbox_scroll = tk.Scrollbar(self.main_run, orient=VERTICAL, command=self.protocol_listbox.yview)
        self.protocol_listbox_scroll.grid(row=2,column=2,sticky=(N,S))
        self.protocol_listbox.configure(yscrollcommand=self.protocol_listbox_scroll.set)

        self.select_button = tk.Button(self.main_run, text='Select Protocol', command=self.protocol_selection)
        self.select_button.grid(row=3,column=1)

        self.main_run.mainloop()

    def protocol_selection(self):
        self.protocol_selected_pos = self.protocol_listbox.curselection()
        self.protocol_selected = self.protocol_listbox.get(self.protocol_selected_pos[0])
        pr.Route_Switch(self.protocol_selected)
        self.main_run.destroy()


main_window = Touchscreen_UI()