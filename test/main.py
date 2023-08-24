from kivy.lang import Builder
from kivy.app import App


class MainApp(App):

    def build(self):
        kiv_file = Builder.load_file('main.kv')
        return kiv_file


if __name__ == '__main__':
    MainApp().run()