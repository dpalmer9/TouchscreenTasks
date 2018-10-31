import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from win32api import GetSystemMetrics
from kivy.core.window import Window
from kivy.config import Config
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock
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


        self.instruction_label = Label(text= 'To make a response, press on one of the images on the screen.\nYou will receive feedback following a response.')
        self.instruction_label.size_hint = (.5,.2)
        self.instruction_label.pos = ((self.center_x - (0.25 * self.monitor_x_dim)),(self.center_y - (0.1*self.monitor_y_dim) + (0.2*self.monitor_y_dim)))

        self.initiate_button = Button(text='Press to Start')
        self.initiate_button.size_hint = (.1,.1)
        self.initiate_button.pos = ((self.center_x - (0.05 * self.monitor_x_dim)),(self.center_y - (0.05*self.monitor_y_dim) - (0.2*self.monitor_y_dim)))
        self.initiate_button.bind(on_press = self.initiate_button_func)


        self.add_widget(self.instruction_label)
        self.add_widget(self.initiate_button)


    def initiate_button_func(self,instance):
        self.remove_widget(self.instruction_label)
        self.remove_widget(self.initiate_button)
        self.set_experiment_parameters()

    def set_experiment_parameters(self):
        self.trial_count = 72
        self.trial_type = [1,2,3,4,5,6]
        self.correct_image = ['left','left','horizontal','horizontal','right','right']
        self.incorrect_image = ['right','horizontal','right','left','horizontal','left']
        self.c_pos_mod = [-0.3,-0.3,0,0,0.3,0.3]
        self.i_pos_mod = [0,0.3,-0.3,0.3,-0.3,0]
        self.curr_trial_type = random.randint(0,5)
        self.current_trial = 1
        self.correction_active = False
        self.iti_time = 5

        self.correct_lat = 0
        self.correct_lat_list = []
        self.incorrect_lat = 0
        self.incorrect_lat_list = []

        self.correct_trials = 0

        self.correction_no = 0


        self.trial_presentation()

    def set_new_trial_configuration(self):
        self.curr_trial_type = random.randint(0,5)
        self.current_trial += 1
        self.ITI_interval()

    def ITI_update(self,*args):
        self.current_time = time.time()
        if (self.current_time - self.start_time) >= self.iti_time:
            Clock.unschedule(self.ITI_update)
            self.remove_widget(self.feedback_wid)
            self.trial_presentation()

    def ITI_interval(self):
        self.start_time = time.time()
        self.current_time = time.time()
        self.feedback_wid = Label(text=self.feedback_string, font_size='25sp')
        self.feedback_wid.size_hint = (.5,.3)
        self.feedback_wid.pos = ((self.center_x - (0.25 * self.monitor_x_dim)),(self.center_y - (0.15*self.monitor_y_dim)))
        self.add_widget(self.feedback_wid)

        Clock.schedule_interval(self.ITI_update,0.25)



    def trial_presentation(self):
        if self.current_trial >= self.trial_count:
            App.get_running_app().stop()

        self.correct_image_wid = ImageButton(source='%s\\Images\\%s.png' % (self.curr_dir, self.correct_image[self.curr_trial_type]))
        self.correct_image_wid.size_hint = (.2,.2)
        self.correct_image_wid.pos = ((self.center_x - (0.1 * self.monitor_x_dim) + (self.c_pos_mod[self.curr_trial_type] * self.monitor_x_dim)), (self.center_y - (0.1*self.monitor_y_dim)))
        self.correct_image_wid.bind(on_press = self.response_correct)

        self.incorrect_image_wid = ImageButton(source='%s\\Images\\%s.png' % (self.curr_dir,self.incorrect_image[self.curr_trial_type]))
        self.incorrect_image_wid.size_hint = (.2,.2)
        self.incorrect_image_wid.pos = ((self.center_x - (0.1 * self.monitor_x_dim) + (self.i_pos_mod[self.curr_trial_type] * self.monitor_x_dim)), (self.center_y - (0.1*self.monitor_y_dim)))
        self.incorrect_image_wid.bind(on_press = self.response_incorrect)

        self.add_widget(self.correct_image_wid)
        self.add_widget(self.incorrect_image_wid)

        self.image_pres_time = time.time()

    def response_correct(self,instance):
        self.image_touch_time = time.time()
        self.remove_widget(self.correct_image_wid)
        self.remove_widget(self.incorrect_image_wid)

        if self.correction_active == False:
            self.correct_lat = self.image_touch_time - self.image_pres_time
            self.correct_lat_list.append(self.correct_lat)
            self.correct_trials += 1

        self.correction_active == False
        self.feedback_string = 'CORRECT'

        self.set_new_trial_configuration()



    def response_incorrect(self,instance):
        self.image_touch_time = time.time()
        self.remove_widget(self.correct_image_wid)
        self.remove_widget(self.incorrect_image_wid)

        if self.correction_active == False:
            self.incorrect_lat = self.image_touch_time - self.image_pres_time
            self.incorrect_lat_list.append(self.incorrect_lat)
        elif self.correction_active == True:
            self.correction_no += 1

        self.correction_active = True
        self.feedback_string = 'INCORRECT - PLEASE TRY AGAIN'

        self.ITI_interval()

class PALApp(App):
    def build(self):
        experiment = Experiment_Staging()
        return experiment

if __name__ == '__main__':
    Config.set('graphics','fullscreen','1')
    monitor_x_dim = GetSystemMetrics(0)
    monitor_y_dim = GetSystemMetrics(1)
    Window.size = (monitor_x_dim,monitor_y_dim)
    Window.fullscreen = True
    PALApp().run()