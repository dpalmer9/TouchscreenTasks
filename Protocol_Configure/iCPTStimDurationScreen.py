import random
import os
import time
import tkinter as tk


class Experiment_Configuration():
    def __init__(self,root_screen):
        self.configure_screen = tk.Toplevel()

        self.root_screen = root_screen

        self.probe_stimdur_var = tk.IntVar()
        self.probe_iti_var = tk.IntVar()
        self.probe_contrast_var = tk.IntVar()
        self.probe_flanker_var = tk.IntVar()

        self.title = tk.Label(self.configure_screen,text='iCPTStimDurationScreen Protocol Setup')
        self.title.grid(row=0,column=1)

        self.trial_max_label = tk.Label(self.configure_screen,text='Maximum Trials:')
        self.trial_max_label.grid(row=1,column=0)

        self.trial_max_input = tk.Entry(self.configure_screen)
        self.trial_max_input.grid(row=1,column=2)
        self.trial_max_input.insert(tk.END,'3000')

        self.session_max_label = tk.Label(self.configure_screen,text='Maximum Session Length:')
        self.session_max_label.grid(row=4,column=0)

        self.session_max_input = tk.Entry(self.configure_screen)
        self.session_max_input.grid(row=4,column=2)
        self.session_max_input.insert(tk.END,'3600')

        self.id_entry_label = tk.Label(self.configure_screen, text='Subject ID:')
        self.id_entry_label.grid(row=8,column=0)

        self.id_entry_input = tk.Entry(self.configure_screen)
        self.id_entry_input.grid(row=8,column=2)

        self.execute_button = tk.Button(self.configure_screen,text='Execute',command=self.start_protocol)
        self.execute_button.grid(row=9,column=1)

    def start_protocol(self):
        self.trial_max = float(self.trial_max_input.get())
        self.session_max = float(self.session_max_input.get())
        self.id_entry = self.id_entry_input.get()
        self.parameters = [self.trial_max,self.session_max,self.id_entry]
        self.root_screen.destroy()

        import Protocols as pr

        pr.Route_Switch('iCPTStimDurationScreen',self.parameters)

