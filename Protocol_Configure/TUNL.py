import random
import os
import time
import tkinter as tk


class Experiment_Configuration():
    def __init__(self,root_screen):
        self.main_run = tk.Toplevel()
        
        self.root_screen = root_screen

        self.title = tk.Label(self.main_run,text='TUNL Protocol Setup')
        self.title.grid(row=0,column=1)

        self.trial_max_label = tk.Label(self.main_run,text='Maximum Trials:')
        self.trial_max_label.grid(row=1,column=0)

        self.trial_max_input = tk.Entry(self.main_run)
        self.trial_max_input.grid(row=1,column=2)
        self.trial_max_input.insert(tk.END,'90')

        self.session_max_label = tk.Label(self.main_run,text='Maximum Session Length:')
        self.session_max_label.grid(row=2,column=0)

        self.session_max_input = tk.Entry(self.main_run)
        self.session_max_input.grid(row=2,column=2)
        self.session_max_input.insert(tk.END,'3600')
        
        self.block_length_label = tk.Label(self.main_run,text='Block Length:')
        self.block_length_label.grid(row=3,column=0)
        
        self.block_length_input = tk.Entry(self.main_run)
        self.block_length_input.grid(row=3,column=2)
        self.block_length_input.insert(tk.END,'30')
        
        self.block_count_label = tk.Label(self.main_run,text='Number of Blocks:')
        self.block_count_label.grid(row=4,column=0)
        
        self.block_count_input = tk.Entry(self.main_run)
        self.block_count_input.grid(row=4,column=2)
        self.block_count_input.insert(tk.END,'3')

        self.id_entry_label = tk.Label(self.main_run, text='Subject ID:')
        self.id_entry_label.grid(row=5,column=0)

        self.id_entry_input = tk.Entry(self.main_run)
        self.id_entry_input.grid(row=5,column=2)

        self.execute_button = tk.Button(self.main_run,text='Execute',command=self.start_protocol)
        self.execute_button.grid(row=6,column=1)

    def start_protocol(self):
        self.trial_max = float(self.trial_max_input.get())
        self.session_max = float(self.session_max_input.get())
        self.block_length = float(self.block_length_input.get())
        self.block_count = float(self.block_count_input.get())
        self.id_entry = self.id_entry_input.get()
        self.parameters = [self.trial_max,self.session_max,self.block_length,self.block_count,self.id_entry]
        
        self.root_screen.destroy()
        
        import Protocols as pr
        
        pr.Route_Switch('TUNL',self.parameters)


