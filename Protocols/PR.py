import random
import os
import time
import sys
from kivy.config import Config
curr_dir = os.getcwd()
if sys.platform == 'linux':
    config_path = curr_dir + '/Configuration.ttconfig'
elif sys.platform == 'win32':
    config_path = curr_dir + '\\Configuration.ttconfig'
    
config_file = open(config_path,'r')
configurations = config_file.readlines()
monitor_x_dim = configurations[0]
monitor_x_dim = monitor_x_dim.replace('x_dim = ','')
monitor_x_dim = monitor_x_dim.replace('\n','')
monitor_x_dim = int(monitor_x_dim)
monitor_y_dim = configurations[1]
monitor_y_dim = monitor_y_dim.replace('y_dim = ','')
monitor_y_dim = monitor_y_dim.replace('\n','')
monitor_y_dim = int(monitor_y_dim)
fullscreen = configurations[2]
fullscreen = fullscreen.replace('fullscreen = ','')
fullscreen = fullscreen.replace('\n','')
fullscreen = str(fullscreen)
config_file.close()

Config.set('kivy', 'keyboard_mode', 'systemandmulti')
Config.set('graphics', 'fullscreen', fullscreen)
Config.set('graphics', 'width', monitor_x_dim)
Config.set('graphics', 'height', monitor_y_dim)
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
#from win32api import GetSystemMetrics
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.uix.vkeyboard import VKeyboard
from functools import partial

class ImageButton(ButtonBehavior,Image):
    def __init__(self,**kwargs):
        super(ImageButton,self).__init__(**kwargs)

