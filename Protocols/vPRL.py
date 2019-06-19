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
import os
import time
import tkinter as tk


class Experiment_Configuration():
    def __init__(self):
        self.main_run = tk.Tk()

        self.title = tk.Label(self.main_run,text='iCPT Protocol Setup')
        self.title.grid(row=0,column=1)

        self.trial_max_label = tk.Label(self.main_run,text='Maximum Trials:')
        self.trial_max_label.grid(row=1,column=0)

        self.trial_max_input = tk.Entry(self.main_run)
        self.trial_max_input.grid(row=1,column=2)

        self.session_max_label = tk.Label(self.main_run,text='Maximum Session Length:')
        self.session_max_label.grid(row=2,column=0)

        self.session_max_input = tk.Entry(self.main_run)
        self.session_max_input.grid(row=2,column=3)

        self.id_entry_label = tk.Label(self.main_run, text='Subject ID:')
        self.id_entry_label.grid(row=3,column=0)

        self.id_entry_input = tk.Entry(self.main_run)
        self.id_entry_input.grid(row=3,column=3)

        self.execute_button = tk.Button(self.main_run,text='Execute',command=self.start_protocol)
        self.execute_button.grid(row=4,column=1)

    def start_protocol(self):
        self.trial_max = float(self.trial_max_input.get())
        self.session_max = float(self.session_max_input.get())
        self.id_entry = self.id_entry_input.get()
        self.main_run.destroy()
        self.monitor_x_dim = GetSystemMetrics(0)
        self.monitor_y_dim = GetSystemMetrics(1)
        Window.size = (self.monitor_x_dim, self.monitor_y_dim)
        Window.fullscreen = True
        self.main_app = Experiment_App()
        self.main_app.set(trial_max=self.trial_max,session_max = self.session_max, id_entry = self.id_entry)
        self.main_app.run()



class ImageButton(ButtonBehavior,Image):
    def __init__(self,**kwargs):
        super(ImageButton,self).__init__(**kwargs)

