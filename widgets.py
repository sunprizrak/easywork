from kivy.clock import mainthread
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.screen import MDScreen


class BaseScreen(MDScreen):
    def __init__(self, **kwargs):
        super(BaseScreen, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()
        #self.md_bg_color = self.theme_cls.bg_light


class MDData(BaseScreen):

    def __init__(self, **kwargs):
        super(MDData, self).__init__(**kwargs)
        self.data_tables = MDDataTable(
            use_pagination=True,
            check=True,
            column_data=[
                ("№", dp(30)),
                ("Username", dp(60), self.sort_on_signal),
                ("ID", dp(30)),
                ("Club", dp(30)),
                ("VPIP", dp(30), self.sort_on_schedule),
                ("PFR", dp(30), self.sort_on_team),
                ("3-Bet", dp(30)),
                ("C-Bet", dp(30)),
                ("Hands", dp(30)),
                ("Date", dp(30)),
            ],
            row_data=[
                # (
                #     "1",
                #     ("alert", [255 / 256, 165 / 256, 0, 1], "No Signal"),
                #     "Astrid: NE shared managed",
                #     "Medium",
                #     "Triaged",
                #     "0:33",
                #     "Chase Nguyen",
                # ),
                # (
                #     "2",
                #     ("alert-circle", [1, 0, 0, 1], "Offline"),
                #     "Cosmo: prod shared ares",
                #     "Huge",
                #     "Triaged",
                #     "0:39",
                #     "Brie Furman",
                # ),
                # (
                #     "3",
                #     (
                #         "checkbox-marked-circle",
                #         [39 / 256, 174 / 256, 96 / 256, 1],
                #         "Online",
                #     ),
                #     "Phoenix: prod shared lyra-lists",
                #     "Minor",
                #     "Not Triaged",
                #     "3:12",
                #     "Jeremy lake",
                # ),
                # (
                #     "4",
                #     (
                #         "checkbox-marked-circle",
                #         [39 / 256, 174 / 256, 96 / 256, 1],
                #         "Online",
                #     ),
                #     "Sirius: NW prod shared locations",
                #     "Negligible",
                #     "Triaged",
                #     "13:18",
                #     "Angelica Howards",
                # ),
                # (
                #     "5",
                #     (
                #         "checkbox-marked-circle",
                #         [39 / 256, 174 / 256, 96 / 256, 1],
                #         "Online",
                #     ),
                #     "Sirius: prod independent account",
                #     "Negligible",
                #     "Triaged",
                #     "22:06",
                #     "Diane Okuma",
                # ),
            ],
            sorted_on="Schedule",
            sorted_order="ASC",
            elevation=2,
        )
        self.data_tables.bind(on_row_press=self.on_row_press)
        self.data_tables.bind(on_check_press=self.on_check_press)
        self.add_widget(self.data_tables)

    @mainthread
    def add_row(self, data) -> None:
        last_num_row = self.count_row
        self.data_tables.add_row([str(last_num_row + 1), *data])

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