import random
import os
import time
import sys
from kivy.config import Config
curr_dir = os.getcwd() # Get Current Working Directory
if sys.platform == 'linux' or sys.platform == 'darwin': # GENERAL: Check if Linux or Mac (Darwin) Operating System
    config_path = curr_dir + '/Configuration.ttconfig'
elif sys.platform == 'win32': # GENERAL: Check if Windows Operating System
    config_path = curr_dir + '\\Configuration.ttconfig' # Set filepath for monitor resolution configuration file
    
config_file = open(config_path,'r') # Open config file
configurations = config_file.readlines() # Read in configuration content to list
monitor_x_dim = configurations[0] # Read x-dimension row
monitor_x_dim = monitor_x_dim.replace('x_dim = ','') # Substitute and remove x_dim = 
monitor_x_dim = monitor_x_dim.replace('\n','') # Substitute and remove the new row string
monitor_x_dim = int(monitor_x_dim) # Convert remaining number into an integer
monitor_y_dim = configurations[1] # Repeat of process for y-dimension
monitor_y_dim = monitor_y_dim.replace('y_dim = ','')
monitor_y_dim = monitor_y_dim.replace('\n','')
monitor_y_dim = int(monitor_y_dim)
fullscreen = configurations[2]
fullscreen = fullscreen.replace('fullscreen = ','') # Repeat of process for fullscreen settingh
fullscreen = fullscreen.replace('\n','')
fullscreen = str(fullscreen) # Convert fullscreen setting to a string value
config_file.close()

Config.set('kivy', 'keyboard_mode', 'systemandmulti') # Set keyboard mode
Config.set('graphics', 'fullscreen', fullscreen) # Enable fullscreen setting (On or Off)
Config.set('graphics', 'width', monitor_x_dim) # Set application X resolution (width)
Config.set('graphics', 'height', monitor_y_dim) # Set application Y resolution (height)
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.uix.vkeyboard import VKeyboard
from functools import partial


class ImageButton(ButtonBehavior,Image): # This is the class object that merges the properties of a Kivy Image with A Kivy Button
    def __init__(self,**kwargs):
        super(ImageButton,self).__init__(**kwargs)

        self.on_press_movement_time = 0
        self.on_press_movement_distance = 0
        self.on_press_movement_bouts
        self.on_release_latency = 0
        self.on_press_position = [0,0]
        self.on_release_position = [0,0]

        self.hold_start_time = 0

        

    def on_press(self):
        self.hold_start_time = time.time()
        Clock.schedule_interval(self.monitor_process,0.01)

    def on_release(self):

    def monitor_process(self):
        