class Experiment_Staging(FloatLayout):
    def __init__(self,trial_max,session_max,block_length,block_count,id_entry,**kwargs):
        super(Experiment_Staging,self).__init__(**kwargs)
        self.curr_dir = os.getcwd()
        if sys.platform == 'linux':
            self.config_path = self.curr_dir + '/Configuration.ttconfig'
        elif sys.platform == 'win32':
            self.config_path = self.curr_dir + '\\Configuration.ttconfig'
            
        self.config_file = open(self.config_path,'r')
        self.configurations = self.config_file.readlines()
        self.monitor_x_dim = self.configurations[0]
        self.monitor_x_dim = self.monitor_x_dim.replace('x_dim = ','')
        self.monitor_x_dim = self.monitor_x_dim.replace('\n','')
        self.monitor_x_dim = int(self.monitor_x_dim)
        self.monitor_y_dim = self.configurations[1]
        self.monitor_y_dim = self.monitor_y_dim.replace('y_dim = ','')
        self.monitor_y_dim = self.monitor_y_dim.replace('\n','')
        self.monitor_y_dim = int(self.monitor_y_dim)
        self.config_file.close()
        Config.set('graphics', 'width', '0')
        Config.set('graphics', 'height', '0')
        self.size = (self.monitor_x_dim,self.monitor_y_dim)
        
        if sys.platform == 'linux':
            self.data_add = '/Data'
            self.delay_hold_path = '%s/Images/white.png' % (self.curr_dir)
            self.yellow_path = '%s/Images/yellow.png' % (self.curr_dir)
            self.red_path = '%s/Images/red.png' % (self.curr_dir)
            self.folder_symbol = '/'
        elif sys.platform == 'win32':
            self.data_add = '\\Data'
            self.delay_hold_path = '%s\\Images\\white.png' % (self.curr_dir)
            self.yellow_path = '%s\\Images\\yellow.png' % (self.curr_dir)
            self.red_path = '%s\\Images\\red.png' % (self.curr_dir)
            self.folder_symbol = '\\'


        self.trial_displayed = False
        self.data_dir = self.curr_dir + self.data_add
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)


        self.delay_length = 4

        self.current_stage = 3
        self.stage_criteria = 48
        self.current_total_correct = 0

        self.max_trials = trial_max
        self.max_time = session_max
        self.id_no = id_entry
        
        self.block_length = block_length
        self.block_threshold = self.block_length
        self.block_count = block_count
        self.threshold_increment = self.block_length
        self.current_block = 1

        self.current_ratio = 4
        self.pr_threshold = 1
        self.current_response = 0
        self.current_points = 0

        self.current_trial = 1
        self.time_elapsed = 0
        self.start_time = time.time()

        self.iti_time = 0.5

        self.feedback_string = 'Reward: 0 Points'


        self.sample_x_shift = random.randint(-3,4)
        self.sample_y_shift = random.randint(-3,4)

        self.sample_coord = (self.sample_x_shift, self.sample_y_shift)

        self.lat = 0
        self.init_lat = 0

        self.current_correct = 0
        self.current_correction = 0

        Clock.schedule_interval(self.clock_update, 0.001)
        self.id_setup()


    def id_setup(self):
        self.participant_data_folder = self.data_dir + self.folder_symbol + self.id_no + self.folder_symbol
        if os.path.exists(self.participant_data_folder) == False:
            os.makedirs(self.participant_data_folder)
        self.participant_data_path = self.participant_data_folder + 'PR %s.csv' % (self.id_no)
        self.data_col_names = 'TrialNo, Current Block, Trial Type, Correction Trial, Correct, Response Latency'
        self.data_file = open(self.participant_data_path, "w+")
        self.data_file.write(self.data_col_names)
        self.data_file.close()

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
        self.present_background()

    def present_background(self,*args):
        #self.x_mod_list = [-4,-3,-2,-1,1,2,3,4]
        #self.y_mod_list = [-4,-3,-2,-1,1,2,3,4]
        self.x_mod_list = [-3,-2,-1,0,1,2,3,4]
        self.y_mod_list = [-3,-2,-1,0,1,2,3,4]
        self.background_image_list = [Image() for i in range(64)]
        for image in self.background_image_list:
            image.size_hint = (.08,.08)
            if sys.platform == 'linux':
                self.image_path = '%s/Images/grey.png' % (self.curr_dir)
            elif sys.platform == 'win32':
                self.image_path = '%s\\Images\\grey.png' % (self.curr_dir)
            image.source = self.image_path
            image.allow_stretch = True

            self.real_pos = 0
            self.x_pos = 0
            self.y_pos = 0
            self.x_mod = 0
            self.y_mod = 0
        for pos_value in range(64):
            self.x_mod = self.x_mod_list[self.x_pos]
            self.y_mod = self.y_mod_list[self.y_pos]
            self.background_image_list[pos_value].pos = ((self.center_x - (0.05*self.monitor_x_dim) + ((self.x_mod * 0.1) * self.monitor_y_dim)), (self.center_y - (0.05*self.monitor_y_dim) + ((self.y_mod * 0.1) * self.monitor_y_dim)))
            self.real_pos = pos_value + 1
            if self.real_pos % 8 == 0:
                self.y_pos += 1
                self.x_pos = 0
            else:
                self.x_pos += 1
        for image in self.background_image_list:
            self.add_widget(image)

        self.feedback_wid = Label(text=self.feedback_string, font_size='50sp')
        self.feedback_wid.size_hint = (.5,.3)
        self.feedback_wid.pos = ((self.center_x - (0.25 * self.monitor_x_dim)),(self.center_y - (0.15*self.monitor_y_dim) + (0.46*self.monitor_y_dim)))
        self.add_widget(self.feedback_wid)

        self.trial_initiation()


    def trial_initiation(self):
        self.initiation_image_wid = ImageButton(source=self.delay_hold_path, allow_stretch=True)
        self.initiation_image_wid.size_hint = (.2,.1)
        self.initiation_image_wid.pos = ((self.center_x - (0.1 * self.monitor_x_dim)),(self.center_y - (0.05 * self.monitor_y_dim) - (0.45 * self.monitor_y_dim)))
        self.initiation_image_wid.bind(on_press= self.initiation_detected)
        self.add_widget(self.initiation_image_wid)
        self.initiation_start_time = time.time()

    def initiation_detected(self,*args):
        self.remove_widget(self.initiation_image_wid)
        self.initiation_end_time = time.time()
        self.init_lat = self.initiation_end_time - self.initiation_start_time
        self.sample_presentation()

    def sample_presentation(self):
        self.sample_image_wid = ImageButton(source=self.delay_hold_path, allow_stretch=True)
        self.sample_image_wid.size_hint = (.08,.08)
        self.sample_image_wid.pos = ((self.center_x - (0.05*self.monitor_x_dim) + ((self.sample_x_shift * 0.1) * self.monitor_y_dim)), (self.center_y - (0.05*self.monitor_y_dim) + ((self.sample_y_shift * 0.1) * self.monitor_y_dim)))
        self.sample_image_wid.bind(on_press = self.sample_pressed)

        self.add_widget(self.sample_image_wid)

        self.image_pres_time = time.time()

    def sample_pressed(self,*args):
        self.remove_widget(self.sample_image_wid)
        self.current_response += 1
        #self.record_data()
        self.set_new_trial_configuration()


    def response_correct(self,*args):
        self.image_touch_time = time.time()

        self.lat = self.image_touch_time - self.image_pres_time

        self.pr_threshold += self.current_ratio
        self.current_response = 0
        self.current_points += 1
        self.feedback_string = 'Reward: %s Points' % (str(self.current_points))
        self.feedback_wid.text = self.feedback_string



    def record_data(self):
        self.data_file = open(self.participant_data_path, "a")
        self.data_file.write("\n")
        self.data_file.write("%s,%s,[%s][%s]/[%s][%s],%s,%s,%s,%s" % (self.current_trial,self.current_block,self.sample_x_shift,self.sample_y_shift,self.choice_x_shift,self.choice_y_shift,self.current_correction,self.current_correct,self.lat,self.init_lat))
        self.data_file.close()

        if self.current_correct == 0:
            self.current_correction = 1
        if self.current_correct == 1:
            self.current_correction = 0

    def set_new_trial_configuration(self):
        
        if self.current_response >= self.pr_threshold:
            self.response_correct()


        self.sample_x_shift = random.randint(-3,4)
        self.sample_y_shift = random.randint(-3,4)




        self.sample_coord = (self.sample_x_shift, self.sample_y_shift)
        self.current_trial += 1

        self.initiation_image_wid.unbind(on_press= self.initiation_detected)
        self.initiation_image_wid.bind(on_press = self.start_iti)
        self.add_widget(self.initiation_image_wid)

        
    def block_hold(self,*args):
        self.delay_hold_button.unbind(on_release=self.premature_response)
        self.remove_widget(self.delay_hold_button)
        if self.current_block == self.block_count:
            self.end_experiment_screen()
        self.current_block += 1
        self.current_trial -= 1
        self.block_threshold += self.threshold_increment


        self.block_instruction_wid = Label(text='PRESS BUTTON TO CONTINUE WHEN READY',font_size='50sp')
        self.block_instruction_wid.size_hint = (.5,.3)
        self.block_instruction_wid.pos = ((self.center_x - (0.25 * self.monitor_x_dim)),(self.center_y - (0.15*self.monitor_y_dim) + (0.3*self.monitor_y_dim)))

        self.block_button = Button(text='Continue')
        self.block_button.size_hint = (.2,.1)
        self.block_button.pos = ((self.center_x - (0.1 * self.monitor_x_dim)),(self.center_y - (0.05*self.monitor_y_dim) + (-0.4*self.monitor_y_dim)))
        self.block_button.bind(on_press = self.block_press)

        self.add_widget(self.block_instruction_wid)
        
        self.block_button_active = False
        self.block_continue_stage()

    def block_continue_stage(self, *args):
        if self.block_button_active == False:
            Clock.schedule_interval(self.block_continue_stage, 0.01)
            self.start_block_hold = time.time()
            self.block_button_active = True
        if (self.block_button_active == True) and ((self.current_time - self.start_block_hold) >= self.block_hold_time):
            Clock.unschedule(self.block_continue_stage)
            self.block_button_active = False
            self.block_button = Button(text='Continue')
            self.block_button.size_hint = (.2, .1)
            self.block_button.pos = ((self.center_x - (0.1 * self.monitor_x_dim)),
                                     (self.center_y - (0.05 * self.monitor_y_dim) + (-0.4 * self.monitor_y_dim)))
            self.block_button.bind(on_press=self.block_press)
            self.add_widget(self.block_button)

    def block_press(self,*args):
        self.remove_widget(self.block_instruction_wid)
        self.remove_widget(self.block_button)
        self.set_new_trial_configuration()
        self.add_widget(self.delay_hold_button)

    def start_iti(self,*args):
        self.start_iti_time = time.time()
        self.iti_clock_trigger = False
        self.end_iti()

    def end_iti(self,*args):
        if self.iti_clock_trigger == False:
            Clock.schedule_interval(self.end_iti, 0.01)
            self.iti_clock_trigger = True
        if (self.current_time - self.start_iti_time) >= self.iti_time:
            Clock.unschedule(self.end_iti)
            self.remove_widget(self.initiation_image_wid)
            if self.time_elapsed >= self.max_time:
                self.end_experiment_screen()
                return
            if self.current_trial >= self.max_trials:
                self.end_experiment_screen()
                return
            self.sample_presentation()

    def clock_update(self,*args):
        self.current_time = time.time()
        self.time_elapsed = time.time() - self.start_time

    def end_experiment_screen(self):
        self.delay_hold_button.unbind(on_release=self.premature_response)
        self.remove_widget(self.delay_hold_button)

        self.end_feedback = Label(text='Thank you for your participation. Please press EXIT to end experiment.',font_size='50sp')
        self.end_feedback.size_hint = (.7,.4)
        self.end_feedback.pos = ((self.center_x - (0.35 * self.monitor_x_dim)),(self.center_y - (0.2*self.monitor_y_dim)))

        self.end_button = Button(text='EXIT')
        self.end_button.size_hint = (.2,.1)
        self.end_button.pos = ((self.center_x - (0.1 * self.monitor_x_dim)),(self.center_y - (0.05*self.monitor_y_dim) + (-0.4*self.monitor_y_dim)))
        self.end_button.bind(on_press = self.end_experiment)

        self.add_widget(self.end_feedback)
        self.add_widget(self.end_button)


    def end_experiment(self,*args):
        App.get_running_app().stop()

class Experiment_App(App):
    def build(self):
        experiment = Experiment_Staging(trial_max = self.trial_max,session_max = self.session_max,block_length=self.block_length,block_count=self.block_count,id_entry=self.id_entry)
        return experiment
    def set(self,trial_max,session_max,block_length,block_count,id_entry):
        self.trial_max = trial_max
        self.session_max = session_max
        self.block_length = block_length
        self.block_count = block_count
        self.id_entry = id_entry

if __name__ == '__main__':
    #monitor_x_dim = GetSystemMetrics(0)
    #monitor_y_dim = GetSystemMetrics(1)
    #Window.size = (monitor_x_dim,monitor_y_dim)
    #Window.fullscreen = True
    Experiment_App().run()
