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

        self.max_trials = 72
        self.max_time = 3600

        self.current_trial = 1
        self.time_elapsed = 0
        self.start_time = time.time()

        self.iti_time = 5

        self.sample_x_shift = 1
        self.sample_y_shift = 1

        self.sample_x_shift = random.randint(-3,3)
        while self.sample_x_shift == 0:
            self.sample_x_shift = random.randint(-3, 3)
        self.sample_y_shift = random.randint(-2,2)
        while self.sample_y_shift == 0:
            self.sample_y_shift = random.randint(-2, 2)
        self.choice_x_shift = 1
        self.choice_y_shift = 1

        self.choice_x_shift = random.randint(1,6)
        while self.choice_x_shift == 0:
            self.choice_x_shift = random.randint(-3, 3)
        self.choice_y_shift = random.randint(1,4)
        while self.choice_y_shift == 0:
            self.choice_y_shift = random.randint(-3, 3)

        self.lat = 0
        self.init_lat = 0

        self.current_correct = 0
        self.current_correction = 0

        Clock.schedule_interval(self.clock_update, 0.001)
        self.stage_manager()



    def stage_shift(self,new_stage):
        self.current_stage = new_stage
        self.stage_executed = False
        if self.stage_executed == False:
            self.stage_executed = True
            self.stage_manager()


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
        self.id_button.bind(on_press = lambda new_stage: self.stage_shift(new_stage=2))

        self.add_widget(self.id_instruction)
        self.add_widget(self.id_entry)
        self.add_widget(self.id_button)

    def clear_id(self):
        self.id_no = self.id_entry.text
        self.id_entry.hide_keyboard()

        self.participant_data_path = self.data_dir + '\\%s.csv' % (self.id_no)
        self.data_col_names = 'TrialNo, Trial Type, Correction Trial, Correct, Response Latency, Initiation Latency'
        self.data_file = open(self.participant_data_path, "w+")
        self.data_file.write(self.data_col_names)
        self.data_file.close()

        self.remove_widget(self.id_instruction)
        self.remove_widget(self.id_entry)
        self.remove_widget(self.id_button)
        self.stage_shift(new_stage=3)

    def instruction_presentation(self):
        self.instruction_label = Label(text= 'To initiate trials, press the white button.\nTo make a response, press on one of the images on the screen.\nYou will receive feedback following a response.'
                                       , font_size = '40sp')
        self.instruction_label.size_hint = (.5,.2)
        self.instruction_label.pos = ((self.center_x - (0.25 * self.monitor_x_dim)),(self.center_y - (0.1*self.monitor_y_dim) + (0.2*self.monitor_y_dim)))

        self.initiate_button = Button(text='Press to Start')
        self.initiate_button.size_hint = (.1,.1)
        self.initiate_button.pos = ((self.center_x - (0.05 * self.monitor_x_dim)),(self.center_y - (0.05*self.monitor_y_dim) - (0.2*self.monitor_y_dim)))
        self.initiate_button.bind(on_press = lambda new_stage: self.stage_shift(new_stage=4))
        self.add_widget(self.instruction_label)
        self.add_widget(self.initiate_button)

    def clear_instruction(self):
        self.remove_widget(self.instruction_label)
        self.remove_widget(self.initiate_button)
        self.start_time = time.time()
        self.stage_shift(new_stage=5)

    def trial_initiation(self):
        self.initiation_image_wid = ImageButton(source='%s\\Images\\white.png' % (self.curr_dir), allow_stretch=True)
        self.initiation_image_wid.size_hint = (.16,.16)
        self.initiation_image_wid.pos = ((self.center_x - (0.08 * self.monitor_x_dim)),(self.center_y - (0.08 * self.monitor_y_dim) - (0.4 * self.monitor_y_dim)))
        self.initiation_image_wid.bind(on_press= lambda new_stage: self.stage_shift(new_stage=6))
        self.add_widget(self.initiation_image_wid)
        self.initiation_start_time = time.time()

    def initiation_detected(self):
        self.remove_widget(self.initiation_image_wid)
        self.initiation_end_time = time.time()
        self.init_lat = self.initiation_end_time - self.initiation_start_time
        self.stage_shift(new_stage=7)

    def sample_presentation(self):
        self.sample_image_wid = ImageButton(source='%s\\Images\\white.png' % (self.curr_dir), allow_stretch=True)
        self.sample_image_wid.size_hint = (.1,.1)
        self.sample_image_wid.pos = ((self.center_x - (0.05 * self.monitor_x_dim) + (self.sample_x_shift * 0.05 * self.monitor_x_dim)), (self.center_y - (0.05*self.monitor_y_dim) + (self.sample_y_shift * 0.05 * self.monitor_x_dim)))
        self.sample_image_wid.bind(on_press = lambda new_stage: self.stage_shift(new_stage=9))

        self.add_widget(self.sample_image_wid)

        self.image_pres_time = time.time()

    def response_correct(self):
        self.image_touch_time = time.time()
        self.remove_widget(self.sample_image_wid)

        self.lat = self.image_touch_time - self.image_pres_time


        self.current_correct = 1
        self.correction_active = False
        self.feedback_string = 'CORRECT'

        #self.record_data()
        self.stage_shift(new_stage=10)



    def response_incorrect(self):
        self.image_touch_time = time.time()
        self.remove_widget(self.correct_image_wid)
        self.remove_widget(self.incorrect_image_wid)

        self.lat = self.image_touch_time - self.image_pres_time

        self.correction_active = True
        self.feedback_string = 'INCORRECT - PLEASE TRY AGAIN'


        self.current_correct = 0
        self.record_data()
        self.stage_shift(new_stage=11)

    def record_data(self):
        self.data_file = open(self.participant_data_path, "a")
        self.data_file.write("\n")
        self.data_file.write("%s,%s,%s,%s,%s,%s" % (self.current_trial,self.trial_type[self.curr_trial_type],self.current_correction,self.current_correct,self.lat,self.init_lat))
        self.data_file.close()

        if self.current_correct == 0:
            self.current_correction = 1
        if self.current_correct == 1:
            self.current_correction = 0

    def set_new_trial_configuration(self):

        self.current_correction = 0

        self.sample_x_shift = random.randint(-3,3)
        while self.sample_x_shift == 0:
            self.sample_x_shift = random.randint(-3, 3)
        self.sample_y_shift = random.randint(-2,2)
        while self.sample_y_shift == 0:
            self.sample_y_shift = random.randint(-2, 2)
        self.choice_x_shift = 1
        self.choice_y_shift = 1

        self.choice_x_shift = random.randint(1,6)
        while self.choice_x_shift == 0:
            self.choice_x_shift = random.randint(-3, 3)
        self.choice_y_shift = random.randint(1,4)
        while self.choice_y_shift == 0:
            self.choice_y_shift = random.randint(-3, 3)

        self.current_trial += 1
        self.stage_shift(new_stage=11)

    def start_iti(self):
        self.start_iti_time = time.time()
        self.feedback_wid = Label(text=self.feedback_string, font_size='50sp')
        self.feedback_wid.size_hint = (.5,.3)
        self.feedback_wid.pos = ((self.center_x - (0.25 * self.monitor_x_dim)),(self.center_y - (0.15*self.monitor_y_dim)))
        self.add_widget(self.feedback_wid)
        self.iti_clock_trigger = False
        self.stage_shift(new_stage=12)

    def end_iti(self,*args):
        if self.iti_clock_trigger == False:
            Clock.schedule_interval(self.end_iti, 0.01)
            self.iti_clock_trigger = True
        if (self.current_time - self.start_iti_time) >= self.iti_time:
            Clock.unschedule(self.end_iti)
            self.remove_widget(self.feedback_wid)
            self.stage_shift(new_stage=5)


    def stage_manager(self,*args):
        if (self.current_trial > self.max_trials) or (self.time_elapsed > self.max_time):
            App.get_running_app().stop()

        if self.current_stage == 1:
            self.id_entry()
        elif self.current_stage == 2:
            self.clear_id()
        elif self.current_stage == 3:
            self.instruction_presentation()
        elif self.current_stage == 4:
            self.clear_instruction()
        elif self.current_stage == 5:
            self.trial_initiation()
        elif self.current_stage == 6:
            self.initiation_detected()
        elif self.current_stage == 7:
            self.sample_presentation()
        elif self.current_stage == 8:
            self.response_incorrect()
        elif self.current_stage == 9:
            self.response_correct()
        elif self.current_stage == 10:
            self.set_new_trial_configuration()
        elif self.current_stage == 11:
            self.start_iti()
        elif self.current_stage == 12:
            self.end_iti()

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