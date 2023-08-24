from kivy.lang import Builder
from kivymd.app import MDApp


KV = '''
MDScreen:
    MDBoxLayout:
        md_bg_color: 'green'
'''


class MainApp(MDApp):

    def build(self):
        kiv_file = Builder.load_string(KV)
        return kiv_file


if __name__ == '__main__':
    MainApp().run()