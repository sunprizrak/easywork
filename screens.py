import os

from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import FallOutTransition, RiseInTransition
from kivymd.uix.filemanager import MDFileManager

from utility.ocr import Ocr
from widgets import BaseScreen
import multiprocessing as mp


def test_start():
    # for test, after delete this list
    response = [['0(.3)', '8727206', 'AK47.', '48', '26', '10', '54', '4,922', '23/07/2023'],
                ['pp8864723', '8864723', 'Bertholletia', '47', '27', '5', '30', '4,292', '23/07/2023'],
                ['Conflux', '8966174', 'K14.0', '40', '14', '2', '37', '3,466', '23/07/2023'],
                ['m@rmel@dk@', '9075270', 'FreedomBlast', '47', '27', '21', '31', '2,928', '23/07/2023'],
                ['pomey', '8668791', 'BITCOIN', '38', '18', '5', '46', '2,531', '23/07/2023'],
                ['m@rmel@dk@', '9075270', 'FreedomBlast', '47', '27', '21', '31', '2,928', '23/07/2023'],
                ['%Quee~fore', '8739697', 'DirtyCarnival', '45', '23', '6', '31', '3,257', '23/07/2023'],
                ['Naatu Naatu', '8514819', 'Gulliver', '43', '21', '7', '46', '8,028', '23/07/2023'],
                ['MonPlatin', '9068808', 'The Thor', '44', '21', '3', '40', '1,547', '23/07/2023'],
                ['Uroda', '8864104', 'FreedomBlast', '51', '29', '20', '60', '1,650', '23/07/2023'], ]
    return response


class MainScreen(BaseScreen):

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.table = ObjectProperty()
        self.ocr = Ocr()

    def open_settings(self):
        self.app.root.transition = FallOutTransition()
        self.app.root.transition.direction = 'left'
        self.app.root.current = 'settings_screen'

    def start(self, button):
        if button.text.lower() == 'start':
            def _callback(response):
                button.text = 'Start'
                button.md_bg_color = 'green'
                self.table.add_row(data=response)

            button.text = 'Stop'
            button.md_bg_color = 'red'
            setattr(self, 'pool', mp.Pool())
            # for test, after delete func test_start

            self.pool.apply_async(func=test_start, callback=_callback)
            self.pool.close()
        else:
            self.pool.terminate()
            button.text = 'Start'
            button.md_bg_color = 'green'


class SettingsScreen(BaseScreen):

    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
        )

    def on_pre_enter(self, *args):
        if self.app.storage.exists('google_sheet'):
            self.ids.path_google_sheet.text = self.app.storage.get('google_sheet').get('api_key')

    def file_manager_open(self):
        self.file_manager.show(os.path.expanduser("~"))
        self.manager_open = True
        self.file_manager.ext.extend(['.json'])

    def select_path(self, path: str):
        self.ids.path_google_sheet.text = path
        self.exit_manager()

    def exit_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()

    def open_main_screen(self):
        self.app.root.transition = RiseInTransition()
        self.app.root.current = 'main_screen'

    def save(self):
        path_key = self.ids.path_google_sheet.text
        self.app.storage.put('google_sheet', api_key=path_key)




