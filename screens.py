import os
from functools import partial
from kivy.clock import Clock, mainthread
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import FallOutTransition, RiseInTransition
from kivymd.uix.filemanager import MDFileManager
from utility.ocr import Ocr
from utility.google_sheet import GoogleSheet
from widgets import BaseScreen, MyProgressBar
import multiprocessing as mp


# for test table
def test_start(path: str):
    # for test, after delete this list
    response = {'8727206': ['/home/sunprizrak/Изображения/vladimir/fdsfgsdf.png', '0(.3)', '8727206', 'AK47.', '48', '26', '10', '54', '4,922', '26/07/2023'], '8835971': ['/home/sunprizrak/Изображения/vladimir/image.png', '"J7"', '8835971', '#HOUSEOFCARDS', '41', '21', '7', '52', '3,357', '26/07/2023'], '8864723': ['/home/sunprizrak/Изображения/vladimir/Без имени.png', 'pp8864723', '8864723', 'Bertholletia', '47', '27', '5', '30', '4,292', '26/07/2023'], '8966174': ['/home/sunprizrak/Изображения/vladimir/betwin.png', 'Conflux', '8966174', 'K14.0', '40', '14', '2', '37', '3,466', '26/07/2023'], '9075270': ['/home/sunprizrak/Изображения/vladimir/photo_2023-07-17_23-45-03.jpg', 'm@rmel@dk@', '9075270', 'FreedomBlast', '47', '27', '21', '31', '2,928', '26/07/2023'], '8668791': ['/home/sunprizrak/Изображения/vladimir/asdfsadfqwe.png', 'pomey', '8668791', 'BITCOIN', '38', '18', '5', '46', '2,531', '26/07/2023'], '8739697': ['/home/sunprizrak/Изображения/vladimir/sdfasdf.png', '%Quee~fore', '8739697', 'DirtyCarnival', '45', '23', '6', '31', '3,257', '26/07/2023'], '8514819': ['/home/sunprizrak/Изображения/vladimir/photo_2023-07-14_20-10-09.jpg', 'Naatu Naatu', '8514819', 'Gulliver', '43', '21', '7', '46', '8,028', '26/07/2023'], '9068808': ['/home/sunprizrak/Изображения/vladimir/photo_2023-07-16_19-45-25.jpg', 'MonPlatin', '9068808', 'The Thor', '44', '21', '3', '40', '1,547', '26/07/2023'], '8864104': ['/home/sunprizrak/Изображения/vladimir/asasdfasdf.png', 'Uroda', '8864104', 'FreedomBlast', '51', '29', '20', '60', '1,650', '26/07/2023']}

    return response


