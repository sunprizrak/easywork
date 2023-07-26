import os
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import FallOutTransition, RiseInTransition
from kivymd.uix.filemanager import MDFileManager
from utility.ocr import Ocr
from widgets import BaseScreen
import multiprocessing as mp


def test_start():
    # for test, after delete this list
    response = {'8727206': ['/home/sunprizrak/Изображения/vladimir/fdsfgsdf.png', '0(.3)', '8727206', 'AK47.', '48', '26', '10', '54', '4,922', '26/07/2023'], '8835971': ['/home/sunprizrak/Изображения/vladimir/image.png', '"J7"', '8835971', '#HOUSEOFCARDS', '41', '21', '7', '52', '3,357', '26/07/2023'], '8864723': ['/home/sunprizrak/Изображения/vladimir/Без имени.png', 'pp8864723', '8864723', 'Bertholletia', '47', '27', '5', '30', '4,292', '26/07/2023'], '8966174': ['/home/sunprizrak/Изображения/vladimir/betwin.png', 'Conflux', '8966174', 'K14.0', '40', '14', '2', '37', '3,466', '26/07/2023'], '9075270': ['/home/sunprizrak/Изображения/vladimir/photo_2023-07-17_23-45-03.jpg', 'm@rmel@dk@', '9075270', 'FreedomBlast', '47', '27', '21', '31', '2,928', '26/07/2023'], '8668791': ['/home/sunprizrak/Изображения/vladimir/asdfsadfqwe.png', 'pomey', '8668791', 'BITCOIN', '38', '18', '5', '46', '2,531', '26/07/2023'], '8739697': ['/home/sunprizrak/Изображения/vladimir/sdfasdf.png', '%Quee~fore', '8739697', 'DirtyCarnival', '45', '23', '6', '31', '3,257', '26/07/2023'], '8514819': ['/home/sunprizrak/Изображения/vladimir/photo_2023-07-14_20-10-09.jpg', 'Naatu Naatu', '8514819', 'Gulliver', '43', '21', '7', '46', '8,028', '26/07/2023'], '9068808': ['/home/sunprizrak/Изображения/vladimir/photo_2023-07-16_19-45-25.jpg', 'MonPlatin', '9068808', 'The Thor', '44', '21', '3', '40', '1,547', '26/07/2023'], '8864104': ['/home/sunprizrak/Изображения/vladimir/asasdfasdf.png', 'Uroda', '8864104', 'FreedomBlast', '51', '29', '20', '60', '1,650', '26/07/2023']}

    return response


class MainScreen(BaseScreen):

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.table = ObjectProperty()
        self.ocr = Ocr()
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
        )

    def file_manager_open(self):
        self.file_manager.show(os.path.expanduser("~"))
        self.manager_open = True

    def select_path(self, path: str):
        if os.path.isfile(path):
            file_name = path.split('/')[-1]
            self.table.add_row([[file_name]])
        elif os.path.isdir(path):
            print('dir')

        self.exit_manager()

    def exit_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()

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

            try:
                self.pool.apply_async(func=self.ocr, callback=_callback)
            except Exception as error:
                print(error)
            finally:
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




