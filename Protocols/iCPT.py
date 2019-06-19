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
    def __init__(self,trial_max,session_max,id_entry,**kwargs):
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

        self.max_trials = trial_max
        self.max_time = session_max
        self.id_no = id_entry

        self.current_trial = 1
        self.current_total_hits = 0
        self.hit_threshold = 5
        self.current_stage = 1
        self.time_elapsed = 0
        self.start_time = time.time()
        self.start_iti_time = 0

        self.iti_time = 0.5
        self.presentation_delay_time = 1
        self.feedback_length = 0.5
        self.stimulus_duration = 0.5

        self.image_list = ['horizontal','horizontal','horizontal','horizontal','vertical','left','right','rings']
        self.image_list_pos = random.randint(0,7)

        self.contrast_list = ['','-50','-25','-125']
        self.contrast_list_pos = random.randint(0,3)
        self.image_name_contrast = '%s%s' % (
        self.image_list[self.image_list_pos], self.contrast_list[self.contrast_list_pos])

        self.distractor_active = random.randint(0,1)
        self.distractor_congruent = random.randint(0,1)
        if self.distractor_active == 1:
            if self.distractor_congruent == 0:
                if self.image_list[self.image_list_pos] == 'horizontal':
                    self.distractor_image_pos = random.randint(4, 7)
                else:
                    self.distractor_image_pos = 0
            elif self.distractor_congruent == 1:
                self.distractor_image_pos = self.image_list_pos

        self.stimulus_duration_list = [1,0.75,0.66,0.5]
        self.stimulus_duration_pos = random.randint(0,3)

        self.iti_duration_list = [0.5,1,2]
        self.iti_duration_pos = random.randint(0,2)

        self.lat = 0
        self.init_lat = 0

        self.current_correct = 0
        self.current_correction = 0

        self.delay_hold_button = ImageButton(source='%s\\Images\\white.png' % (self.curr_dir), allow_stretch=True)
        self.delay_hold_button.size_hint = (.16,.16)
        self.delay_hold_button.pos = ((self.center_x - (0.08 * self.monitor_x_dim)),(self.center_y - (0.08 * self.monitor_y_dim) - (0.4 * self.monitor_y_dim)))

        Clock.schedule_interval(self.clock_update, 0.001)
        self.id_setup()


    def id_setup(self):
        self.participant_data_folder = self.data_dir + '\\' + self.id_no + '\\'
        if os.path.exists(self.participant_data_folder) == False:
            os.makedirs(self.participant_data_folder)
        self.participant_data_path = self.participant_data_folder + 'iCPT %s.csv' % (self.id_no)
        self.data_col_names = 'TrialNo, Trial Type, Correction Trial, Correct, Response Latency'
        self.data_file = open(self.participant_data_path, "w+")
        self.data_file.write(self.data_col_names)
        self.data_file.close()

        self.instruction_presentation()

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
        self.data_col_names = 'TrialNo, Trial Type, Correction Trial, Correct, Response Latency'
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
            if self.current_stage == 2:
                self.image_wid = ImageButton(
                    source='%s\\Images\\%s.png' % (self.curr_dir, self.image_name_contrast),
                    allow_stretch=True)
            else:
                self.image_wid = ImageButton(source='%s\\Images\\%s.png' % (self.curr_dir,self.image_list[self.image_list_pos]), allow_stretch=True)
                
            self.image_wid.size_hint = (.3, .3)
            self.image_wid.pos = (
            (self.center_x - (0.15 * self.monitor_x_dim)), (self.center_y - (0.15 * self.monitor_y_dim)))
            self.image_wid.bind(on_press= self.image_pressed)
            if self.current_stage == 3 and self.distractor_active == 1:
                self.distractor_one_wid = ImageButton(source='%s\\Images\\%s.png' % (self.curr_dir,self.image_list[self.distractor_image_pos]), allow_stretch=True)
                self.distractor_one_wid.size_hint = (.3, .3)
                self.distractor_one_wid.pos = (
                    (self.center_x - (0.15 * self.monitor_x_dim) - (0.25 * self.monitor_x_dim)), (self.center_y - (0.15 * self.monitor_y_dim)))

                self.distractor_two_wid = ImageButton(
                    source='%s\\Images\\%s.png' % (self.curr_dir, self.image_list[self.distractor_image_pos]),
                    allow_stretch=True)
                self.distractor_two_wid.size_hint = (.3, .3)
                self.distractor_two_wid.pos = (
                    (self.center_x - (0.15 * self.monitor_x_dim) + (0.25 * self.monitor_x_dim)),
                    (self.center_y - (0.15 * self.monitor_y_dim)))

                self.add_widget(self.distractor_one_wid)
                self.add_widget(self.distractor_two_wid)
            self.add_widget(self.image_wid)
            self.image_pres_time = time.time()
            self.image_on_screen = True
            Clock.schedule_interval(self.image_presentation,0.01)
        if (self.current_time - self.image_pres_time) >= self.stimulus_duration:
            Clock.unschedule(self.image_presentation)
            self.feedback_string = ''
            self.remove_widget(self.image_wid)
            if self.current_stage == 3 and self.distractor_active == 1:
                self.remove_widget(self.distractor_one_wid)
                self.remove_widget(self.distractor_two_wid)
            if (self.image_list[self.image_list_pos] == 'horizontal'):
                self.current_correct = 0
            else:
                self.current_correct = 1
            self.lat = ''
            self.record_data()
            self.set_new_trial_configuration()
            self.start_iti()


    def image_pressed(self,*args):
        Clock.unschedule(self.image_presentation)
        self.remove_widget(self.image_wid)
        if self.current_stage == 3 and self.distractor_active == 1:
            self.remove_widget(self.distractor_one_wid)
            self.remove_widget(self.distractor_two_wid)
        if self.image_list[self.image_list_pos] == 'horizontal':
            self.response_correct()
        else:
            self.response_incorrect()


    def response_correct(self):
        self.image_touch_time = time.time()

        self.lat = self.image_touch_time - self.image_pres_time


        self.current_correct = 1
        self.current_total_hits += 1
        self.correction_active = False
        self.feedback_string = 'CORRECT'

        self.delay_hold_button.bind(on_press=self.start_iti)
        self.record_data()
        self.set_new_trial_configuration()
        self.feedback_report()




    def response_incorrect(self):
        self.image_touch_time = time.time()

        self.lat = self.image_touch_time - self.image_pres_time

        self.correction_active = True
        self.feedback_string = 'INCORRECT - PLEASE TRY AGAIN'


        self.current_correct = 0
        self.delay_hold_button.bind(on_press=self.start_iti)
        self.record_data()
        self.feedback_report()


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
        self.data_file.write("%s,%s,%s,%s,%s" % (self.current_trial,self.image_list[self.image_list_pos],self.current_correction,self.current_correct,self.lat))
        self.data_file.close()

        if self.current_correct == 0:
            self.current_correction = 1
        if self.current_correct == 1:
            self.current_correction = 0

    def set_new_trial_configuration(self):

        self.current_correction = 0

        self.image_list_pos = random.randint(0,7)


        self.current_trial += 1

        if self.current_total_hits >= self.hit_threshold:
            self.remove_widget(self.delay_hold_button)
            self.block_hold()
            return
        if self.current_stage == 2:
            self.contrast_list_pos = random.randint(0, 3)
            self.image_name_contrast = '%s%s' % (self.image_list[self.image_list_pos], self.contrast_list[self.contrast_list_pos])
        if self.current_stage == 3:
            self.distractor_active = random.randint(0,1)
            self.distractor_congruent = random.randint(0,1)
            if self.distractor_active == 1:
                if self.distractor_congruent == 0:
                    if self.image_list[self.image_list_pos] == 'horizontal':
                        self.distractor_image_pos = random.randint(4,7)
                    else:
                        self.distractor_image_pos = 0
                elif self.distractor_congruent == 1:
                    self.distractor_image_pos = self.image_list_pos
        if self.current_stage == 4:
            self.stimulus_duration_pos = random.randint(0,3)
            self.stimulus_duration = self.stimulus_duration_list[self.stimulus_duration_pos]
        if self.current_stage == 5:
            self.iti_duration_pos = random.randint(0,2)
            self.iti_time = self.iti_duration_list[self.iti_duration_pos]


    def block_hold(self,*args):
        self.current_stage += 1
        self.iti_time = 0.5
        self.presentation_delay_time = 0.5
        self.feedback_length = 0.5
        self.stimulus_duration = 0.5
        self.current_total_hits = 0
        self.current_trial -= 1

        self.block_instruction_wid = Label(text='PRESS BUTTON TO CONTINUE WHEN READY',font_size='50sp')
        self.block_instruction_wid.size_hint = (.5,.3)
        self.block_instruction_wid.pos = ((self.center_x - (0.25 * self.monitor_x_dim)),(self.center_y - (0.15*self.monitor_y_dim) + (0.3*self.monitor_y_dim)))

        self.block_button = Button(text='Continue')
        self.block_button.size_hint = (.2,.1)
        self.block_button.pos = ((self.center_x - (0.1 * self.monitor_x_dim)),(self.center_y - (0.05*self.monitor_y_dim) + (-0.4*self.monitor_y_dim)))
        self.block_button.bind(on_press = self.block_press)

        self.add_widget(self.block_instruction_wid)
        self.add_widget(self.block_button)

    def block_press(self,*args):
        self.remove_widget(self.block_instruction_wid)
        self.remove_widget(self.block_button)
        self.set_new_trial_configuration()
        self.add_widget(self.delay_hold_button)


    def feedback_report(self,*args):
        self.feedback_displayed = True
        self.iti_clock_trigger = False
        self.feedback_wid = Label(text=self.feedback_string, font_size='50sp')
        self.feedback_wid.size_hint = (.5,.3)
        self.feedback_wid.pos = ((self.center_x - (0.25 * self.monitor_x_dim)),(self.center_y - (0.15*self.monitor_y_dim)))
        if self.current_total_hits < self.hit_threshold:
            self.add_widget(self.feedback_wid)

    def start_iti(self,*args):
        self.delay_hold_button.unbind(on_press=self.start_iti)
        self.delay_hold_button.bind(on_release=self.premature_response)
        self.start_feedback_time = time.time()
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
        experiment = Experiment_Staging(trial_max=self.trial_maximum,session_max=self.session_maximum,id_entry=self.id_value)
        return experiment
    def set(self,trial_max,session_max,id_entry):
        self.trial_maximum = trial_max
        self.session_maximum = session_max
        self.id_value = id_entry
