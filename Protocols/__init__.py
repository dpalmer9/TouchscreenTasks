from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

class ImageButton(ButtonBehavior,Image):
    def __init__(self,**kwargs):
        super(ImageButton,self).__init__(**kwargs)

def Route_Switch(protocol):
    if protocol == 'TUNL':
        import Protocols.TUNL as prt
    elif protocol == 'vPRL':
        import Protocols.vPRL as prt
    elif protocol == 'PAL':
        import Protocols.PAL as prt
    elif protocol == 'iCPT':
        import Protocols.iCPT as prt

    prt.Experiment_Configuration()