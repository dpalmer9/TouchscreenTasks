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
import random

class Experiment_Staging(FloatLayout):
    def __init__(self,**kwargs):
        super(Experiment_Staging,self).__init__(**kwargs)
        self.monitor_x_dim = GetSystemMetrics(0)
        self.monitor_y_dim = GetSystemMetrics(1)
        self.size = (self.monitor_x_dim,self.monitor_y_dim)


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

    def main_loop(self):
        self.trial_count = 72
        self.trial_type = [1,2,3,4,5,6]
        self.correct_image = ['left','left','horizontal','horizontal','right','right']
        self.incorrect_image ['right','horizontal','right','left','horizontal','left']


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