def Route_Switch(protocol,parameters):
    if protocol == 'TUNL':
        trial_max = parameters[0]
        session_max = parameters[1]
        block_length = parameters[2]
        block_count = parameters[3]
        id_entry = parameters[4]
        import Protocols.TUNL as prt
        main_app = prt.Experiment_App()
        main_app.set(trial_max=trial_max,session_max=session_max,block_length=block_length,block_count=block_count,id_entry=id_entry)
        main_app.run()
    elif protocol == 'PR':
        trial_max = parameters[0]
        session_max = parameters[1]
        block_length = parameters[2]
        block_count = parameters[3]
        id_entry = parameters[4]
        import Protocols.PR as prt
        main_app = prt.Experiment_App()
        main_app.set(trial_max=trial_max,session_max=session_max,block_length=block_length,block_count=block_count,id_entry=id_entry)
        main_app.run()
        
    elif protocol == 'PR2':
        session_max = parameters[0]
        reward_type = parameters[1]
        id_entry = parameters[2]
        import Protocols.PR2 as prt
        main_app = prt.Experiment_App()
        main_app.set(session_max=session_max,reward_type=reward_type,id_entry=id_entry)
        main_app.run()

    elif protocol == 'vPRL':
        import Protocols.vPRL as prt

        trial_max = parameters[0]
        session_max = parameters[1]
        reversal_threshold = parameters[2]
        max_reversal = parameters[3]
        reward_prob = parameters[4]
        id_entry = parameters[5]

        import Protocols.vPRL as prt

        Activate()
        main_app = prt.Experiment_App()
        main_app.set(trial_max=trial_max,session_max=session_max,reversal_threshold=reversal_threshold,max_reversal=max_reversal,reward_prob=reward_prob,id_entry=id_entry)
        main_app.run()
    elif protocol == 'PAL':
        trial_max = parameters[0]
        session_max = parameters[1]
        block_length = parameters[2]
        block_count = parameters[3]
        id_entry = parameters[4]
        
        import Protocols.PAL as prt
        Activate()
        main_app = prt.Experiment_App()
        main_app.set(trial_max=trial_max,session_max=session_max,block_length=block_length,block_count=block_count,id_entry=id_entry)
        main_app.run()
    elif protocol == 'iCPT':
        trial_max= parameters[0]
        session_max = parameters[1]
        block_max = parameters[2]
        block_count = parameters[3]
        probe_check = parameters[4]
        id_entry = parameters[5]

        import Protocols.iCPT as prt
        Activate()
        main_app = prt.Experiment_App()
        main_app.set(trial_max=trial_max,session_max = session_max, block_max=block_max, block_count = block_count, probe_check = probe_check, id_entry = id_entry)
        main_app.run()
    elif protocol == 'iCPT2':
        trial_max= parameters[0]
        session_max = parameters[1]
        block_max = parameters[2]
        block_count = parameters[3]
        stimulus_duration = parameters[4]
        limited_hold = parameters[5]
        target_prob = parameters[6]
        probe_check = parameters[7]
        id_entry = parameters[8]

        import Protocols.iCPT2 as prt
        Activate()
        main_app = prt.Experiment_App()
        main_app.set(trial_max=trial_max,session_max = session_max, block_max=block_max, block_count = block_count,stimulus_duration=stimulus_duration,
                     limited_hold=limited_hold,target_prob=target_prob,probe_check = probe_check, id_entry = id_entry)
        main_app.run()
    elif protocol == 'iCPTImage2':
        trial_max= parameters[0]
        session_max = parameters[1]
        block_max = parameters[2]
        block_count = parameters[3]
        probe_check = parameters[4]
        id_entry = parameters[5]

        import Protocols.iCPTImage2 as prt
        Activate()
        main_app = prt.Experiment_App()
        main_app.set(trial_max=trial_max,session_max = session_max, block_max=block_max, block_count = block_count, probe_check = probe_check, id_entry = id_entry)
        main_app.run()
    elif protocol == 'iCPTStimDurationScreen':
        trial_max= parameters[0]
        session_max = parameters[1]
        id_entry = parameters[2]

        import Protocols.iCPTStimDurationScreen as prt
        Activate()
        main_app = prt.Experiment_App()
        main_app.set(trial_max=trial_max,session_max = session_max, id_entry = id_entry)
        main_app.run()
    elif protocol == 'iCPTImageScreen':
        trial_max= parameters[0]
        session_max = parameters[1]
        id_entry = parameters[2]

        import Protocols.iCPTImageScreen as prt
        Activate()
        main_app = prt.Experiment_App()
        main_app.set(trial_max=trial_max,session_max = session_max, id_entry = id_entry)
        main_app.run()
    elif protocol == 'iCPTStimImageScreen':
        trial_max= parameters[0]
        session_max = parameters[1]
        id_entry = parameters[2]

        import Protocols.iCPTStimImageScreen as prt
        Activate()
        main_app = prt.Experiment_App()
        main_app.set(trial_max=trial_max,session_max = session_max, id_entry = id_entry)
        main_app.run()

def Activate():
    import os
    import sys
    curr_dir = os.getcwd()
    if sys.platform == 'linux'or sys.platform == 'darwin':
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
    

    from kivy.config import Config
    from kivy.core.window import Window
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
    from kivy.uix.image import Image
    from kivy.uix.behaviors import ButtonBehavior
    class ImageButton(ButtonBehavior, Image):
        def __init__(self, **kwargs):
            super(ImageButton, self).__init__(**kwargs)

    #self.monitor_x_dim = Window.size[0]
    #self.monitor_y_dim = WIndow.size[1]


