from kivy.storage.jsonstore import JsonStore
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.theming import ThemeManager
from kivy.core.text import LabelBase


class CustomThemeManager(ThemeManager):
    def __init__(self, **kwargs):
        super(CustomThemeManager, self).__init__(**kwargs)
        self.theme_style = 'Dark'
        self.font_styles.update({
            "Button": ["GlossySheen", 21, True, 1.25],
        })
        LabelBase.register(name='GlossySheen', fn_regular='assets/font/GlossySheenRegular.ttf')


class MainApp(MDApp):

    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.title = 'EasyWork'
        self.theme_cls = CustomThemeManager()
        self.storage = JsonStore('storage.json')

    def build(self):
        kv_file = Builder.load_file('kv_files/layout.kv')
        return kv_file


if __name__ == '__main__':
    MainApp().run()