class Experiment_Staging(FloatLayout):
    def __init__(self,**kwargs):
        super(Experiment_Staging,self).__init__(**kwargs)
        self.monitor_x_dim = GetSystemMetrics(0)
        self.monitor_y_dim = GetSystemMetrics(1)
        self.size = (self.monitor_x_dim,self.monitor_y_dim)

        self.curr_dir = os.getcwd()
        self.trial_displayed = False
        self.data_dir = self.curr_dir + "\\Data"
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        self.current_stage = 1
        self.next_stage = 1
        self.stage_executed = False

        self.presentation_delay_start = False
        self.image_on_screen = False
        self.feedback_displayed = False

        self.delay_length = 4

        self.max_trials = 72
        self.max_time = 3600

        self.current_trial = 1
        self.current_stage = 1
        self.time_elapsed = 0
        self.start_time = time.time()
        self.start_iti_time = 0

        self.total_correct = 0

        self.iti_time = 1
        self.presentation_delay_time = 1
        self.feedback_length = 1
        self.stimulus_duration = 1

        self.image_list = ['left','right']
        self.image_pos = [-1,1]
        self.image_one_selected = random.randint(0,1)


        self.image_two_selected = random.randint(0,1)

        while self.image_one_selected == self.image_two_selected:
            self.image_two_selected = random.randint(0,1)

        self.image_one_probability = random.randint(1,10)
        self.image_one_reward_threshold = 0
        self.image_two_probability = random.randint(1,10)
        self.image_two_reward_threshold = 0

        self.reversal_threshold = 8

        self.start_condition = random.randint(0,1)

        if self.start_condition == 0:
            self.image_one_reward_threshold = 8
            self.image_two_reward_threshold = 2
        else:
            self.image_one_reward_threshold = 2
            self.image_two_reward_threshold = 8



        self.lat = 0
        self.init_lat = 0

        self.current_correct = 0
        self.current_correction = 0

        self.delay_hold_button = ImageButton(source='%s\\Images\\white.png' % (self.curr_dir), allow_stretch=True)
        self.delay_hold_button.size_hint = (.16,.16)
        self.delay_hold_button.pos = ((self.center_x - (0.08 * self.monitor_x_dim)),(self.center_y - (0.08 * self.monitor_y_dim) - (0.4 * self.monitor_y_dim)))

        self.current_score = 0000
        self.scoreboard_wid = Label(text = '%s' % (self.current_score), font_size='30sp')
        self.scoreboard_wid.size_hint = (.3,.3)
        self.scoreboard_wid.pos = ((self.center_x - (0.15 * self.monitor_x_dim)),(self.center_y - (0.15*self.monitor_y_dim) + (0.3*self.monitor_y_dim)))


        Clock.schedule_interval(self.clock_update, 0.001)
        self.id_entry()



    def id_entry(self):
        self.id_instruction = Label(text = 'Please enter a participant ID #:')
        self.id_instruction.size_hint = (.5,.2)
        self.id_instruction.pos = ((self.center_x - (0.25 * self.monitor_x_dim)),(self.center_y - (0.1*self.monitor_y_dim) + (0.3*self.monitor_y_dim)))

        self.id_entry = TextInput(text='', multiline=False)
        self.id_entry.size_hint = (.3,.1)
        self.id_entry.pos = ((self.center_x - (0.15 * self.monitor_x_dim)),(self.center_y - (0.05*self.monitor_y_dim) + (-0.3*self.monitor_y_dim)))


        self.id_button = Button(text='OK')
        self.id_button.size_hint = (.1,.1)
        self.id_button.pos = ((self.center_x - (0.05 * self.monitor_x_dim)),(self.center_y - (0.05*self.monitor_y_dim) + (-0.4*self.monitor_y_dim)))
        self.id_button.bind(on_press = self.clear_id)

        self.add_widget(self.id_instruction)
        self.add_widget(self.id_entry)
        self.add_widget(self.id_button)

    def clear_id(self,*args):
        self.id_no = self.id_entry.text
        self.id_entry.hide_keyboard()

        self.participant_data_path = self.data_dir + '\\%s.csv' % (self.id_no)
        self.data_col_names = 'TrialNo,Correct,Rewarded,Response Latency'
        self.data_file = open(self.participant_data_path, "w+")
        self.data_file.write(self.data_col_names)
        self.data_file.close()

        self.remove_widget(self.id_instruction)
        self.remove_widget(self.id_entry)
        self.remove_widget(self.id_button)
        self.instruction_presentation()

    def instruction_presentation(self):
        self.instruction_label = Label(text= 'To initiate trials, press the white button.\nTo make a response, press on one of the images on the screen.\nYou will receive feedback following a response.'
                                       , font_size = '40sp')
        self.instruction_label.size_hint = (.5,.2)
        self.instruction_label.pos = ((self.center_x - (0.25 * self.monitor_x_dim)),(self.center_y - (0.1*self.monitor_y_dim) + (0.2*self.monitor_y_dim)))

        self.initiate_button = Button(text='Press to Start')
        self.initiate_button.size_hint = (.1,.1)
        self.initiate_button.pos = ((self.center_x - (0.05 * self.monitor_x_dim)),(self.center_y - (0.05*self.monitor_y_dim) - (0.2*self.monitor_y_dim)))
        self.initiate_button.bind(on_press = self.clear_instruction)
        self.add_widget(self.instruction_label)
        self.add_widget(self.initiate_button)

    def clear_instruction(self,*args):
        self.remove_widget(self.instruction_label)
        self.remove_widget(self.initiate_button)
        self.start_time = time.time()
        self.trial_initiation()

    def trial_initiation(self):
        self.initiation_image_wid = ImageButton(source='%s\\Images\\white.png' % (self.curr_dir), allow_stretch=True)
        self.initiation_image_wid.size_hint = (.16,.16)
        self.initiation_image_wid.pos = ((self.center_x - (0.08 * self.monitor_x_dim)),(self.center_y - (0.08 * self.monitor_y_dim) - (0.4 * self.monitor_y_dim)))
        self.initiation_image_wid.bind(on_press= self.initiation_detected)
        self.add_widget(self.initiation_image_wid)
        self.add_widget(self.scoreboard_wid)
        self.initiation_start_time = time.time()

    def initiation_detected(self,*args):
        self.remove_widget(self.initiation_image_wid)
        self.delay_hold_button.bind(on_release= self.premature_response)
        self.add_widget(self.delay_hold_button)
        self.initiation_end_time = time.time()
        self.init_lat = self.initiation_end_time - self.initiation_start_time
        self.presentation_delay()

    def presentation_delay(self,*args):
        if self.presentation_delay_start == False:
            self.presentation_delay_start_time = time.time()
            Clock.schedule_interval(self.presentation_delay,0.01)
            self.presentation_delay_start = True
        if (self.current_time - self.presentation_delay_start_time) >= self.presentation_delay_time:
            Clock.unschedule(self.presentation_delay)
            self.delay_hold_button.unbind(on_release=self.premature_response)
            self.presentation_delay_start = False
            self.image_presentation()

    def image_presentation(self,*args):
        if self.image_on_screen == False:
            self.delay_hold_button.unbind(on_release=self.premature_response)

            self.one_image_wid = ImageButton(source='%s\\Images\\%s.png' % (self.curr_dir,self.image_list[0]), allow_stretch=True)
            self.one_image_wid.size_hint = (.3, .3)
            self.one_image_wid.pos = (
            (self.center_x - (0.15 * self.monitor_x_dim) + (0.15 * self.image_pos[self.image_one_selected] * self.monitor_x_dim)), (self.center_y - (0.15 * self.monitor_y_dim)))
            self.one_image_wid.bind(on_press= self.response_one)
            self.add_widget(self.one_image_wid)

            self.two_image_wid = ImageButton(source='%s\\Images\\%s.png' % (self.curr_dir,self.image_list[1]), allow_stretch=True)
            self.two_image_wid.size_hint = (.3, .3)
            self.two_image_wid.pos = (
            (self.center_x - (0.15 * self.monitor_x_dim) + (0.15 * self.image_pos[self.image_two_selected] * self.monitor_x_dim)), (self.center_y - (0.15 * self.monitor_y_dim)))
            self.two_image_wid.bind(on_press= self.response_two)
            self.add_widget(self.two_image_wid)


            self.image_pres_time = time.time()
            self.image_on_screen = True

    def response_one(self, *args):
        self.image_touch_time = time.time()
        self.remove_widget(self.one_image_wid)
        self.remove_widget(self.two_image_wid)

        self.lat = self.image_touch_time - self.image_pres_time

        if self.image_one_reward_threshold < self.image_two_reward_threshold:
            self.current_correct = 1
            self.total_correct += 1
        else:
            self.current_correct = 0

        if self.image_one_probability > self.image_one_reward_threshold:
            self.feedback_string = 'Reward'
            self.current_reward = 1
            self.current_score += 1
            self.scoreboard_wid.text = '%s' % (self.current_score)
        else:
            self.feedback_string = 'No Reward'
            self.current_reward = 0

        self.record_data()
        self.set_new_trial_configuration()
        self.feedback_report()
        self.delay_hold_button.bind(on_press=self.start_iti)

    def response_two(self, *args):
        self.image_touch_time = time.time()
        self.remove_widget(self.one_image_wid)
        self.remove_widget(self.two_image_wid)

        self.lat = self.image_touch_time - self.image_pres_time

        if self.image_one_reward_threshold > self.image_two_reward_threshold:
            self.current_correct = 1
            self.total_correct += 1
        else:
            self.current_correct = 0

        if self.image_two_probability > self.image_two_reward_threshold:
            self.feedback_string = 'Reward'
            self.current_reward = 1
            self.current_score += 1
            self.scoreboard_wid.text = '%s' % (self.current_score)
        else:
            self.feedback_string = 'No Reward'
            self.current_reward = 0

        self.record_data()
        self.set_new_trial_configuration()
        self.feedback_report()
        self.delay_hold_button.bind(on_press=self.start_iti)

    def premature_response(self,*args):
        if self.image_on_screen == True:
            return None
        Clock.unschedule(self.end_iti)
        Clock.unschedule(self.presentation_delay)
        if self.feedback_displayed == True:
            self.remove_widget(self.feedback_wid)

        self.image_on_screen = False
        self.feedback_string = 'WAIT FOR IMAGE - PLEASE TRY AGAIN'
        self.correction_active = True
        self.current_correct = 2
        self.lat = ''
        self.delay_hold_button.bind(on_press=self.start_iti)
        self.record_data()
        self.feedback_report()

    def record_data(self):
        self.data_file = open(self.participant_data_path, "a")
        self.data_file.write("\n")
        self.data_file.write("%s,%s,%s,%s" % (self.current_trial,self.current_correct,self.current_reward,self.lat))
        self.data_file.close()

        if self.current_correct == 0:
            self.current_correction = 1
        if self.current_correct == 1:
            self.current_correction = 0

    def set_new_trial_configuration(self):

        self.current_correction = 0
        self.current_trial += 1

        self.image_one_probability = random.randint(1, 10)
        self.image_two_probability = random.randint(1, 10)

        self.image_one_selected = random.randint(0,1)
        self.image_two_selected = random.randint(0,1)

        if (self.total_correct % self.reversal_threshold) == 0:
            if self.start_condition == 0:
                self.start_condition = 1
                self.image_one_reward_threshold = 2
                self.image_two_reward_threshold = 8
            elif self.start_condition == 1:
                self.start_condition = 0
                self.image_one_reward_threshold = 8
                self.image_two_reward_threshold = 2

        while self.image_one_selected == self.image_two_selected:
            self.image_two_selected = random.randint(0,1)





    def feedback_report(self,*args):
        self.feedback_displayed = True
        self.iti_clock_trigger = False
        self.feedback_wid = Label(text=self.feedback_string, font_size='50sp')
        self.feedback_wid.size_hint = (.5,.3)
        self.feedback_wid.pos = ((self.center_x - (0.25 * self.monitor_x_dim)),(self.center_y - (0.15*self.monitor_y_dim)))
        self.add_widget(self.feedback_wid)
        self.start_feedback_time = time.time()

    def start_iti(self,*args):
        self.delay_hold_button.unbind(on_press=self.start_iti)
        self.delay_hold_button.bind(on_release=self.premature_response)
        self.iti_clock_trigger = False
        self.image_on_screen = False
        self.end_iti()

    def end_iti(self,*args):
        if self.iti_clock_trigger == False:
            Clock.schedule_interval(self.end_iti, 0.01)
            self.start_iti_time = time.time()
            self.iti_clock_trigger = True
        if ((self.current_time - self.start_feedback_time) >= self.feedback_length) and (self.feedback_displayed == True):
            self.remove_widget(self.feedback_wid)
            self.start_iti_time = time.time()
            self.feedback_displayed = False
        if ((self.current_time - self.start_iti_time) >= self.iti_time) and self.feedback_displayed == False:
            Clock.unschedule(self.end_iti)
            self.image_presentation()



    def clock_update(self,*args):
        self.current_time = time.time()
        self.time_elapsed = time.time() - self.start_time

class Experiment_App(App):
    def build(self):
        experiment = Experiment_Staging()
        return experiment

if __name__ == '__main__':
    monitor_x_dim = GetSystemMetrics(0)
    monitor_y_dim = GetSystemMetrics(1)
    Window.size = (monitor_x_dim,monitor_y_dim)
    Window.fullscreen = True
    Experiment_App().run()