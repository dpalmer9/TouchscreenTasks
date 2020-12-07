import random
import os
import time
import tkinter as tk
from tkinter import ttk


class Experiment_Configuration():
    def __init__(self,root_screen):
        self.main_run = tk.Toplevel()
        
        self.root_screen = root_screen

        self.title = tk.Label(self.main_run,text='PRv2 Protocol Setup')
        self.title.grid(row=0,column=1)


        self.session_max_label = tk.Label(self.main_run,text='Maximum Session Length:')
        self.session_max_label.grid(row=1,column=0)

        self.session_max_input = tk.Entry(self.main_run)
        self.session_max_input.grid(row=1,column=2)
        self.session_max_input.insert(tk.END,'1200')
        
        self.reward_type_list = ['Points','Reward']
        
        self.reward_type_label = tk.Label(self.main_run,text='Reward Type:')
        self.reward_type_label.grid(row=2,column=0)
        
        self.reward_type_cb = ttk.Combobox(self.main_run,values=self.reward_type_list)
        self.reward_type_cb.grid(row=2,column=2)
        

        self.id_entry_label = tk.Label(self.main_run, text='Subject ID:')
        self.id_entry_label.grid(row=3,column=0)

        self.id_entry_input = tk.Entry(self.main_run)
        self.id_entry_input.grid(row=3,column=2)

        self.execute_button = tk.Button(self.main_run,text='Execute',command=self.start_protocol)
        self.execute_button.grid(row=4,column=1)

    def start_protocol(self):
        self.session_max = float(self.session_max_input.get())
        self.reward_type = int(self.reward_type_cb.current())
        self.id_entry = self.id_entry_input.get()
        self.parameters = [self.session_max,self.reward_type,self.id_entry]
        
        self.root_screen.destroy()
        
        import Protocols as pr
        
        pr.Route_Switch('PR2',self.parameters)


