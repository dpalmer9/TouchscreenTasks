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

        self.title = tk.Label(self.configure_screen,text='iCPT2 Protocol Setup')
        self.title.grid(row=0,column=1)

        self.trial_max_label = tk.Label(self.configure_screen,text='Maximum Trials:')
        self.trial_max_label.grid(row=1,column=0)

        self.trial_max_input = tk.Entry(self.configure_screen)
        self.trial_max_input.grid(row=1,column=2)
        self.trial_max_input.insert(tk.END,'3000')

        self.block_max_label = tk.Label(self.configure_screen,text='Block Length:')
        self.block_max_label.grid(row=2,column=0)

        self.block_max_input = tk.Entry(self.configure_screen)
        self.block_max_input.grid(row=2,column=2)
        self.block_max_input.insert(tk.END,'40')

        self.block_count_label = tk.Label(self.configure_screen,text='# of Blocks:')
        self.block_count_label.grid(row=3,column=0)

        self.block_count_input = tk.Entry(self.configure_screen)
        self.block_count_input.grid(row=3,column=2)
        self.block_count_input.insert(tk.END,'3')

        self.stimulus_duration_label = tk.Label(self.configure_screen,text="Stimulus Duration (sec): ")
        self.stimulus_duration_label.grid(row=4,column=0)

        self.stimulus_duration_input = tk.Entry(self.configure_screen)
        self.stimulus_duration_input.grid(row=4,column=2)
        self.stimulus_duration_input.insert(tk.END,'0.4')

        self.limited_hold_label = tk.Label(self.configure_screen,text="Limited Hold (sec): ")
        self.limited_hold_label.grid(row=5,column=0)

        self.limited_hold_input = tk.Entry(self.configure_screen)
        self.limited_hold_input.grid(row=5,column=2)
        self.limited_hold_input.insert(tk.END,"0.3")

        self.target_prob_label = tk.Label(self.configure_screen,text="Target Probability (0-1): ")
        self.target_prob_label.grid(row=6,column=0)

        self.target_prob_input = tk.Entry(self.configure_screen)
        self.target_prob_input.grid(row=6,column=2)
        self.target_prob_input.insert(tk.END,"0.5")

        self.session_max_label = tk.Label(self.configure_screen,text='Maximum Session Length (sec): ')
        self.session_max_label.grid(row=7,column=0)

        self.session_max_input = tk.Entry(self.configure_screen)
        self.session_max_input.grid(row=7,column=2)
        self.session_max_input.insert(tk.END,'3600')

        self.probe_label = tk.Label(self.configure_screen,text='Probe Options:')
        self.probe_label.grid(row=8,column=1)

        self.probe_stimdur_check = tk.Checkbutton(self.configure_screen,text='Stimulus Duration', variable=self.probe_stimdur_var,onvalue=1, offvalue=0)
        self.probe_stimdur_check.grid(row=9,column=0)

        self.probe_iti_check = tk.Checkbutton(self.configure_screen,text='ITI', variable=self.probe_iti_var,onvalue=1, offvalue=0)
        self.probe_iti_check.grid(row=9,column=2)

        self.probe_contrast_check = tk.Checkbutton(self.configure_screen,text='Contrast', variable=self.probe_contrast_var,onvalue=1, offvalue=0)
        self.probe_contrast_check.grid(row=10,column=0)

        self.probe_flanker_check = tk.Checkbutton(self.configure_screen,text='Flanker', variable=self.probe_flanker_var,onvalue=1, offvalue=0)
        self.probe_flanker_check.grid(row=10,column=2)

        self.id_entry_label = tk.Label(self.configure_screen, text='Subject ID:')
        self.id_entry_label.grid(row=11,column=0)

        self.id_entry_input = tk.Entry(self.configure_screen)
        self.id_entry_input.grid(row=11,column=2)

        self.execute_button = tk.Button(self.configure_screen,text='Execute',command=self.start_protocol)
        self.execute_button.grid(row=12,column=1)

    def start_protocol(self):
        self.trial_max = float(self.trial_max_input.get())
        self.session_max = float(self.session_max_input.get())
        self.block_max = float(self.block_max_input.get())
        self.block_count = float(self.block_count_input.get())
        self.stimulus_duration = float(self.stimulus_duration_input.get())
        self.limited_hold = float(self.limited_hold_input.get())
        self.target_prob = float(self.target_prob_input.get())
        self.probe_check = [self.probe_stimdur_var.get(),self.probe_iti_var.get(),self.probe_contrast_var.get(),self.probe_flanker_var.get()]
        self.id_entry = self.id_entry_input.get()
        self.parameters = [self.trial_max,self.session_max,self.block_max,self.block_count,self.stimulus_duration,self.limited_hold,self.target_prob,self.probe_check,self.id_entry]
        self.root_screen.destroy()

        import Protocols as pr

        pr.Route_Switch('iCPT2',self.parameters)

