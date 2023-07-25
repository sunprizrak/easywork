from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.screen import MDScreen


class BaseScreen(MDScreen):
    def __init__(self, **kwargs):
        super(BaseScreen, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.md_bg_color = self.theme_cls.bg_light


class MDData(MDScreen):

    def __init__(self, **kwargs):
        super(MDData, self).__init__(**kwargs)
        self.data_tables = MDDataTable(
            background_color_header="#65275d",
            background_color_cell="#451938",
            background_color_selected_cell="e4514f",
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

    def add_row(self, data) -> None:
        try:
            for el in data:
                last_num_row = self.count_row
                self.data_tables.add_row([str(last_num_row + 1), *el])
        except Exception as error:
            print(error)

    @property
    def count_row(self):
        return len(self.data_tables.row_data)

    def on_row_press(self, instance_table, instance_row):
        '''Called when a table row is clicked.'''

        print(instance_table, instance_row)

    def on_check_press(self, instance_table, current_row):
        '''Called when the check box in the table row is checked.'''

        print(instance_table, current_row)

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