import os
from functools import partial
from kivy.clock import mainthread
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import FallOutTransition, RiseInTransition
from kivymd.uix.filemanager import MDFileManager
from google_sheet import GoogleSheet
from widgets import BaseScreen, MyProgressBar
import multiprocessing as mp
from ocr import Ocr


class MainScreen(BaseScreen):
    path = StringProperty()
    table = ObjectProperty()
    state = StringProperty("stop")

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.manager_open = False
        self.pool = mp.Pool(processes=3)
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
        )
        self.progress_bars = []

    def on_pre_enter(self, *args):
        if self.app.storage:
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
            button.text = 'Stop'
            button.md_bg_color = 'red'

            def _callback(response, spin: bool):
                self.table.add_row(data_image=response)

                if spin:
                    button.text = 'Start'
                    button.md_bg_color = 'green'
                    self.ids.main_spin.active = False

            def _error_callback(response):
                print(response)
                print(response.args)

            ocr = Ocr()

            if os.path.isfile(self.path):
                self.pool.apply_async(func=partial(ocr, path=self.path), callback=partial(_callback, spin=True))
                self.ids.main_spin.active = True
            elif os.path.isdir(self.path):
                file_name_list = [file_name for file_name in os.listdir(path=self.path) if os.path.isfile(os.path.join(self.path, file_name))]

                for i, file_name in enumerate(file_name_list):
                    path = os.path.join(self.path, file_name)
                    spin = False

                    if i == 0:
                        self.ids.main_spin.active = True

                    if i == len(file_name_list) - 1:
                        spin = True

                    self.pool.apply_async(func=partial(ocr, path=path), callback=partial(_callback, spin=spin), error_callback=_error_callback)

        else:
            self.pool.terminate()
            self.pool.close()
            self.pool = mp.Pool(processes=3)
            button.text = 'Start'
            button.md_bg_color = 'green'
            self.ids.main_spin.active = False

    def push(self, button):
        sheet_name = self.app.storage.get('google_sheet_name').get('name')
        if all([self.app.storage.exists('google_sheet'), sheet_name]):
            setattr(self, 'google_sheet', GoogleSheet(key=self.app.storage.get('google_sheet').get('api_key')))

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
                self.ids.main_spin.active = False

                self.app.open_snackbar(
                    text='Pushed successfully',
                    md_bg_color="#17d86e",
                    pos_hint={'top': 1},
                )

                button.disabled = False

            self.pool.apply_async(func=partial(
                self.google_sheet.update,
                name_sheet=sheet_name,
                data_table=self.table.data),
                callback=_callback,
                error_callback=_error_callback,
            )

            self.ids.main_spin.active = True
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
        if self.app.storage:
            if self.app.storage.exists('google_sheet'):
                self.ids.path_google_sheet.text = self.app.storage['google_sheet'].get('api_key')

            if self.app.storage.exists('folder_path'):
                self.ids.folder_path.text = self.app.storage['folder_path'].get('path')

            if self.app.storage.exists('google_sheet_name'):
                self.ids.google_sheet_name.text = self.app.storage['google_sheet_name'].get('name')

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


