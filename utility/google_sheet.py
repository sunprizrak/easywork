import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread.utils import rowcol_to_a1


class GoogleSheet:

    def __init__(self, key):
        scope = ['https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive"]

        credentials = ServiceAccountCredentials.from_json_keyfile_name(key, scope)
        self.client = gspread.authorize(credentials)
        self.sheet = None

    def open(self, name_sheet: str):
        self.sheet = self.client.open(name_sheet)

    def update(self, name_sheet: str, error_callback, success_callback):
        try:
            self.open(name_sheet=name_sheet)
        except gspread.exceptions.SpreadsheetNotFound:
            error_text = 'check the correctness of the entered name'
            return error_callback(error=error_text)



        return success_callback()



if __name__ == '__main__':
    gs = GoogleSheet(key='gs_credentials.json')
    gs.open('Vladimir_Ocr')

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



