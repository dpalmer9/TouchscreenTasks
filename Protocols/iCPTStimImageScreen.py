import random
import os
import time
import sys
from kivy.config import Config
curr_dir = os.getcwd()
if sys.platform == 'linux' or sys.platform == 'darwin':
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
    def __init__(self,trial_max,session_max,id_entry,**kwargs):
        super(Experiment_Staging,self).__init__(**kwargs)
        
        self.curr_dir = os.getcwd()
        if sys.platform == 'linux' or sys.platform == 'darwin':
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
        
        if sys.platform == 'linux' or sys.platform == 'darwin':
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
        self.hold_removed = False
        self.not_pressed = True


        self.delay_length = 4

        self.max_trials = trial_max
        self.max_time = session_max
        self.id_no = id_entry

        self.current_trial = 1
        self.current_total_hits = 0
        self.current_total_miss = 0
        self.hit_threshold = 20
        self.threshold_increment = self.hit_threshold
        self.current_stage = 0 # 1=main, 1=sd probe, 2=iti, 3=contrast,4=flanker
        self.time_elapsed = 0
        self.start_time = time.time()
        self.start_iti_time = 0

        self.current_block = 1
        self.probe_pos = 0
        self.start_pos = 0

        self.iti_time = 0.5
        self.presentation_delay_time = 1
        self.feedback_length = 0.5
        self.stimulus_duration = 1
        self.block_hold_time = 5

        self.image_list = []
        self.image_prob = 0.33
        self.target_item = '4'
        self.distractor_list = ['1','2','3','5','9','10','11','13','14','15','16','20','30']
        self.distractor_count = round(((1 - self.image_prob) / len(self.distractor_list)) * 100,0)

        self.image_count = int(self.image_prob * 100)

        for image in range(0,self.image_count):
            self.image_list.append(self.target_item)

        for distractor in self.distractor_list:
            for repeat in range(0,int(self.distractor_count)):
                self.image_list.append(distractor)

        self.image_list_pos = random.randint(0,(len(self.image_list) - 1))
        self.current_image = 'snowflake'

        
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

        self.delay_hold_button = ImageButton(source=self.delay_hold_path, allow_stretch=True)
        self.delay_hold_button.size_hint = (.24,.24)
        self.delay_hold_button.pos = ((self.center_x - (0.12 * self.monitor_x_dim)),(self.center_y - (0.12 * self.monitor_y_dim) - (0.4 * self.monitor_y_dim)))

        Clock.schedule_interval(self.clock_update, 0.001)
        self.id_setup()


    def id_setup(self):
        self.participant_data_folder = self.data_dir + self.folder_symbol + self.id_no + self.folder_symbol
        if os.path.exists(self.participant_data_folder) == False:
            os.makedirs(self.participant_data_folder)
        self.participant_data_path = self.participant_data_folder + 'iCPTStimImageScreen %s.csv' % (self.id_no)
        self.data_col_names = 'TrialNo, Stage, Block #, Trial Type, Correction Trial, Correct, Response Latency'
        self.data_file = open(self.participant_data_path, "w+")
        self.data_file.write(self.data_col_names)
        self.data_file.close()

        self.instruction_presentation()

    def instruction_presentation(self):
        self.instruction_label = Label(text= 'During the experiment, hold your finger on the white square before responding .\nTo make a response, press on one of the images on the centre of the screen.\nYou will receive feedback following touching an image.'
                                       , font_size = '35sp',text_size = ((0.8*self.monitor_x_dim),(0.4*self.monitor_y_dim)))
        self.instruction_label.size_hint = (0.6,0.4)
        self.instruction_label.pos = ((self.center_x - (0.3 * self.monitor_x_dim)),(self.center_y - (0.2*self.monitor_y_dim) + (0.2*self.monitor_y_dim)))

        self.initiate_button = Button(text='Press to Begin')
        self.initiate_button.size_hint = (.1,.1)
        self.initiate_button.pos = ((self.center_x - (0.05 * self.monitor_x_dim)),(self.center_y - (0.05*self.monitor_y_dim) - (0.2*self.monitor_y_dim)))
        self.initiate_button.bind(on_press = self.clear_instruction)
        self.add_widget(self.instruction_label)
        self.add_widget(self.initiate_button)
        print(self.size_hint)

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
            self.presentation_delay_start = False
            self.image_presentation()

    def image_presentation(self,*args):
        if self.image_on_screen == False:
            self.delay_hold_button.unbind(on_release=self.premature_response)
            self.delay_hold_button.bind(on_release=self.hold_removed_presentation)
            self.delay_hold_button.bind(on_press=self.hold_returned_presentation)
            if self.current_stage == 4:
                if sys.platform == 'linux'or sys.platform == 'darwin':
                    self.image_path = '%s/Images/%s.png' % (self.curr_dir, self.image_name_contrast)
                elif sys.platform == 'win32':
                    self.image_path = '%s\\Images\\%s.png' % (self.curr_dir, self.image_name_contrast)
                self.image_wid = ImageButton(
                    source=self.image_path,allow_stretch=True)
                
            elif self.current_stage == 0:
                if sys.platform == 'linux'or sys.platform == 'darwin':
                    self.image_path = '%s/Images/snowflake.png' % (self.curr_dir)
                elif sys.platform == 'win32':
                    self.image_path = '%s\\Images\\snowflake.png' % (self.curr_dir)
                self.image_wid = ImageButton(source=self.image_path,allow_stretch=True)
                self.current_image = 'snowflake'
            else:
                if sys.platform == 'linux'or sys.platform == 'darwin':
                    self.image_path = '%s/Images/%s.png' % (self.curr_dir, self.image_list[self.image_list_pos])
                elif sys.platform == 'win32':
                    self.image_path = '%s\\Images\\%s.png' % (self.curr_dir, self.image_list[self.image_list_pos])
                self.image_wid = ImageButton(source=self.image_path, allow_stretch=True)
                
            self.image_wid.size_hint = (.4, .4)
            self.image_wid.pos = (
            (self.center_x - (0.2 * self.monitor_x_dim)), (self.center_y - (0.2 * self.monitor_y_dim)))
            self.image_wid.bind(on_press= self.image_pressed)
            if self.current_stage == 5 and self.distractor_active == 1:
                if sys.platform == 'linux'or sys.platform == 'darwin':
                    self.image_path_d1 = '%s/Images/%s.png' % (self.curr_dir, self.image_list[self.distractor_image_pos])
                elif sys.platform == 'win32':
                    self.image_path_d1 = '%s\\Images\\%s.png' % (self.curr_dir, self.image_list[self.distractor_image_pos])
                self.distractor_one_wid = ImageButton(source=self.image_path_d1, allow_stretch=True)
                self.distractor_one_wid.size_hint = (.4, .4)
                self.distractor_one_wid.pos = (
                    (self.center_x - (0.2 * self.monitor_x_dim) - (0.33 * self.monitor_x_dim)), (self.center_y - (0.2 * self.monitor_y_dim)))

                if sys.platform == 'linux'or sys.platform == 'darwin':
                    self.image_path_d2 = '%s/Images/%s.png' % (self.curr_dir, self.image_list[self.distractor_image_pos])
                elif sys.platform == 'win32':
                    self.image_path_d2 = '%s\\Images\\%s.png' % (self.curr_dir, self.image_list[self.distractor_image_pos])
                self.distractor_two_wid = ImageButton(
                    source=self.image_path_d2,allow_stretch=True)
                self.distractor_two_wid.size_hint = (.4, .4)
                self.distractor_two_wid.pos = (
                    (self.center_x - (0.2 * self.monitor_x_dim) + (0.33 * self.monitor_x_dim)),
                    (self.center_y - (0.2 * self.monitor_y_dim)))

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
            if self.current_stage == 5 and self.distractor_active == 1:
                self.remove_widget(self.distractor_one_wid)
                self.remove_widget(self.distractor_two_wid)
            if (self.image_list[self.image_list_pos] == 'horizontal') or (self.current_image == 'snowflake') or (self.current_image == self.target_item):
                self.current_total_miss += 1
                self.current_correct = 0
                self.trial_contingency = 4
            else:
                self.current_correct = 1
                self.trial_contingency = 3
            self.lat = ''
            self.not_pressed = True
            self.record_data()
            if self.hold_removed == True:
                self.hold_not_returned()
                return
            self.set_new_trial_configuration()



    def image_pressed(self,*args):
        Clock.unschedule(self.image_presentation)
        self.remove_widget(self.image_wid)
        self.delay_hold_button.unbind(on_release=self.hold_removed_presentation)
        self.delay_hold_button.unbind(on_press=self.hold_returned_presentation)
        self.not_pressed = False
        if self.current_stage == 5 and self.distractor_active == 1:
            self.remove_widget(self.distractor_one_wid)
            self.remove_widget(self.distractor_two_wid)
        if (self.image_list[self.image_list_pos] == 'horizontal') | (self.current_image == 'snowflake') | (self.current_image == self.target_item):
            self.response_correct()
        else:
            self.response_incorrect()


    def response_correct(self):
        self.image_touch_time = time.time()

        self.lat = self.image_touch_time - self.image_pres_time


        self.current_correct = 1
        self.trial_contingency = 1
        self.current_total_hits += 1
        self.current_total_miss = 0
        self.correction_active = False
        self.feedback_string = '[color=008000]CORRECT[/color]'


        self.delay_hold_button.bind(on_press=self.start_iti)
        if (self.current_total_hits < 10 and self.current_stage == 0) or ((self.current_total_hits < (self.hit_threshold) and (self.current_stage != 0))):
            self.feedback_report()
        self.record_data()
        self.set_new_trial_configuration()




    def response_incorrect(self):
        self.image_touch_time = time.time()

        self.lat = self.image_touch_time - self.image_pres_time

        self.correction_active = True
        self.feedback_string = '[color=FF0000]INCORRECT - PLEASE TRY AGAIN[/color]'


        self.current_correct = 0
        self.trial_contingency = 2

        self.delay_hold_button.bind(on_press=self.start_iti)
        if (self.current_total_hits <= 10 and self.current_stage == 0) or ((self.current_total_hits < (self.hit_threshold) and (self.current_stage != 0))):
            self.feedback_report()
        self.record_data()


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
        self.trial_contingency = 5
        self.lat = ''
        self.delay_hold_button.bind(on_press=self.start_iti)
        self.record_data()
        self.feedback_report()

    def hold_not_returned(self,*args):
        self.feedback_string = 'PLEASE RETURN FINGER TO HOLD POSITION'
        self.delay_hold_button.unbind(on_release=self.hold_removed_presentation)
        self.delay_hold_button.unbind(on_press=self.hold_returned_presentation)
        self.delay_hold_button.bind(on_press=self.set_new_trial_configuration)
        self.feedback_report()

    def hold_returned_presentation(self,*args):
        self.hold_removed = False

    def hold_removed_presentation(self,*args):
        self.hold_removed = True

    def record_data(self):
        self.data_file = open(self.participant_data_path, "a")
        self.data_file.write("\n")
        self.data_file.write("%s,%s,%s,%s,%s,%s,%s" % (self.current_trial,self.stage_label,self.current_block,self.current_image,self.current_correction,self.trial_contingency,self.lat))
        self.data_file.close()

        if self.current_correct == 0:
            self.current_correction = 1
        if self.current_correct == 1:
            self.current_correction = 0

    def set_new_trial_configuration(self,*args):

        self.delay_hold_button.unbind(on_press=self.set_new_trial_configuration)

        self.current_correction = 0

        self.image_list_pos = random.randint(0,(len(self.image_list) - 1))
        self.current_image = self.image_list[self.image_list_pos]


        self.current_trial += 1


        if self.current_total_hits >= self.hit_threshold and self.current_stage > 0:
            self.remove_widget(self.delay_hold_button)
            self.block_hold()
            return
        if self.current_total_hits >= 10 and self.current_stage == 0:
            self.remove_widget(self.delay_hold_button)
            self.block_hold()
            return
        if self.current_total_miss >= 20 and self.current_stage > 0:
            self.remove_widget(self.delay_hold_button)
            self.end_experiment_screen()
            return
        if self.current_stage == 4:
            self.contrast_list_pos = random.randint(0, 3)
            self.image_name_contrast = '%s%s' % (self.image_list[self.image_list_pos], self.contrast_list[self.contrast_list_pos])
            self.current_image = self.image_name_contrast
        if self.current_stage == 5:
            self.distractor_active = random.randint(0,1)
            self.distractor_congruent = random.randint(0,1)
            if self.distractor_congruent == 0:
                self.congruent_label = 'Incongruent'
                if self.image_list[self.image_list_pos] == 'horizontal':
                    self.distractor_image_pos = random.randint(4,7)
                else:
                    self.distractor_image_pos = 0
            elif self.distractor_congruent == 1:
                self.congruent_label = 'Congruent'
                self.distractor_image_pos = self.image_list_pos
            if self.distractor_active == 0:
                self.distractor_label = 'No Distractor'
            else:
                self.distractor_label = 'Distractor'
            self.current_image = '%s-%s-%s' % (self.image_list[self.image_list_pos],self.distractor_label,self.congruent_label)
                
        if self.current_stage == 2:
            self.stimulus_duration_pos = random.randint(0,3)
            self.stimulus_duration = self.stimulus_duration_list[self.stimulus_duration_pos]
        if self.current_stage == 3:
            self.iti_duration_pos = random.randint(0,2)
            self.iti_time = self.iti_duration_list[self.iti_duration_pos]
        if self.current_stage == 0:
            self.current_image = 'snowflake'

        if self.not_pressed == True:
            self.start_iti()


    def block_hold(self,*args):
        self.delay_hold_button.unbind(on_release=self.premature_response)
        self.remove_widget(self.delay_hold_button)

        if self.current_stage >= 1:
            self.stimulus_duration -= 0.1

        self.current_block += 1
        self.current_total_miss = 0
        #self.iti_time = 0.5
        self.presentation_delay_time = 1
        #self.feedback_length = 0.5
        self.current_trial -= 1
        self.hit_threshold += self.threshold_increment
        
        if self.current_stage == 0:
            self.current_stage = 1
            self.current_block -= 1
            self.hit_threshold -= self.threshold_increment
            self.hit_threshold += 10
            self.stage_label == 'Main Task'
        if self.current_stage == 1:
            self.stage_label = 'Main Task %s' % (str(self.stimulus_duration))
        if self.current_stage == 2:
            self.stage_label == 'Stimulus Duration Probe'
        if self.current_stage == 3:
            self.stage_label = 'Inter-Trial Interval Probe'
        if self.current_stage == 4:
            self.stage_label = 'Image Contrast Probe'
        if self.current_stage == 5:
            self.stage_label = 'Flanker Probe'


        self.block_instruction_wid = Label(text='PRESS BUTTON TO CONTINUE WHEN READY',font_size='50sp')
        self.block_instruction_wid.size_hint = (.5,.3)
        self.block_instruction_wid.pos = ((self.center_x - (0.25 * self.monitor_x_dim)),(self.center_y - (0.15*self.monitor_y_dim) + (0.3*self.monitor_y_dim)))

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
        self.feedback_wid = Label(text=self.feedback_string, font_size='50sp', markup=True)
        self.feedback_wid.size_hint = (.7,.4)
        self.feedback_wid.pos = ((self.center_x - (0.35 * self.monitor_x_dim)),(self.center_y - (0.2*self.monitor_y_dim)))
        if self.current_total_hits < self.hit_threshold:
            self.add_widget(self.feedback_wid)

    def start_iti(self,*args):
        self.delay_hold_button.unbind(on_release=self.hold_removed_presentation)
        self.delay_hold_button.unbind(on_press=self.hold_returned_presentation)
        self.delay_hold_button.unbind(on_press=self.start_iti)
        self.delay_hold_button.bind(on_release=self.premature_response)
        self.start_feedback_time = time.time()
        self.iti_clock_trigger = False
        self.image_on_screen = False
        self.hold_removed = False
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
            self.image_presentation()



    def clock_update(self,*args):
        self.current_time = time.time()
        self.time_elapsed = time.time() - self.start_time


    def end_experiment_screen(self):
        self.delay_hold_button.unbind(on_release=self.premature_response)
        self.remove_widget(self.delay_hold_button)

        self.end_feedback = Label(text='Thank you for your participation. Please press EXIT to end experiment.',font_size='50sp'
                                  ,text_size = ((0.8*self.monitor_x_dim),(0.4*self.monitor_y_dim)))
        self.end_feedback.size_hint = (.6,.4)
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
        experiment = Experiment_Staging(trial_max=self.trial_maximum,session_max=self.session_maximum,id_entry=self.id_value)
        return experiment
    def set(self,trial_max,session_max,id_entry):
        self.trial_maximum = trial_max
        self.session_maximum = session_max
        self.id_value = id_entry

if __name__ == '__main__':
    #monitor_x_dim = GetSystemMetrics(0)
    #monitor_y_dim = GetSystemMetrics(1)
    #Window.fullscreen = True
    #Window.size = (monitor_x_dim,monitor_y_dim)
    Experiment_App().run()
