import random
import os
import time
import tkinter as tk


class Experiment_Configuration():
    def __init__(self,root_screen):
        self.root_screen = root_screen
        self.main_run = tk.Toplevel()

        self.title = tk.Label(self.main_run,text='vPRL Protocol Setup')
        self.title.grid(row=0,column=1)

        self.trial_max_label = tk.Label(self.main_run,text='Maximum Trials:')
        self.trial_max_label.grid(row=1,column=0)

        self.trial_max_input = tk.Entry(self.main_run)
        self.trial_max_input.grid(row=1,column=2)
        self.trial_max_input.insert(tk.END,'500')

        self.reward_prob_label = tk.Label(self.main_run,text='Probability of Reward for S+ (0-1 decimal):')
        self.reward_prob_label.grid(row=2,column=0)

        self.reward_prob_input = tk.Entry(self.main_run)
        self.reward_prob_input.grid(row=2,column=2)
        self.reward_prob_input.insert(tk.END,'1')

        self.reversal_threshold_label = tk.Label(self.main_run,text='Reversal Threshold:')
        self.reversal_threshold_label.grid(row=3,column=0)

        self.reversal_threshold_input = tk.Entry(self.main_run)
        self.reversal_threshold_input.grid(row=3,column=2)
        self.reversal_threshold_input.insert(tk.END, '8')

        self.trial_max_reversal_label = tk.Label(self.main_run,text='Maximum Reversals:')
        self.trial_max_reversal_label.grid(row=4,column=0)

        self.trial_max_reversal_input = tk.Entry(self.main_run)
        self.trial_max_reversal_input.grid(row=4,column=2)
        self.trial_max_reversal_input.insert(tk.END,'9')

        self.session_max_label = tk.Label(self.main_run,text='Maximum Session Length:')
        self.session_max_label.grid(row=5,column=0)

        self.session_max_input = tk.Entry(self.main_run)
        self.session_max_input.grid(row=5,column=2)
        self.session_max_input.insert(tk.END,'3600')

        self.id_entry_label = tk.Label(self.main_run, text='Subject ID:')
        self.id_entry_label.grid(row=6,column=0)

        self.id_entry_input = tk.Entry(self.main_run)
        self.id_entry_input.grid(row=6,column=2)

        self.execute_button = tk.Button(self.main_run,text='Execute',command=self.start_protocol)
        self.execute_button.grid(row=7,column=1)

    def start_protocol(self):
        self.trial_max = float(self.trial_max_input.get())
        self.reversal_threshold = float(self.reversal_threshold_input.get())
        self.reward_prob = float(self.reward_prob_input.get())
        self.reward_prob = round(self.reward_prob,2)
        self.session_max = float(self.session_max_input.get())
        self.id_entry = self.id_entry_input.get()
        self.max_reversal = float(self.trial_max_reversal_input.get())
        self.parameters = [self.trial_max, self.session_max, self.reversal_threshold, self.max_reversal, self.reward_prob,
                           self.id_entry]
        self.root_screen.destroy()

        import Protocols as pr

        pr.Route_Switch('vPRL',self.parameters)
