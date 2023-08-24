from kivy.lang import Builder
from kivy.app import App


KV = '''
Screen:

    BoxLayout:
        canvas:
            Color:
                rgba: .3, .3, .3, 1
            Rectangle:
                size: self.size
                pos: self.pos
'''


class MainApp(App):

    def build(self):
        kiv_file = Builder.load_string(KV)
        return kiv_file


if __name__ == '__main__':
    MainApp().run()