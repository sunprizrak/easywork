from kivy.lang import Builder
from kivymd.app import MDApp
import os, sys
from kivy.resources import resource_add_path, resource_find


class MainApp(MDApp):

    def build(self):
        kiv_file = Builder.load_file('main.kv')
        return kiv_file


if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    MainApp().run()