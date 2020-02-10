
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
import Protocol_Configure as prc
import sys

## TKinter-Object ##

class Touchscreen_UI():
    def __init__(self):
        self.main_path = os.getcwd()
        self.protocol_path = self.main_path + "\\Protocols\\"

        #self.protocol_list = list()

        #for file in os.listdir(self.protocol_path):
            #if file.endswith(".py"):
                #self.protocol_list.append(file)

        #self.protocol_list = [protocol.replace('.py','') for protocol in self.protocol_list]

        self.protocol_list = ['iCPT','iCPTImage2','iCPTStimDurationScreen','iCPTImageScreen','iCPTStimImageScreen','vPRL','PAL','TUNL','PR']

        self.main_screen = tk.Tk()

        self.protocol_title = tk.Label(self.main_screen, text='TouchCog Launcher v0-1-0')
        self.protocol_title.grid(row=0,column=1)

        self.author_title = tk.Label(self.main_screen, text='Daniel Palmer,PhD')
        self.author_title.grid(row=1,column=1)

        self.protocol_listbox = tk.Listbox(self.main_screen, selectmode=BROWSE)
        for protocol in self.protocol_list:
            self.protocol_listbox.insert(END, protocol)
        self.protocol_listbox.grid(row=2,column=0, sticky=(N,W,E,S))
        self.protocol_listbox_scroll = tk.Scrollbar(self.main_screen, orient=VERTICAL, command=self.protocol_listbox.yview)
        self.protocol_listbox_scroll.grid(row=2,column=2,sticky=(N,S))
        self.protocol_listbox.configure(yscrollcommand=self.protocol_listbox_scroll.set)

        self.select_button = tk.Button(self.main_screen, text='Select Protocol', command=self.protocol_selection)
        self.select_button.grid(row=3,column=1)
        
        self.configure_button = tk.Button(self.main_screen,text='Configuration',command=self.configuration_menu)
        self.configure_button.grid(row=4,column=1)

        self.main_screen.mainloop()

    def protocol_selection(self):
        self.protocol_selected_pos = self.protocol_listbox.curselection()
        self.protocol_selected = str(self.protocol_listbox.get(self.protocol_selected_pos[0]))
        prc.Route_Switch(self.protocol_selected,self.main_screen)
        #self.main_run.destroy()
    
    def configuration_menu(self):
        if sys.platform == 'linux'or sys.platform == 'darwin':
            self.config_path = self.main_path + '/Configuration.ttconfig'
        elif sys.platform == 'win32':
            self.config_path = self.main_path + '\\Configuration.ttconfig'
            
        self.config_file = open(self.config_path,'r')
        self.configurations = self.config_file.readlines()
        self.x_dim = self.configurations[0]
        self.x_dim = self.x_dim.replace('x_dim = ','')
        self.x_dim = self.x_dim.replace('\n','')
        self.x_dim = int(self.x_dim)
        self.y_dim = self.configurations[1]
        self.y_dim = self.y_dim.replace('y_dim = ','')
        self.y_dim = self.y_dim.replace('\n','')
        self.y_dim = int(self.y_dim)
        self.fullscreen_var = tk.IntVar()
        self.fullscreen = self.configurations[2]
        self.fullscreen = self.fullscreen.replace('fullscreen = ','')
        self.fullscreen = self.fullscreen.replace('\n','')
        self.fullscreen = int(self.fullscreen)
        self.fullscreen_var.set(self.fullscreen)
        self.config_file.close()
        
        self.configuration_menu_top = tk.Toplevel() 
        
        self.configuration_title = tk.Label(self.configuration_menu_top,text='Configuration')
        self.configuration_title.grid(row=0,column=1)
        
        self.x_res_label = tk.Label(self.configuration_menu_top,text='X Resolution:')
        self.x_res_label.grid(row=1,column=0)
        
        self.x_res_field = tk.Entry(self.configuration_menu_top)
        self.x_res_field.grid(row=1,column=2)
        self.x_res_field.insert(tk.END,str(self.x_dim))
        
        self.y_res_label = tk.Label(self.configuration_menu_top,text='Y Resolution:')
        self.y_res_label.grid(row=2,column=0)
        
        self.y_res_field = tk.Entry(self.configuration_menu_top)
        self.y_res_field.grid(row=2,column=2)
        self.y_res_field.insert(tk.END,str(self.y_dim))
        
        self.fullscreen_checkbox = tk.Checkbutton(self.configuration_menu_top,text='Fullscreen',
                                                  variable=self.fullscreen_var)
        self.fullscreen_checkbox.grid(row=3,column=1)
        
        self.accept_button = tk.Button(self.configuration_menu_top,text='Accept',command=self.close_configuration)
        self.accept_button.grid(row=4,column=1)
        
    def close_configuration(self):
        self.x_dim = str(self.x_res_field.get())
        self.x_setting = 'x_dim = %s\n' % (self.x_dim)
        self.y_dim = str(self.y_res_field.get())
        self.y_setting = 'y_dim = %s\n' % (self.y_dim)
        self.fullscreen_set = str(self.fullscreen_var.get())
        self.fullscreen_setting = 'fullscreen = %s\n' % (self.fullscreen_set)
        self.settings = [self.x_setting,self.y_setting,self.fullscreen_setting]
        self.config_file = open(self.config_path,'w')
        self.config_file.writelines(self.settings)
        self.config_file.close()
        self.configuration_menu_top.destroy()


main_window = Touchscreen_UI()

