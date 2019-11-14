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
    def __init__(self,trial_max,reward_prob,reversal_threshold,session_max,id_entry,max_reversal,**kwargs):
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
            self.folder_symbol = '/'
        elif sys.platform == 'win32':
            self.data_add = '\\Data'
            self.delay_hold_path = '%s\\Images\\white.png' % (self.curr_dir)
            self.folder_symbol = '\\'

        self.trial_displayed = False
        self.data_dir = self.curr_dir + self.data_add
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        self.current_stage = 0
        self.stage_label = 'Train'
        self.next_stage = 1
        self.stage_executed = False

        self.presentation_delay_start = False
        self.image_on_screen = False
        self.feedback_displayed = False

        self.delay_length = 4
        self.block_hold_time = 5

        self.max_trials = trial_max
        self.max_time = session_max
        self.id_no = id_entry
        self.max_reversal = max_reversal
        self.reward_prob_smin = reward_prob * 100
        self.reward_prob_spos = 100 - self.reward_prob_smin


        self.current_trial = 1
        self.current_stage = 0
        self.current_reversal = 0
        self.time_elapsed = 0
        self.start_time = time.time()
        self.start_iti_time = 0

        self.total_correct = 0

        self.iti_time = 0.5
        self.presentation_delay_time = 0.5
        self.feedback_length = 0.5
        self.stimulus_duration = 1

        self.image_list = ['left','right']
        self.train_list = ['snowflake','grey']
        self.image_pos = [-1,1]
        self.image_one_selected = random.randint(0,1)


        self.image_two_selected = random.randint(0,1)

        while self.image_one_selected == self.image_two_selected:
            self.image_two_selected = random.randint(0,1)
            
        self.trial_contingency = self.train_list[self.image_one_selected] + '-' + self.train_list[self.image_two_selected]

        self.image_one_probability = random.randint(1,100)
        self.image_one_reward_threshold = 0
        self.image_two_probability = random.randint(1,100)
        self.image_two_reward_threshold = 0

        self.reversal_threshold = reversal_threshold

        self.start_condition = random.randint(0,1)

        self.image_one_reward_threshold = self.reward_prob_spos
        self.image_two_reward_threshold = self.reward_prob_smin




        self.lat = 0
        self.init_lat = 0

        self.current_correct = 0
        self.current_correction = 0

        self.delay_hold_button = ImageButton(source=self.delay_hold_path, allow_stretch=True)
        self.delay_hold_button.size_hint = (.24,.24)
        self.delay_hold_button.pos = ((self.center_x - (0.12 * self.monitor_x_dim)),(self.center_y - (0.12 * self.monitor_y_dim) - (0.4 * self.monitor_y_dim)))

        self.current_score = 0000
        self.scoreboard_wid = Label(text = 'Your Points:\n       %s' % (self.current_score), font_size='50sp',markup=True)
        self.scoreboard_wid.size_hint = (.4,.4)
        self.scoreboard_wid.pos = ((self.center_x - (0.2 * self.monitor_x_dim)),(self.center_y - (0.2*self.monitor_y_dim) + (0.3*self.monitor_y_dim)))


        Clock.schedule_interval(self.clock_update, 0.001)
        self.id_setup()

    def id_setup(self):
        self.participant_data_folder = self.data_dir + self.folder_symbol + self.id_no + self.folder_symbol
        if os.path.exists(self.participant_data_folder) == False:
            os.makedirs(self.participant_data_folder)
        self.participant_data_path = self.participant_data_folder + 'vPRL %s.csv' % (self.id_no)
        self.data_col_names = 'TrialNo, Current Stage, Reversal #, Trial Type, Correct, Reward Contingency, Response Latency'
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
        self.data_col_names = 'TrialNo,Correct,Rewarded,Response Latency'
        self.data_file = open(self.participant_data_path, "w+")
        self.data_file.write(self.data_col_names)
        self.data_file.close()

        self.remove_widget(self.id_instruction)
        self.remove_widget(self.id_entry)
        self.remove_widget(self.id_button)
        self.instruction_presentation()

    def instruction_presentation(self):
        self.instruction_label = Label(text= '[color=FFFFFF]To start trials, press the white button.[/color]\n[color=FFFFFF]To make a response, press on one of the images on the screen.[/color]\n[color=FFFFFF]You will receive feedback following a response.[/color]'
                                       , font_size = '40sp',markup=True)
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
        self.initiation_image_wid = ImageButton(source=self.delay_hold_path, allow_stretch=True)
        self.initiation_image_wid.size_hint = (.24,.24)
        self.initiation_image_wid.pos = ((self.center_x - (0.12 * self.monitor_x_dim)),(self.center_y - (0.12 * self.monitor_y_dim) - (0.4 * self.monitor_y_dim)))
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
            
            if self.current_stage == 1:
                if sys.platform == 'linux':
                    self.image_path = '%s/Images/%s.png' % (self.curr_dir, self.image_list[0])
                elif sys.platform == 'win32':
                    self.image_path = '%s\\Images\\%s.png' % (self.curr_dir, self.image_list[0])
                self.one_image_wid = ImageButton(source=self.image_path, allow_stretch=True)
            elif self.current_stage == 0:
                if sys.platform == 'linux':
                    self.image_path = '%s/Images/%s.png' % (self.curr_dir, self.train_list[0])
                elif sys.platform == 'win32':
                    self.image_path = '%s\\Images\\%s.png' % (self.curr_dir, self.train_list[0])
                self.one_image_wid = ImageButton(source=self.image_path, allow_stretch=True)
            self.one_image_wid.size_hint = (.4, .4)
            self.one_image_wid.pos = (
            (self.center_x - (0.2 * self.monitor_x_dim) + (0.2 * self.image_pos[self.image_one_selected] * self.monitor_x_dim)), (self.center_y - (0.2 * self.monitor_y_dim)))
            self.one_image_wid.bind(on_press= self.response_one)
            self.add_widget(self.one_image_wid)

            if self.current_stage == 1:
                if sys.platform == 'linux':
                    self.image_path2 = '%s/Images/%s.png' % (self.curr_dir, self.image_list[1])
                elif sys.platform == 'win32':
                    self.image_path2 = '%s\\Images\\%s.png' % (self.curr_dir, self.image_list[1])
                self.two_image_wid = ImageButton(source=self.image_path2, allow_stretch=True)
            elif self.current_stage == 0:
                if sys.platform == 'linux':
                    self.image_path2 = '%s/Images/%s.png' % (self.curr_dir, self.train_list[1])
                elif sys.platform == 'win32':
                    self.image_path2 = '%s\\Images\\%s.png' % (self.curr_dir, self.train_list[1])
                self.two_image_wid = ImageButton(source=self.image_path2, allow_stretch=True)
            self.two_image_wid.size_hint = (.4, .4)
            self.two_image_wid.pos = (
            (self.center_x - (0.2 * self.monitor_x_dim) + (0.2 * self.image_pos[self.image_two_selected] * self.monitor_x_dim)), (self.center_y - (0.2 * self.monitor_y_dim)))
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
            self.total_correct = 0

        if self.image_one_probability > self.image_one_reward_threshold:
            self.feedback_string = '[color=008000]YOU WIN 50 POINTS[/color]'
            self.current_reward = 1
            self.current_score += 50
            self.scoreboard_wid.text = 'Your Points:\n       %s' % (self.current_score)
        else:
            self.feedback_string = '[color=FF0000]NO POINTS[/color]'
            self.current_reward = 0

        self.feedback_report()
        self.record_data()
        self.set_new_trial_configuration()
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
            self.total_correct = 0

        if self.image_two_probability > self.image_two_reward_threshold:
            self.feedback_string = '[color=008000]YOU WIN 50 POINTS[/color]'
            self.current_reward = 1
            self.current_score += 50
            self.scoreboard_wid.text = 'Your Points:\n       %s' % (self.current_score)
        else:
            self.feedback_string = '[color=FF0000]NO POINTS[/color]'
            self.current_reward = 0

        self.feedback_report()
        self.record_data()
        self.set_new_trial_configuration()
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
        self.feedback_report()
        self.record_data()

    def record_data(self):
        self.data_file = open(self.participant_data_path, "a")
        self.data_file.write("\n")
        self.data_file.write("%s,%s,%s,%s,%s,%s,%s" % (self.current_trial,self.stage_label,self.current_reversal,self.trial_contingency,self.current_correct,self.current_reward,self.lat))
        self.data_file.close()

        if self.current_correct == 0:
            self.current_correction = 1
        if self.current_correct == 1:
            self.current_correction = 0

    def set_new_trial_configuration(self):
        
        if (self.current_stage == 0) & (self.current_trial > 10):
            self.block_hold()
            return

        self.current_correction = 0
        self.current_trial += 1

        self.image_one_probability = random.randint(1, 100)
        self.image_two_probability = random.randint(1, 100)

        self.image_one_selected = random.randint(0,1)
        self.image_two_selected = random.randint(0,1)
        

        if (self.total_correct % (self.reversal_threshold) == 0) & (self.total_correct > 0) & (self.current_stage == 1):
            self.current_reversal += 1
            self.total_correct = 0
            self.stage_label = 'Main Task - Reversal ' + str(self.current_reversal)
            if self.image_one_reward_threshold == self.reward_prob_spos:
                self.start_condition = 1
                self.image_one_reward_threshold = self.reward_prob_smin
                self.image_two_reward_threshold = self.reward_prob_spos
            elif self.image_one_reward_threshold == self.reward_prob_smin:
                self.start_condition = 0
                self.image_one_reward_threshold = self.reward_prob_spos
                self.image_two_reward_threshold = self.reward_prob_smin

        while self.image_one_selected == self.image_two_selected:
            self.image_two_selected = random.randint(0,1)
        if self.current_stage == 0:
            self.trial_contingency = self.train_list[self.image_one_selected] + '-' + self.train_list[self.image_two_selected]
        if self.current_stage == 1:
            self.trial_contingency = self.image_list[self.image_one_selected] + '-' + self.image_list[self.image_two_selected]


    def block_hold(self,*args):
        self.delay_hold_button.unbind(on_release=self.premature_response)
        self.remove_widget(self.delay_hold_button)
        self.remove_widget(self.feedback_wid)
        
        self.current_stage = 1
        self.current_trial = 0
        self.current_score = 0
        self.scoreboard_wid.text = 'Your Points:\n       %s' % (self.current_score)
        self.stage_label = 'Main Task - Reversal 0'
            


        self.block_instruction_wid = Label(text='PRESS BUTTON TO CONTINUE WHEN READY',font_size='50sp')
        self.block_instruction_wid.size_hint = (.5,.3)
        self.block_instruction_wid.pos = ((self.center_x - (0.25 * self.monitor_x_dim)),(self.center_y - (0.15*self.monitor_y_dim) + (0.1*self.monitor_y_dim)))

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




    def feedback_report(self,*args):
        self.feedback_displayed = True
        self.iti_clock_trigger = False
        self.feedback_wid = Label(text=self.feedback_string, font_size='60sp',markup=True)
        self.feedback_wid.size_hint = (.6,.4)
        self.feedback_wid.pos = ((self.center_x - (0.3 * self.monitor_x_dim)),(self.center_y - (0.2*self.monitor_y_dim)))
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
            if self.time_elapsed >= self.max_time:
                self.end_experiment_screen()
                return
            if self.current_trial >= self.max_trials:
                self.end_experiment_screen()
                return
            if self.current_reversal >= self.max_reversal:
                self.end_experiment_screen()
                return
            self.image_presentation()

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
        Experiment_App.stop()



    def clock_update(self,*args):
        self.current_time = time.time()
        self.time_elapsed = time.time() - self.start_time

class Experiment_App(App):
    def build(self):
        experiment = Experiment_Staging(trial_max=self.trial_maximum,reward_prob=self.reward_prob, reversal_threshold=self.reversal_threshold,session_max=self.session_maximum,id_entry=self.id_value,max_reversal=self.maximum_reversal)
        return experiment
    def set(self,trial_max,reward_prob,reversal_threshold,session_max,id_entry,max_reversal):
        self.trial_maximum = trial_max
        self.reward_prob = reward_prob
        self.reversal_threshold = reversal_threshold
        self.session_maximum = session_max
        self.id_value = id_entry
        self.maximum_reversal = max_reversal

if __name__ == '__main__':
    #monitor_x_dim = GetSystemMetrics(0)
    #monitor_y_dim = GetSystemMetrics(1)
    #Window.fullscreen = True
    #Window.size = (monitor_x_dim,monitor_y_dim)
    Experiment_App().run()