class Experiment_Staging(FloatLayout): # Float Layout application
    def __init__(self,trial_max,session_max,block_max,block_count,probe_check,id_entry,**kwargs): # Initializing function: Takes in arguments from initializer
        super(Experiment_Staging,self).__init__(**kwargs) # Command to initialize application
        
        self.curr_dir = os.getcwd() # Set current working directory within class
        if sys.platform == 'linux' or sys.platform == 'darwin': # Find monitor configuration
            self.config_path = self.curr_dir + '/Configuration.ttconfig'
        elif sys.platform == 'win32':
            self.config_path = self.curr_dir + '\\Configuration.ttconfig'
            
        self.config_file = open(self.config_path,'r') # Internal repeat of monitor configuration
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
        
        if sys.platform == 'linux' or sys.platform == 'darwin': # Set key defaults for file systems depending on operating system
            self.data_add = '/Data'
            self.delay_hold_path = '%s/Images/white.png' % (self.curr_dir)
            self.folder_symbol = '/'
        elif sys.platform == 'win32':
            self.data_add = '\\Data'
            self.delay_hold_path = '%s\\Images\\white.png' % (self.curr_dir)
            self.folder_symbol = '\\'


        self.trial_displayed = False # Boolean value to track whether stimuli is on screen or not
        self.data_dir = self.curr_dir + self.data_add # Data directory
        if not os.path.exists(self.data_dir): # If data directory missing, is automatically generated
            os.makedirs(self.data_dir)

        self.current_stage = 0 # Set default starting training stage. Default = 0, Training Phase
        self.stage_label = 'Train' # String information for current stage. Is used for the data output
        self.stage_executed = False

        self.presentation_delay_start = False
        self.image_on_screen = False # Boolean value to check whether stimuli is still active
        self.feedback_displayed = False # Boolean value to check whether feedback is being presented
        self.hold_removed = False # Boolean value for whether finger is off delay hold button
        self.not_pressed = True

        self.probe_check = [int(x) for x in probe_check] # List of all stages active for current experiment. Will include training, main stage, and any probes selected in checkbox

        self.delay_length = 4 # Length of delay (integer)

        self.max_trials = trial_max #Generate maximum trial count from initializer
        self.max_time = session_max # Generate session maximum time from initializer
        self.id_no = id_entry # Generate animal ID from initializer

        self.current_trial = 1 # Integer value for current trial number
        self.current_total_hits = 0 # Integer value for current number of hits that are completed
        self.hit_threshold = block_max # Integer value specifying the hit threshold per block. Is collected from initializer
        self.threshold_increment = self.hit_threshold # Integer value specifying how much the threshold should increment following a block. Is set from the initial hit threshold
        self.block_count = block_count # Integer value specifying the number of blocks to be completed. Is collected from initializer
        self.current_stage = 0 # 0=train 1=main, 2=sd probe, 3=iti, 4=contrast,5=flanker
        self.time_elapsed = 0 # Float value specifying the total time active in experiment
        self.start_time = time.time() # Generate current time as of the program initialization.
        self.start_iti_time = 0 # Float value to hold the start time for the inter-trial interval

        self.current_block = 1 # Integer value to encode which block the protocol is current set to
        self.probe_pos = 0 # Integer value to specify the current position in probe
        self.start_pos = 0 # Integer value to specify the current start position

        self.image_contact_lat = 0 # Float value to hold the contact latency
        self.image_contact_start = 0 # Float value to hold the start time of the latency event


        self.iti_time = 0.5 # Float value to hold the length of the inter-trial interval
        self.presentation_delay_time = 1 # Float value to hold the length of time following the initial presentation following instructions
        self.feedback_length = 0.5 # Float value to hold the length of time feedback is presented on the screen
        self.stimulus_duration = 1 # Float value to hold the length of time images remain on the screen
        self.block_hold_time = 5 # Float value to hold the length of time a block must be active before the continue option appears

        self.image_list = ['horizontal','horizontal','horizontal','horizontal','vertical','left','right','rings'] # Image list. Frequency of values sets the probability of outcomes.
        self.image_list_pos = random.randint(0,7) # Generate a random index position
        self.current_image = 'snowflake' # For training stage, sets the training image to snowflake
        
        self.contrast_list = ['','-50','-25','-125'] # Contract string list: Holds the contrast values
        self.contrast_list_pos = random.randint(0,3) # Generate a random index position for contrast
        self.image_name_contrast = '%s%s' % (
        self.image_list[self.image_list_pos], self.contrast_list[self.contrast_list_pos]) # Generate Image Contrast Filename based on merged parameters

        self.distractor_active = random.randint(0,1) # Random integer to specify whether a distractor trial will be occuring
        self.distractor_congruent = random.randint(0,1) # Random integer to specify whether a given distractor trial will be congruent or incongruent
        if self.distractor_active == 1: # Condition for if a distractor is active (Not run typically in initialization unless user modified)
            if self.distractor_congruent == 0:
                if self.image_list[self.image_list_pos] == 'horizontal':
                    self.distractor_image_pos = random.randint(4, 7)
                else:
                    self.distractor_image_pos = 0
            elif self.distractor_congruent == 1:
                self.distractor_image_pos = self.image_list_pos

        self.stimulus_duration_list = [1,0.75,0.66,0.5] # Stimulus Duration List for SD Probe
        self.stimulus_duration_pos = random.randint(0,3) # Generate a random index position for stimulus duration

        self.iti_duration_list = [0.5,1,2] # Inter-Trial Interval List for ITI Probe
        self.iti_duration_pos = random.randint(0,2) # Generate a random index position for ITI

        self.lat = 0 # Float value for latency length
        self.init_lat = 0 # Float value for initiation latency following a response

        self.current_correct = 0 # Interger value for holding whether a current trial is correct or incorrect
        self.current_correction = 0 # Integer value for determining whether the current trial is of the correction trial type

        self.delay_hold_button = ImageButton(source=self.delay_hold_path, allow_stretch=True) # Generate an Imagebutton for the hold button
        self.delay_hold_button.size_hint = (.24,.24) # Size hint to generate image dimensions
        self.delay_hold_button.pos = ((self.center_x - (0.12 * self.monitor_x_dim)),(self.center_y - (0.12 * self.monitor_y_dim) - (0.4 * self.monitor_y_dim))) # Generate x,y position for delay button

        Clock.schedule_interval(self.clock_update, 0.001) # Schedule a function to update the current clock for the experiment. Will remain active for the duration
        self.id_setup() # Run ID Setup Function


    def id_setup(self):
        self.participant_data_folder = self.data_dir + self.folder_symbol + self.id_no + self.folder_symbol # Create participant data folder
        if os.path.exists(self.participant_data_folder) == False: # If folder is not in existence, create it
            os.makedirs(self.participant_data_folder)
        self.participant_data_path = self.participant_data_folder + 'iCPT %s.csv' % (self.id_no) # Set file name for participant including task name and ID number
        self.data_col_names = 'TrialNo, Stage, Block #, Trial Type, Correction Trial, Correct, Response Latency' # String containing data file column names
        self.data_file = open(self.participant_data_path, "w+") # Open new file in write mode
        self.data_file.write(self.data_col_names) # Write column names to new file
        self.data_file.close() # Close file

        self.instruction_presentation() # Proceed to Instruction Presentation

    def instruction_presentation(self):
        self.instruction_label = Label(text= 'During the experiment, hold your finger on the white square before responding .\nTo make a response, press on one of the images on the centre of the screen.\nYou will receive feedback following touching an image.'
                                       , font_size = '35sp',text_size = ((0.8*self.monitor_x_dim),(0.4*self.monitor_y_dim))) # Generate string for instructions
        self.instruction_label.size_hint = (0.6,0.4)
        self.instruction_label.pos = ((self.center_x - (0.3 * self.monitor_x_dim)),(self.center_y - (0.2*self.monitor_y_dim) + (0.2*self.monitor_y_dim)))

        self.initiate_button = Button(text='Press to Begin') # Generate start button
        self.initiate_button.size_hint = (.1,.1)
        self.initiate_button.pos = ((self.center_x - (0.05 * self.monitor_x_dim)),(self.center_y - (0.05*self.monitor_y_dim) - (0.2*self.monitor_y_dim)))
        self.initiate_button.bind(on_press = self.clear_instruction)
        self.add_widget(self.instruction_label) # Add widget to display
        self.add_widget(self.initiate_button)

    def clear_instruction(self,*args):
        self.remove_widget(self.instruction_label) # Remove widget to display
        self.remove_widget(self.initiate_button)
        self.start_time = time.time() # Get start time updated at point of instructions being complete
        self.trial_initiation() # Initialize Trial

    def trial_initiation(self):
        self.initiation_image_wid = ImageButton(source=self.delay_hold_path, allow_stretch=True) # Initiation Button Widget
        self.initiation_image_wid.size_hint = (.24,.24)
        self.initiation_image_wid.pos = ((self.center_x - (0.12 * self.monitor_x_dim)),(self.center_y - (0.12 * self.monitor_y_dim) - (0.4 * self.monitor_y_dim)))
        self.initiation_image_wid.bind(on_press= self.initiation_detected) # Bind function to press event on initiation button
        self.add_widget(self.initiation_image_wid)
        self.initiation_start_time = time.time() # Initiation start time

    def initiation_detected(self,*args):
        self.remove_widget(self.initiation_image_wid) # Remove widget
        self.delay_hold_button.bind(on_release= self.premature_response) # Bind function to release of delay hold button - Premature Response
        self.add_widget(self.delay_hold_button)
        self.initiation_end_time = time.time()
        self.init_lat = self.initiation_end_time - self.initiation_start_time # Get initiation latency value
        self.presentation_delay() # Start Presentation Delay

    def presentation_delay(self,*args):
        if self.presentation_delay_start == False:
            self.presentation_delay_start_time = time.time() # Get start time
            Clock.schedule_interval(self.presentation_delay,0.01) # Repeat function on clock/repeat until delay is complete
            self.presentation_delay_start = True
        if (self.current_time - self.presentation_delay_start_time) >= self.presentation_delay_time: # Conditional to check if delay is complete
            Clock.unschedule(self.presentation_delay) # Remove function off clock/repeat
            self.presentation_delay_start = False # Reset boolean flag
            self.image_presentation() # Start Presentation

    def image_presentation(self,*args):
        if self.image_on_screen == False:
            self.delay_hold_button.unbind(on_release=self.premature_response)
            self.delay_hold_button.bind(on_release=self.hold_removed_presentation)
            self.delay_hold_button.bind(on_press=self.hold_returned_presentation) # Reset bindings
            if self.current_stage == 4: # Generate Contrast Target if probe is active
                if sys.platform == 'linux'or sys.platform == 'darwin':
                    self.image_path = '%s/Images/%s.png' % (self.curr_dir, self.image_name_contrast)
                elif sys.platform == 'win32':
                    self.image_path = '%s\\Images\\%s.png' % (self.curr_dir, self.image_name_contrast)
                self.image_wid = ImageButton(
                    source=self.image_path,allow_stretch=True)
                
            elif self.current_stage == 0: # Else If condition produce training image if during training
                if sys.platform == 'linux'or sys.platform == 'darwin':
                    self.image_path = '%s/Images/snowflake.png' % (self.curr_dir)
                elif sys.platform == 'win32':
                    self.image_path = '%s\\Images\\snowflake.png' % (self.curr_dir)
                self.image_wid = ImageButton(source=self.image_path,allow_stretch=True)
                self.current_image = 'snowflake'
            else: # Else condition to trigger normal presentation for main, SD, ITI, and Flanker probe
                if sys.platform == 'linux'or sys.platform == 'darwin':
                    self.image_path = '%s/Images/%s.png' % (self.curr_dir, self.image_list[self.image_list_pos])
                elif sys.platform == 'win32':
                    self.image_path = '%s\\Images\\%s.png' % (self.curr_dir, self.image_list[self.image_list_pos])
                self.image_wid = ImageButton(source=self.image_path, allow_stretch=True)
                
            self.image_wid.size_hint = (.4, .4)
            self.image_wid.pos = (
            (self.center_x - (0.2 * self.monitor_x_dim)), (self.center_y - (0.2 * self.monitor_y_dim)))
            self.image_wid.bind(on_press= self.image_pressed)
            if self.current_stage == 5 and self.distractor_active == 1: # Conditional to check if flanker task with an active distractor
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
            self.image_pres_time = time.time() # Start of image presentation
            self.image_on_screen = True
            Clock.schedule_interval(self.image_presentation,0.01) # Check protocol to determine if presentation time has expired
        if (self.current_time - self.image_pres_time) >= self.stimulus_duration: # Conditional to determine if stimulus duration timer has finished
            Clock.unschedule(self.image_presentation) # Unschedule Protocol
            self.feedback_string = '' # Disable feedback string
            self.remove_widget(self.image_wid)
            if self.current_stage == 5 and self.distractor_active == 1: # Remove distractors if presented
                self.remove_widget(self.distractor_one_wid)
                self.remove_widget(self.distractor_two_wid)
            if (self.image_list[self.image_list_pos] == 'horizontal') or (self.current_image == 'snowflake'): # Check if trial is a miss
                self.current_correct = 0
                self.trial_contingency = 4
            else: # Else event occurs if event was a correct rejection
                self.current_correct = 1
                self.trial_contingency = 3
            self.lat = '' # No latency for non-pressed response
            self.not_pressed = True
            self.record_data() # Activate data record function
            if self.hold_removed == True:
                self.hold_not_returned() # Check if hold position not active
                return
            self.set_new_trial_configuration() # Generate new trial configuration



    def image_pressed(self,*args):
        Clock.unschedule(self.image_presentation) # Unschedule image presentation if a response is made
        self.image_contact_start = time.time() # Get the image contact time
        self.remove_widget(self.image_wid)
        self.delay_hold_button.unbind(on_release=self.hold_removed_presentation)
        self.delay_hold_button.unbind(on_press=self.hold_returned_presentation)
        self.not_pressed = False
        if self.current_stage == 5 and self.distractor_active == 1: # Remove Distractors if active
            self.remove_widget(self.distractor_one_wid)
            self.remove_widget(self.distractor_two_wid)
        if (self.image_list[self.image_list_pos] == 'horizontal') | (self.current_image == 'snowflake'): # Check if trial is correct
            self.response_correct() # Activate correct response contigency
        else:
            self.response_incorrect() # Activate incorrect response contingency

    def response_correct(self):
        self.image_touch_time = time.time() # Get the final touch time

        self.lat = self.image_touch_time - self.image_pres_time # Generate the image touch latency


        self.current_correct = 1 # Set flag to correct
        self.trial_contingency = 1 # Set trial contingency
        self.current_total_hits += 1 # Increment total number of hits
        self.correction_active = False # Set correction flag to False
        self.feedback_string = '[color=008000]CORRECT[/color]' # Set feedback string


        self.delay_hold_button.bind(on_press=self.start_iti)
        if (self.current_total_hits < 10 and self.current_stage =
            = 0) or ((self.current_total_hits < (self.hit_threshold) and (self.current_stage != 0))):
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

        self.image_list_pos = random.randint(0,7)
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
        if (self.current_block >= self.block_count) and (self.current_stage > 0):
            self.current_block = 0
            if self.current_stage == 5:
                self.end_experiment_screen()
                return
            self.start_pos = self.probe_pos
            for probe in range(self.start_pos,6):
                self.current_stage += 1
                if self.current_stage > 5:
                    self.end_experiment_screen()
                    return
                if int(self.probe_check[self.probe_pos]) == 1:
                    self.probe_pos += 1
                    self.start_pos = self.probe_pos
                    break
                else:
                    self.probe_pos += 1
                    
            

        self.current_block += 1
        self.presentation_delay_time = 1
        self.stimulus_duration = 1
        self.current_trial -= 1
        self.hit_threshold += self.threshold_increment
        
        if self.current_stage == 0:
            self.current_stage = 1
            self.current_block -= 1
            self.hit_threshold -= self.threshold_increment
            self.hit_threshold += 10
            self.stage_label == 'Main Task'
        if self.current_stage == 1:
            self.stage_label = 'Main Task'
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
        experiment = Experiment_Staging(trial_max=self.trial_maximum,session_max=self.session_maximum,block_max = self.block_max,block_count=self.block_count, probe_check = self.probe_check,id_entry=self.id_value)
        return experiment
    def set(self,trial_max,session_max,block_max,block_count,probe_check,id_entry):
        self.trial_maximum = trial_max
        self.session_maximum = session_max
        self.block_max = block_max
        self.block_count = block_count
        self.probe_check = probe_check
        self.id_value = id_entry

if __name__ == '__main__':
    Experiment_App().run()
