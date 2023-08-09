import os

from kivy.metrics import dp
from kivy.storage.jsonstore import JsonStore
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.theming import ThemeManager
from kivy.core.text import LabelBase
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import MDSnackbar


class CustomThemeManager(ThemeManager):
    def __init__(self, **kwargs):
        super(CustomThemeManager, self).__init__(**kwargs)
        self.theme_style = 'Dark'
        self.font_styles.update({
            "Button": ["GlossySheen", 21, True, 1.25],
        })

        font_path = os.sep.join(['assets', 'font', 'GlossySheenRegular.ttf'])

        LabelBase.register(name='GlossySheen', fn_regular=font_path)


class MainApp(MDApp):

    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.title = 'EasyWork'
        self.theme_cls = CustomThemeManager()
        self.storage = JsonStore('storage.json')
        self.dialog = None

    def build(self):
        layout_path = os.sep.join(['kv_files', 'layout.kv'])
        print(layout_path)
        kv_file = Builder.load_file(layout_path)
        return kv_file

    def open_snackbar(self, **kwargs):
        MDSnackbar(
            MDLabel(
                text=kwargs.get('text'),
            ),
            md_bg_color=kwargs.get('md_bg_color'),
            pos_hint=kwargs.get('pos_hint'),
        ).open()

    def show_dialog(self, button=None, content=None):
        self.dialog = MDDialog(
            title='Notice!',
            type='custom',
            radius=[dp(20), dp(7), dp(20), dp(7)],
            content_cls=content,
            buttons=[
                button,
                MDFlatButton(
                    text="Close",
                    theme_text_color="Custom",
                    font_style='Button',
                    text_color='white',
                    on_release=self.close_dialog,
                ),
            ],
        )
        self.dialog.children[0].children[3].line_height = 1.5
        self.dialog.children[0].children[3].color = 'white'
        self.dialog.open()

    def close_dialog(self, inst):
        self.dialog.dismiss()


if __name__ == '__main__':
    MainApp().run()