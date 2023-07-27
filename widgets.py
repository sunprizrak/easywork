from kivy.clock import Clock
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.textfield import MDTextField


class BaseScreen(MDScreen):
    def __init__(self, **kwargs):
        super(BaseScreen, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.md_bg_color = self.theme_cls.bg_light


class MDData(MDScreen):

    def __init__(self, **kwargs):
        super(MDData, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.data = {}
        self.data_tables = MDDataTable(
            background_color_header="#65275d",
            background_color_cell="#451938",
            background_color_selected_cell="#e4514f",
            use_pagination=True,
            check=True,
            column_data=[
                ("№", dp(20)),
                ("Username", dp(30)),
                ("ID", dp(30)),
                ("Club", dp(30)),
                ("VPIP", dp(20)),
                ("PFR", dp(20)),
                ("3-Bet", dp(20)),
                ("C-Bet", dp(20)),
                ("Hands", dp(20)),
                ("Date", dp(20)),
            ],
            row_data=[],
            rows_num=20,
            sorted_on="Schedule",
            sorted_order="ASC",
        )
        self.data_tables.bind(on_row_press=self.on_row_press)
        self.data_tables.bind(on_check_press=self.on_check_press)
        self.add_widget(self.data_tables)

    def add_row(self, data: dict) -> None:
        for key, val in data.items():
            last_num_row = self.count_row
            try:
                if self.data.get(key):
                    if float(self.data[key][-2].replace(',', '.')) <= float(val[-2].replace(',', '.')):
                        self.data[key] = val
                        for el in self.data_tables.row_data:
                            if key in el:
                                self.data_tables.update_row(
                                    el,
                                    [el[0], *val[1:]]
                                )
                                break
                else:
                    self.data[key] = val
                    self.data_tables.add_row([str(last_num_row + 1), *val[1:]])
            except Exception as error:
                print(error)

    @property
    def count_row(self):
        return len(self.data_tables.row_data)

    def on_row_press(self, instance_table, instance_row):
        '''Called when a table row is clicked.'''

        if self.data.get(instance_row.text):
            key_id = instance_row.text
            self.app.root.ids.main_screen.ids.screenshot.source = self.data[key_id][0]

            name_columns = [el[0] for el in self.data_tables.column_data[1:-1]]
            data = list(zip(name_columns, self.data[instance_row.text][1:-1]))

            screen = self.app.root.ids.main_screen

            def _clear_widgets():
                if all([screen.ids.fields_box.children, screen.ids.buttons_box.children]):
                    screen.ids.fields_box.clear_widgets(children=None)
                    screen.ids.buttons_box.clear_widgets(children=None)

                self.app.root.ids.main_screen.ids.screenshot.source = 'assets/img/chost_image.png'

            close_button = MDIconButton(
                icon='close',
                icon_color='white',
                pos_hint={'x': .965, 'y': .95},
                on_release=lambda x: _clear_widgets(),
            )

            screen.ids.main_layout.add_widget(close_button)

            def _add_edit_tools():
                for el in data:

                    field = MDTextField(
                        mode="rectangle",
                        hint_text=el[0],
                        text=el[1],
                        readonly=True,
                    )

                    screen.ids.fields_box.add_widget(field)

                def _switch_on():
                    for widget in screen.ids.buttons_box.children:
                        if isinstance(widget, MDRaisedButton):
                            widget.disabled = False

                    setattr(self, 'data_edit', {})

                    for widget in screen.ids.fields_box.children:
                        widget.readonly = False
                        self.data_edit[widget.hint_text] = widget.text

                def _switch_off():
                    for widget in screen.ids.buttons_box.children:
                        if isinstance(widget, MDRaisedButton):
                            widget.disabled = True

                    if self.__dict__.get('data_edit'):

                        for widget in screen.ids.fields_box.children:
                            widget.text = self.data_edit.get(widget.hint_text)
                            widget.readonly = True

                        delattr(self, 'data_edit')

                class SwitchUpdate(MDSwitch):
                    def __init__(self, **kwargs):
                        super(SwitchUpdate, self).__init__(**kwargs)
                        self.icon_active = 'check'
                        self.icon_inactive_color = 'grey'

                    def on_active(self, instance_switch, active_value: bool) -> None:
                        super(SwitchUpdate, self).on_active(instance_switch, active_value)
                        if active_value:
                            _switch_on()
                        else:
                            _switch_off()

                switch = SwitchUpdate()

                button_update = MDRaisedButton(
                    text='Update row',
                    md_bg_color='blue',
                    disabled=True,
                )

                screen.ids.buttons_box.add_widget(switch)
                screen.ids.buttons_box.add_widget(button_update)

            if all([screen.ids.fields_box.children, screen.ids.buttons_box.children]):
                for el in data:
                    for widget in screen.ids.fields_box.children:
                        if widget.hint_text == el[0]:
                            widget.text = el[1]
            else:
                _add_edit_tools()

    def on_check_press(self, instance_table, current_row):
        '''Called when the check box in the table row is checked.'''
        return current_row

    def sort_on_signal(self, data):
        return zip(*sorted(enumerate(data), key=lambda l: l[1][2]))

    def sort_on_schedule(self, data):
        return zip(
            *sorted(
                enumerate(data),
                key=lambda l: sum(
                    [
                        int(l[1][-2].split(":")[0]) * 60,
                        int(l[1][-2].split(":")[1]),
                    ]
                ),
            )
        )

    def sort_on_team(self, data):
        return zip(*sorted(enumerate(data), key=lambda l: l[1][-1]))