class MainScreen(BaseScreen):
    path = StringProperty()
    table = ObjectProperty()
    state = StringProperty("stop")

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.ocr = Ocr()
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
        )
        self.progress_bars = []

    def on_pre_enter(self, *args):
        self.path = self.app.storage.get('folder_path').get('path')

    def on_state(self, instance, value):
        def _start():
            for progress_bar in self.progress_bars:
                progress_bar.start()

        def _stop():
            for progress_bar in self.progress_bars:
                progress_bar.stop()

        {
            "start": _start,
            "stop": _stop,
        }.get(value)()

    def press_progress(self):
        if self.state == 'stop':
            self.state = 'start'
        else:
            self.state = 'stop'
            for el in self.progress_bars:
                self.ids.main_layout.remove_widget(el)
            self.progress_bars.clear()

    def file_manager_open(self):
        self.file_manager.show(os.path.expanduser("~"))
        self.manager_open = True

    def select_path(self, path: str):
        self.path = path
        if os.path.isdir(self.path):
            self.app.storage.put('folder_path', path=self.path)
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
                self.ids.main_spin.active = False

                if len(response) > 1:
                    setattr(self, 'count', 0)
                    res = [{el[0]: el[1]} for el in response.items()]

                    def __callback(dt):
                        if self.count == len(res):
                            delattr(self, 'count')
                            self.event.cancel()
                            delattr(self, 'event')
                        else:
                            self.table.add_row(data=res[self.count])
                            self.count += 1

                    setattr(self, 'event', Clock.schedule_interval(
                        callback=__callback,
                        timeout=0.5,
                    ))
                    self.event()
                else:
                    self.table.add_row(data=response)

            button.text = 'Stop'
            button.md_bg_color = 'red'
            setattr(self, 'pool', mp.Pool())

            try:
                self.pool.apply_async(func=partial(self.ocr, path=self.path), callback=_callback)
                self.ids.main_spin.active = True
            except Exception as error:
                print(error)
            finally:
                self.pool.close()
        else:
            self.pool.terminate()
            button.text = 'Start'
            button.md_bg_color = 'green'
            self.ids.main_spin.active = False

    def push(self, button):
        sheet_name = self.app.storage.get('google_sheet_name').get('name')
        if all([self.app.storage.exists('google_sheet'), sheet_name]):
            setattr(self, 'google_sheet', GoogleSheet(key=self.app.storage.get('google_sheet').get('api_key')))
            setattr(self, 'pool', mp.Pool())

            @mainthread
            def _error_callback(response):
                self.press_progress()
                print(response)
                print(response.args)

                if type(response.args[0]) is dict:
                    error_text = response.args[0].get("error")
                    self.app.open_snackbar(
                        text=error_text,
                        md_bg_color="red",
                        pos_hint={'top': 1},
                    )

                button.disabled = False

            @mainthread
            def _callback(response):
                self.press_progress()

                self.app.open_snackbar(
                    text='Pushed successfully',
                    md_bg_color="#17d86e",
                    pos_hint={'top': 1},
                )

                button.disabled = False

            try:
                self.pool.apply_async(func=partial(
                    self.google_sheet.update,
                    name_sheet=sheet_name,
                    data_table=self.table.data),
                    callback=_callback,
                    error_callback=_error_callback,
                )
            except Exception as error:
                print(error)
            finally:
                self.pool.close()

            button.disabled = True

            for key, val in {'left': 'vertical', 'top': 'horizontal', 'right': 'vertical', 'bottom': 'horizontal'}.items():

                progress_bar = MyProgressBar(
                    type='determinate',
                    back_color=self.md_bg_color,
                    orientation=val,
                    running_duration=1,
                    catching_duration=1.5,
                    pos_hint={key: 1},
                    size_hint_y=0.005 if val == 'horizontal' else 1,
                    size_hint_x=0.002 if val == 'vertical' else 1,
                    edge=key,
                )

                self.progress_bars.append(progress_bar)
                self.ids.main_layout.add_widget(progress_bar)

            self.press_progress()
        else:
            self.open_settings()

    def delete_img(self):
        for data in self.table.data_tables.get_row_checks():
            os.remove(path=self.table.data.get(data[2])[0])

        self.table.delete_checked_rows()


class SettingsScreen(BaseScreen):

    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
        )

    def on_pre_enter(self, *args):
        self.ids.path_google_sheet.text = self.app.storage.get('google_sheet').get('api_key')
        self.ids.folder_path.text = self.app.storage.get('folder_path').get('path')
        self.ids.google_sheet_name.text = self.app.storage.get('google_sheet_name').get('name')

    def file_manager_open(self, instance):
        setattr(self, 'cur_field', instance)
        self.file_manager.show(os.path.expanduser("~"))
        self.manager_open = True
        self.file_manager.ext.extend(['.json'])

    def select_path(self, path: str):
        self.cur_field.text = path
        delattr(self, 'cur_field')
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
        folder_path = self.ids.folder_path.text
        self.app.storage.put('folder_path', path=folder_path)
        sheet_name = self.ids.google_sheet_name.text
        self.app.storage.put('google_sheet_name', name=sheet_name)

        self.app.open_snackbar(
            text='save successfully',
            md_bg_color="#17d86e",
            pos_hint={'center_x': .5, 'top': 1},
        )






