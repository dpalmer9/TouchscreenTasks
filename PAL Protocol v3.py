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

        self.iti_time = 1
        self.presentation_delay_time = 1
        self.feedback_length = 1
        self.stimulus_duration = 1

        self.image_list = ['horizontal','left','right']
        self.image_correct_pos = [0,-1,1]
        self.image_correct_selected = random.randint(0,2)

        self.image_incorrect_selected = random.randint(0,2)

        while self.image_correct_selected == self.image_incorrect_selected:
            self.image_incorrect_selected = random.randint(0,2)

        if self.image_incorrect_selected or self.image_correct_selected != 0:
            self.image_incorrect_position = 0
        elif self.image_incorrect_selected or self.image_correct_selected != 1:
            self.image_incorrect_position = 1
        elif self.image_incorrect_selected or self.image_correct_selected != 2:
            self.image_incorrect_position = 2




        self.lat = 0
        self.init_lat = 0

        self.current_correct = 0
        self.current_correction = 0

        self.delay_hold_button = ImageButton(source='%s\\Images\\white.png' % (self.curr_dir), allow_stretch=True)
        self.delay_hold_button.size_hint = (.16,.16)
        self.delay_hold_button.pos = ((self.center_x - (0.08 * self.monitor_x_dim)),(self.center_y - (0.08 * self.monitor_y_dim) - (0.4 * self.monitor_y_dim)))

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

            self.correct_image_wid = ImageButton(source='%s\\Images\\%s.png' % (self.curr_dir,self.image_list[self.image_correct_selected]), allow_stretch=True)
            self.correct_image_wid.size_hint = (.3, .3)
            self.correct_image_wid.pos = (
            (self.center_x - (0.15 * self.monitor_x_dim) + (0.1 * self.image_correct_pos[self.image_correct_selected] * self.monitor_x_dim)), (self.center_y - (0.15 * self.monitor_y_dim)))
            self.correct_image_wid.bind(on_press= self.response_correct)
            self.add_widget(self.correct_image_wid)

            self.incorrect_image_wid = ImageButton(source='%s\\Images\\%s.png' % (self.curr_dir,self.image_list[self.image_incorrect_selected]), allow_stretch=True)
            self.incorrect_image_wid.size_hint = (.3, .3)
            self.incorrect_image_wid.pos = (
            (self.center_x - (0.15 * self.monitor_x_dim) + (0.1 * self.image_incorrect_position * self.monitor_x_dim)), (self.center_y - (0.15 * self.monitor_y_dim)))
            self.incorrect_image_wid.bind(on_press= self.response_incorrect)
            self.add_widget(self.incorrect_image_wid)


            self.image_pres_time = time.time()
            self.image_on_screen = True

    def response_correct(self, *args):
        self.image_touch_time = time.time()
        self.remove_widget(self.correct_image_wid)
        self.remove_widget(self.incorrect_image_wid)

        self.lat = self.image_touch_time - self.image_pres_time

        self.current_correct = 1
        self.correction_active = False
        self.feedback_string = 'CORRECT'

        self.record_data()
        self.set_new_trial_configuration()

    def response_incorrect(self, *args):
        self.image_touch_time = time.time()
        self.remove_widget(self.correct_image_wid)
        self.remove_widget(self.incorrect_image_wid)

        self.lat = self.image_touch_time - self.image_pres_time

        self.correction_active = True
        self.feedback_string = 'INCORRECT - PLEASE TRY AGAIN'

        self.current_correct = 0
        self.record_data()
        self.start_iti()

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
        self.data_file.write("%s,%s,%s,%s,%s" % (self.current_trial,self.image_list[self.image_correct_selected],self.current_correction,self.current_correct,self.lat))
        self.data_file.close()

        if self.current_correct == 0:
            self.current_correction = 1
        if self.current_correct == 1:
            self.current_correction = 0

    def set_new_trial_configuration(self):

        self.current_correction = 0
        self.current_trial += 1

        self.image_correct_selected = random.randint(0,2)

        self.image_incorrect_selected = random.randint(0,2)

        while self.image_correct_selected == self.image_incorrect_selected:
            self.image_incorrect_selected = random.randint(0,2)

        if self.image_incorrect_selected or self.image_correct_selected != 0:
            self.image_incorrect_position = 0
        elif self.image_incorrect_selected or self.image_correct_selected != 1:
            self.image_incorrect_position = 1
        elif self.image_incorrect_selected or self.image_correct_selected != 2:
            self.image_incorrect_position = 2


        self.start_iti()



    def feedback_report(self,*args):
        self.feedback_displayed = True
        self.iti_clock_trigger = False
        self.feedback_wid = Label(text=self.feedback_string, font_size='50sp')
        self.feedback_wid.size_hint = (.5,.3)
        self.feedback_wid.pos = ((self.center_x - (0.25 * self.monitor_x_dim)),(self.center_y - (0.15*self.monitor_y_dim)))
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
        experiment = Experiment_Staging()
        return experiment

if __name__ == '__main__':
    monitor_x_dim = GetSystemMetrics(0)
    monitor_y_dim = GetSystemMetrics(1)
    Window.size = (monitor_x_dim,monitor_y_dim)
    Window.fullscreen = True
    Experiment_App().run()