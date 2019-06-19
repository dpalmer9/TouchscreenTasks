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


        self.delay_length = 4

        self.current_stage = 3
        self.stage_criteria = 48
        self.current_total_correct = 0

        self.max_trials = 72
        self.max_time = 3600

        self.current_trial = 1
        self.time_elapsed = 0
        self.start_time = time.time()

        self.iti_time = 5


        self.sample_x_shift = random.randint(-3,4)
        self.sample_y_shift = random.randint(-3,4)


        self.choice_x_shift = random.randint(-3,4)
        self.choice_y_shift = random.randint(-3,4)

        if (self.choice_x_shift == self.sample_x_shift) and (self.choice_y_shift == self.sample_y_shift):
            while (self.choice_x_shift == self.sample_x_shift) or (self.choice_y_shift == self.sample_y_shift):
                self.choice_x_shift = random.randint(-3, 4)
                self.choice_y_shift = random.randint(-3, 4)

        self.interfere_x_shift = random.randint(-3,4)
        self.interfere_y_shift = random.randint(-3,4)

        while ((self.interfere_x_shift == self.sample_x_shift) and (self.interfere_y_shift == self.sample_y_shift)) or ((self.interfere_x_shift == self.choice_x_shift) and (self.interfere_y_shift == self.choice_y_shift)):
            self.interfere_x_shift = random.randint(-3, 4)
            self.interfere_y_shift = random.randint(-3, 4)

        self.interference_presentation_length = 0.5
        self.interference_start_time = 0
        self.interference_active = False
        
        self.interfere_press = 0

        self.sample_coord = (self.sample_x_shift, self.sample_y_shift)
        self.choice_coord = (self.choice_x_shift, self.choice_y_shift)

        self.interfere_x_shift_1 = random.randint(-3, 4)
        self.interfere_y_shift_1 = random.randint(-3, 4)
        self.interfere_shift_1_coord = (self.interfere_x_shift_1, self.interfere_y_shift_1)

        self.interfere_x_shift_2 = random.randint(-3, 4)
        self.interfere_y_shift_2 = random.randint(-3, 4)
        self.interfere_shift_2_coord = (self.interfere_x_shift_2, self.interfere_y_shift_2)

        self.interfere_x_shift_3 = random.randint(-3, 4)
        self.interfere_y_shift_3 = random.randint(-3, 4)
        self.interfere_shift_3_coord = (self.interfere_x_shift_3, self.interfere_y_shift_3)

        self.distractor_x_shift_1 = random.randint(-3, 4)
        self.distractor_y_shift_1 = random.randint(-3, 4)
        self.distractor_shift_1_coord = (self.distractor_x_shift_1, self.distractor_y_shift_1)

        self.distractor_x_shift_2 = random.randint(-3, 4)
        self.distractor_y_shift_2 = random.randint(-3, 4)
        self.distractor_shift_2_coord = (self.distractor_x_shift_2, self.distractor_y_shift_2)

        self.distractor_x_shift_3 = random.randint(-3, 4)
        self.distractor_y_shift_3 = random.randint(-3, 4)
        self.distractor_shift_3_coord = (self.distractor_x_shift_3, self.distractor_y_shift_3)

        self.coordinate_list = [self.sample_coord, self.choice_coord, self.interfere_shift_1_coord,
                                self.interfere_shift_2_coord,
                                self.interfere_shift_3_coord, self.distractor_shift_1_coord,
                                self.distractor_shift_2_coord,
                                self.distractor_shift_3_coord]

        self.work_list = self.coordinate_list

        for pos in range(2, 7):
            self.check_list = [0, 1, 2, 3, 4, 5, 6, 7]
            self.check_list.remove(pos)
            for check in self.check_list:
                if self.coordinate_list[pos] == self.coordinate_list[check]:
                    if pos == 2:
                        self.interfere_x_shift_1 = random.randint(-3, 4)
                        self.interfere_y_shift_1 = random.randint(-3, 4)
                        self.interfere_shift_1_coord = (self.interfere_x_shift_1, self.interfere_y_shift_1)
                    if pos == 3:
                        self.interfere_x_shift_2 = random.randint(-3, 4)
                        self.interfere_y_shift_2 = random.randint(-3, 4)
                        self.interfere_shift_2_coord = (self.interfere_x_shift_2, self.interfere_y_shift_2)
                    if pos == 4:
                        self.interfere_x_shift_3 = random.randint(-3, 4)
                        self.interfere_y_shift_3 = random.randint(-3, 4)
                        self.interfere_shift_3_coord = (self.interfere_x_shift_3, self.interfere_y_shift_3)
                    if pos == 5:
                        self.distractor_x_shift_1 = random.randint(-3, 4)
                        self.distractor_y_shift_1 = random.randint(-3, 4)
                        self.distractor_shift_1_coord = (self.distractor_x_shift_1, self.distractor_y_shift_1)
                    if pos == 6:
                        self.distractor_x_shift_2 = random.randint(-3, 4)
                        self.distractor_y_shift_2 = random.randint(-3, 4)
                        self.distractor_shift_2_coord = (self.distractor_x_shift_2, self.distractor_y_shift_2)
                    if pos == 7:
                        self.distractor_x_shift_3 = random.randint(-3, 4)
                        self.distractor_y_shift_3 = random.randint(-3, 4)
                        self.distractor_shift_3_coord = (self.distractor_x_shift_3, self.distractor_y_shift_3)

        self.lat = 0
        self.init_lat = 0

        self.current_correct = 0
        self.current_correction = 0

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
        self.data_col_names = 'TrialNo, Trial Type, Correction Trial, Correct, Response Latency, Initiation Latency'
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
        self.present_background()

    def present_background(self,*args):
        #self.x_mod_list = [-4,-3,-2,-1,1,2,3,4]
        #self.y_mod_list = [-4,-3,-2,-1,1,2,3,4]
        self.x_mod_list = [-3,-2,-1,0,1,2,3,4]
        self.y_mod_list = [-3,-2,-1,0,1,2,3,4]
        self.background_image_list = [Image() for i in range(64)]
        for image in self.background_image_list:
            image.size_hint = (.08,.08)
            image.source = '%s\\Images\\grey.png' % (self.curr_dir)
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

        self.trial_initiation()


    def trial_initiation(self):
        self.initiation_image_wid = ImageButton(source='%s\\Images\\white.png' % (self.curr_dir), allow_stretch=True)
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
        self.sample_image_wid = ImageButton(source='%s\\Images\\white.png' % (self.curr_dir), allow_stretch=True)
        self.sample_image_wid.size_hint = (.08,.08)
        self.sample_image_wid.pos = ((self.center_x - (0.05*self.monitor_x_dim) + ((self.sample_x_shift * 0.1) * self.monitor_y_dim)), (self.center_y - (0.05*self.monitor_y_dim) + ((self.sample_y_shift * 0.1) * self.monitor_y_dim)))
        self.sample_image_wid.bind(on_press = self.sample_pressed)

        self.add_widget(self.sample_image_wid)

        self.image_pres_time = time.time()

    def sample_pressed(self,*args):
        self.remove_widget(self.sample_image_wid)
        self.delay_start = time.time()
        self.delay_clock_start = False
        self.interference_active = False
        self.sample_delay_end()

    def sample_delay_end(self,*args):
        if self.delay_clock_start == False:
            Clock.schedule_interval(self.sample_delay_end, 0.01)
            self.delay_clock_start = True
            print('%s %s %s' % (self.delay_clock_start, self.current_stage, self.interference_active))
        if (self.delay_clock_start == True) and (self.current_stage == 2) and (self.interference_active == False) and ((self.current_time - self.delay_start) < (self.iti_time - self.interference_presentation_length)):
            self.intereference_image_wid = ImageButton(source='%s\\Images\\yellow.png' % (self.curr_dir),
                                                    allow_stretch=True)
            self.intereference_image_wid.size_hint = (.08, .08)
            self.intereference_image_wid.pos = (
            (self.center_x - (0.05 * self.monitor_x_dim) + ((self.interfere_x_shift * 0.1) * self.monitor_y_dim)),
            (self.center_y - (0.05 * self.monitor_y_dim) + ((self.interfere_y_shift * 0.1) * self.monitor_y_dim)))
            self.add_widget(self.intereference_image_wid)
            self.interference_start_time = time.time()
            self.interference_active = True
            
        if (self.delay_clock_start == True) and (self.current_stage == 3) and (self.interference_active == False):
            self.intereference_image_wid_1 = ImageButton(source='%s\\Images\\yellow.png' % (self.curr_dir),
                                                    allow_stretch=True)
            self.intereference_image_wid_1.size_hint = (.08, .08)
            self.intereference_image_wid_1.pos = (
            (self.center_x - (0.05 * self.monitor_x_dim) + ((self.interfere_x_shift_1 * 0.1) * self.monitor_y_dim)),
            (self.center_y - (0.05 * self.monitor_y_dim) + ((self.interfere_y_shift_1 * 0.1) * self.monitor_y_dim)))
            self.intereference_image_wid_1.bind(on_press = self.interefere_1_press)
            
            self.intereference_image_wid_2 = ImageButton(source='%s\\Images\\yellow.png' % (self.curr_dir),
                                                    allow_stretch=True)
            self.intereference_image_wid_2.size_hint = (.08, .08)
            self.intereference_image_wid_2.pos = (
            (self.center_x - (0.05 * self.monitor_x_dim) + ((self.interfere_x_shift_2 * 0.1) * self.monitor_y_dim)),
            (self.center_y - (0.05 * self.monitor_y_dim) + ((self.interfere_y_shift_2 * 0.1) * self.monitor_y_dim)))
            self.intereference_image_wid_2.bind(on_press=self.interefere_2_press)
            
            self.intereference_image_wid_3 = ImageButton(source='%s\\Images\\yellow.png' % (self.curr_dir),
                                                    allow_stretch=True)
            self.intereference_image_wid_3.size_hint = (.08, .08)
            self.intereference_image_wid_3.pos = (
            (self.center_x - (0.05 * self.monitor_x_dim) + ((self.interfere_x_shift_3 * 0.1) * self.monitor_y_dim)),
            (self.center_y - (0.05 * self.monitor_y_dim) + ((self.interfere_y_shift_3 * 0.1) * self.monitor_y_dim)))
            self.intereference_image_wid_3.bind(on_press=self.interefere_3_press)

            self.distractor_image_wid_1 = ImageButton(source='%s\\Images\\red.png' % (self.curr_dir),
                                                         allow_stretch=True)
            self.distractor_image_wid_1.size_hint = (.08, .08)
            self.distractor_image_wid_1.pos = (
                (self.center_x - (0.05 * self.monitor_x_dim) + ((self.distractor_x_shift_1 * 0.1) * self.monitor_y_dim)),
                (self.center_y - (0.05 * self.monitor_y_dim) + ((self.distractor_y_shift_1 * 0.1) * self.monitor_y_dim)))

            self.distractor_image_wid_2 = ImageButton(source='%s\\Images\\red.png' % (self.curr_dir),
                                                         allow_stretch=True)
            self.distractor_image_wid_2.size_hint = (.08, .08)
            self.distractor_image_wid_2.pos = (
                (self.center_x - (0.05 * self.monitor_x_dim) + ((self.distractor_x_shift_2 * 0.1) * self.monitor_y_dim)),
                (self.center_y - (0.05 * self.monitor_y_dim) + ((self.distractor_y_shift_2 * 0.1) * self.monitor_y_dim)))

            self.distractor_image_wid_3 = ImageButton(source='%s\\Images\\red.png' % (self.curr_dir),
                                                         allow_stretch=True)
            self.distractor_image_wid_3.size_hint = (.08, .08)
            self.distractor_image_wid_3.pos = (
                (self.center_x - (0.05 * self.monitor_x_dim) + ((self.distractor_x_shift_3 * 0.1) * self.monitor_y_dim)),
                (self.center_y - (0.05 * self.monitor_y_dim) + ((self.distractor_y_shift_3 * 0.1) * self.monitor_y_dim)))
            
            self.add_widget(self.intereference_image_wid_1)
            self.add_widget(self.intereference_image_wid_2)
            self.add_widget(self.intereference_image_wid_3)

            self.add_widget(self.distractor_image_wid_1)
            self.add_widget(self.distractor_image_wid_2)
            self.add_widget(self.distractor_image_wid_3)
            self.interference_start_time = time.time()
            self.interference_active = True

        if ((self.current_time - self.interference_start_time) >= self.interference_presentation_length) and (self.interference_active == True) and (self.current_stage == 2):
            self.remove_widget(self.intereference_image_wid)
            self.interfere_x_shift = random.randint(-3,4)
            self.interfere_y_shift = random.randint(-3,4)

            while ((self.interfere_x_shift == self.sample_x_shift) and (self.interfere_y_shift == self.sample_y_shift)) or ((self.interfere_x_shift == self.choice_x_shift) and (self.interfere_y_shift == self.choice_y_shift)):
                self.interfere_x_shift = random.randint(-3, 4)
                self.interfere_y_shift = random.randint(-3, 4)
            self.interference_active = False
        if ((self.current_time - self.delay_start) >= self.iti_time) and (self.current_stage != 3):
            Clock.unschedule(self.sample_delay_end)
            self.initiation_image_wid = ImageButton(source='%s\\Images\\white.png' % (self.curr_dir),
                                                    allow_stretch=True)
            self.initiation_image_wid.size_hint = (.2, .1)
            self.initiation_image_wid.pos = ((self.center_x - (0.1 * self.monitor_x_dim)), (
                        self.center_y - (0.05 * self.monitor_y_dim) - (0.45 * self.monitor_y_dim)))
            self.initiation_image_wid.bind(on_press= self.choice_presentation)
            self.add_widget(self.initiation_image_wid)
        if (self.current_stage == 3) and (self.interfere_press >= 3):
            Clock.unschedule(self.sample_delay_end)
            self.interfere_press = 0
            self.interference_active == False
            
            self.remove_widget(self.intereference_image_wid_1)
            self.remove_widget(self.intereference_image_wid_2)
            self.remove_widget(self.intereference_image_wid_3)

            self.remove_widget(self.distractor_image_wid_1)
            self.remove_widget(self.distractor_image_wid_2)
            self.remove_widget(self.distractor_image_wid_3)
            
            self.initiation_image_wid = ImageButton(source='%s\\Images\\white.png' % (self.curr_dir),
                                                    allow_stretch=True)
            self.initiation_image_wid.size_hint = (.2, .1)
            self.initiation_image_wid.pos = ((self.center_x - (0.1 * self.monitor_x_dim)), (
                        self.center_y - (0.05 * self.monitor_y_dim) - (0.45 * self.monitor_y_dim)))
            self.initiation_image_wid.bind(on_press= self.choice_presentation)
            self.add_widget(self.initiation_image_wid)
    def interefere_1_press(self,*args):
        self.intereference_image_wid_1.source ='%s\\Images\\grey.png' % (self.curr_dir)
        self.interfere_press += 1
        self.intereference_image_wid_1.unbind(on_press = self.interefere_1_press)

    def interefere_2_press(self, *args):
        self.intereference_image_wid_2.source ='%s\\Images\\grey.png' % (self.curr_dir)
        self.interfere_press += 1
        self.intereference_image_wid_2.unbind(on_press=self.interefere_2_press)

    def interefere_3_press(self, *args):
        self.intereference_image_wid_3.source ='%s\\Images\\grey.png' % (self.curr_dir)
        self.interfere_press += 1
        self.intereference_image_wid_3.unbind(on_press=self.interefere_3_press)

    def choice_presentation(self,*args):
        self.delay_end = time.time()
        self.delay_length = self.delay_end - self.delay_start
        self.remove_widget(self.initiation_image_wid)

        self.sample_image_wid = ImageButton(source='%s\\Images\\white.png' % (self.curr_dir), allow_stretch=True)
        self.sample_image_wid.size_hint = (.08,.08)
        self.sample_image_wid.pos = ((self.center_x - (0.05*self.monitor_x_dim) + ((self.sample_x_shift * 0.1) * self.monitor_y_dim)), (self.center_y - (0.05*self.monitor_y_dim) + ((self.sample_y_shift * 0.1) * self.monitor_y_dim)))
        self.sample_image_wid.bind(on_press = self.response_incorrect)

        self.choice_image_wid = ImageButton(source='%s\\Images\\white.png' % (self.curr_dir), allow_stretch=True)
        self.choice_image_wid.size_hint = (.08,.08)
        self.choice_image_wid.pos = ((self.center_x - (0.05*self.monitor_x_dim) + ((self.choice_x_shift * 0.1) * self.monitor_y_dim)), (self.center_y - (0.05*self.monitor_y_dim) + ((self.choice_y_shift * 0.1) * self.monitor_y_dim)))
        self.choice_image_wid.bind(on_press = self.response_correct)

        self.add_widget(self.sample_image_wid)
        self.add_widget(self.choice_image_wid)

        self.image_pres_time = time.time()

    def response_correct(self,*args):
        self.image_touch_time = time.time()
        self.remove_widget(self.sample_image_wid)
        self.remove_widget(self.choice_image_wid)

        self.lat = self.image_touch_time - self.image_pres_time


        self.current_correct = 1
        self.current_total_correct += 1
        self.correction_active = False
        self.feedback_string = 'CORRECT'

        self.record_data()
        self.set_new_trial_configuration()



    def response_incorrect(self,*args):
        self.image_touch_time = time.time()
        self.remove_widget(self.choice_image_wid)
        self.remove_widget(self.sample_image_wid)

        self.lat = self.image_touch_time - self.image_pres_time

        self.correction_active = True
        self.feedback_string = 'INCORRECT - PLEASE TRY AGAIN'


        self.current_correct = 0
        self.record_data()
        self.start_iti()

    def record_data(self):
        self.data_file = open(self.participant_data_path, "a")
        self.data_file.write("\n")
        self.data_file.write("%s,[%s][%s]/[%s][%s],%s,%s,%s,%s" % (self.current_trial,self.sample_x_shift,self.sample_y_shift,self.choice_x_shift,self.choice_y_shift,self.current_correction,self.current_correct,self.lat,self.init_lat))
        self.data_file.close()

        if self.current_correct == 0:
            self.current_correction = 1
        if self.current_correct == 1:
            self.current_correction = 0

    def set_new_trial_configuration(self):

        self.current_correction = 0

        self.sample_x_shift = random.randint(-3,4)
        self.sample_y_shift = random.randint(-3,4)

        self.choice_x_shift = random.randint(-3,4)
        self.choice_y_shift = random.randint(-3,4)


        while (self.choice_x_shift == self.sample_x_shift) and (self.choice_y_shift == self.sample_y_shift):
            if (self.choice_x_shift == self.sample_x_shift) and (self.choice_y_shift == self.sample_y_shift):
                while (self.choice_x_shift == self.sample_x_shift) and (self.choice_y_shift == self.sample_y_shift):
                    self.choice_x_shift = random.randint(-3, 4)
                    self.choice_y_shift = random.randint(-3, 4)

        self.sample_coord = (self.sample_x_shift, self.sample_y_shift)
        self.choice_coord = (self.choice_x_shift, self.choice_y_shift)

        if self.current_total_correct >= self.stage_criteria:
            self.current_total_correct = 0
            self.current_stage += 1

        if self.current_stage == 2:
            self.interfere_x_shift = random.randint(-3,4)
            self.interfere_y_shift = random.randint(-3,4)

            while ((self.interfere_x_shift == self.sample_x_shift) and (self.interfere_y_shift == self.sample_y_shift)) or ((self.interfere_x_shift == self.choice_x_shift) and (self.interfere_y_shift == self.choice_y_shift)):
                self.interfere_x_shift = random.randint(-3, 4)
                self.interfere_y_shift = random.randint(-3, 4)

        if self.current_stage == 3:
            self.interfere_x_shift_1 = random.randint(-3,4)
            self.interfere_y_shift_1 = random.randint(-3,4)
            self.interfere_shift_1_coord = (self.interfere_x_shift_1,self.interfere_y_shift_1)

            self.interfere_x_shift_2 = random.randint(-3,4)
            self.interfere_y_shift_2 = random.randint(-3,4)
            self.interfere_shift_2_coord = (self.interfere_x_shift_2,self.interfere_y_shift_2)

            self.interfere_x_shift_3 = random.randint(-3,4)
            self.interfere_y_shift_3 = random.randint(-3,4)
            self.interfere_shift_3_coord = (self.interfere_x_shift_3,self.interfere_y_shift_3)
            
            self.distractor_x_shift_1 = random.randint(-3,4)
            self.distractor_y_shift_1 = random.randint(-3,4)
            self.distractor_shift_1_coord = (self.distractor_x_shift_1,self.distractor_y_shift_1)

            self.distractor_x_shift_2 = random.randint(-3,4)
            self.distractor_y_shift_2 = random.randint(-3,4)
            self.distractor_shift_2_coord = (self.distractor_x_shift_2,self.distractor_y_shift_2)

            self.distractor_x_shift_3 = random.randint(-3,4)
            self.distractor_y_shift_3 = random.randint(-3,4)
            self.distractor_shift_3_coord = (self.distractor_x_shift_3,self.distractor_y_shift_3)

            self.coordinate_list = [self.sample_coord, self.choice_coord, self.interfere_shift_1_coord,self.interfere_shift_2_coord,
                                    self.interfere_shift_3_coord,self.distractor_shift_1_coord,self.distractor_shift_2_coord,
                                    self.distractor_shift_3_coord]

            self.work_list = self.coordinate_list

            for pos in range(2,7):
                self.check_list = [0,1,2,3,4,5,6,7]
                self.check_list.remove(pos)
                for check in self.check_list:
                    if self.coordinate_list[pos] == self.coordinate_list[check]:
                        if pos == 2:
                            self.interfere_x_shift_1 = random.randint(-3, 4)
                            self.interfere_y_shift_1 = random.randint(-3, 4)
                            self.interfere_shift_1_coord = (self.interfere_x_shift_1, self.interfere_y_shift_1)
                        if pos == 3:
                            self.interfere_x_shift_2 = random.randint(-3, 4)
                            self.interfere_y_shift_2 = random.randint(-3, 4)
                            self.interfere_shift_2_coord = (self.interfere_x_shift_2, self.interfere_y_shift_2)
                        if pos == 4:
                            self.interfere_x_shift_3 = random.randint(-3, 4)
                            self.interfere_y_shift_3 = random.randint(-3, 4)
                            self.interfere_shift_3_coord = (self.interfere_x_shift_3, self.interfere_y_shift_3)
                        if pos == 5:
                            self.distractor_x_shift_1 = random.randint(-3, 4)
                            self.distractor_y_shift_1 = random.randint(-3, 4)
                            self.distractor_shift_1_coord = (self.distractor_x_shift_1, self.distractor_y_shift_1)
                        if pos == 6:
                            self.distractor_x_shift_2 = random.randint(-3, 4)
                            self.distractor_y_shift_2 = random.randint(-3, 4)
                            self.distractor_shift_2_coord = (self.distractor_x_shift_2, self.distractor_y_shift_2)
                        if pos == 7:
                            self.distractor_x_shift_3 = random.randint(-3, 4)
                            self.distractor_y_shift_3 = random.randint(-3, 4)
                            self.distractor_shift_3_coord = (self.distractor_x_shift_3, self.distractor_y_shift_3)




        self.current_trial += 1
        self.start_iti()

    def start_iti(self):
        self.start_iti_time = time.time()
        self.feedback_wid = Label(text=self.feedback_string, font_size='50sp')
        self.feedback_wid.size_hint = (.5,.3)
        self.feedback_wid.pos = ((self.center_x - (0.25 * self.monitor_x_dim)),(self.center_y - (0.15*self.monitor_y_dim) + (0.48*self.monitor_y_dim)))
        self.add_widget(self.feedback_wid)
        self.iti_clock_trigger = False
        self.end_iti()

    def end_iti(self,*args):
        if self.iti_clock_trigger == False:
            Clock.schedule_interval(self.end_iti, 0.01)
            self.iti_clock_trigger = True
        if (self.current_time - self.start_iti_time) >= self.iti_time:
            Clock.unschedule(self.end_iti)
            self.remove_widget(self.feedback_wid)
            self.trial_initiation()

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