from kivy.properties import ObjectProperty
from utility.ocr import Ocr
from widgets import BaseScreen


class MainScreen(BaseScreen):

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.table = ObjectProperty()

    def start(self):
        ocr = Ocr()
        ocr()

