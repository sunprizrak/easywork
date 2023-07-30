import re
import string

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread.utils import rowcol_to_a1
import pandas as pd

# Connect to google sheets
scope = ['https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name('gs_credentials.json', scope)


class GoogleSheet:

    def __init__(self):
        self.client = gspread.authorize(credentials)
        self.sheet = None
        self.df = None

    def create(self, name_sheet: str):
        self.sheet = self.client.create(name_sheet)

    def share(self, email: str):
        self.sheet.share(email, perm_type='user', role='writer')

    def open(self, name_sheet: str):
        self.sheet = self.client.open(name_sheet)

    def read_csv(self, name_csv: str):
        self.df = pd.read_csv(name_csv)

    def update(self):
        self.sheet.update([self.df.colums.values.tolist()]) + self.df.values.tolist()


if __name__ == '__main__':
    gs = GoogleSheet()
    gs.open('Vladimir_Ocr')
    # data = gs.sheet.get_all_values()
    # headers = data.pop(0)
    #
    # df = pd.DataFrame(data, columns=headers)
    # pd.set_option('display.max_rows', None)
    # pd.set_option('display.max_columns', None)
    # print(df)


    def get_address(index):
        alfabet = string.ascii_uppercase
        alf_num = {len(alfabet) * i: letter for i, letter in enumerate(alfabet, 1)}

        if one_letter := max([el for el in alf_num.keys() if index > el], default=0):
            if two_letter := index % len(alfabet):
                return alf_num[one_letter] + alfabet[two_letter - 1]
            else:
                return alf_num[one_letter] + alfabet[len(alfabet) - 1]
        else:
            return alfabet[index - 1]

    ''' get all lists '''
    all_worksheets = gs.sheet.worksheets()

    worksheet = all_worksheets[-2]
    data = worksheet.get_all_values()

    patterns = ['vpip', 'pfr', '3\D*bet', 'c\D*bet', 'hands', 'date']
    columns = [max(i for i, el in enumerate(data[0], 1) if re.search(pattern, el.lower())) for pattern in patterns]

    rows_number = [cell.row for cell in worksheet.findall('8966173')]

    columns_range = [f'{rowcol_to_a1(row, columns[0])}:{rowcol_to_a1(row, columns[-1])}' for row in rows_number]

    for el in columns_range:
        cell_list = worksheet.range(el)

        for cell in cell_list:
            cell.value = '1'

        worksheet.update_cells(cell_list)



