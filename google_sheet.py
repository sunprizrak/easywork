import re
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread.utils import rowcol_to_a1


class GoogleSheet:

    def __init__(self, key):
        self.key = key
        self.sheet = None

    def auth(self):
        scope = ['https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.key, scope)
        setattr(self, 'client', gspread.authorize(credentials))

    def open(self, name_sheet: str):
        if getattr(self, 'client'):
            self.sheet = getattr(self, 'client').open(name_sheet)

    def update(self, name_sheet: str, data_table: dict):
        self.auth()

        try:
            self.open(name_sheet=name_sheet)
        except gspread.exceptions.SpreadsheetNotFound:
            error = dict(error='check the correctness of the entered name')
            assert False, error

        all_worksheets = self.sheet.worksheets()

        for worksheet in all_worksheets:
            data = worksheet.get_all_values()
            print(f'worksheet: {worksheet}')

            patterns = ['vpipovrll', 'pfrovrll', '3\D*betovrll', 'c\D*betovrll', 'handsovrll', 'dateovrll']

            columns = [max(walrus) for pattern in patterns if (walrus := [i for i, el in enumerate(data[0], 1) if re.fullmatch(pattern, el.lower().replace(' ', ''))])]

            if len(columns) == len(patterns):

                for key, val in data_table.items():
                    rows_number = [cell.row for cell in worksheet.findall(key)]

                    for row in rows_number:
                        hands_value = worksheet.cell(row, columns[-2]).value

                        if type(hands_value) is str:
                            if hands_value.replace(',', '').isdigit() and int(val[-2]) < int(hands_value.replace(',', '')):
                                continue

                        column_range = f'{rowcol_to_a1(row, columns[0])}:{rowcol_to_a1(row, columns[-1])}'
                        cell_list = worksheet.range(column_range)

                        for i, cell in enumerate(cell_list):
                            cell.value = int(val[4:][i]) if '/' not in val[4:][i] else val[4:][i]

                        worksheet.update_cells(cell_list)
                        print(f'update: {worksheet}')
            time.sleep(3)


if __name__ == '__main__':
    gs = GoogleSheet(key='gs_credentials.json')
    gs.auth()
    gs.open('Vladimir_Ocr')

