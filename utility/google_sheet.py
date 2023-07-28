import gspread
from oauth2client.service_account import ServiceAccountCredentials
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
        self.sheet = self.client.open(name_sheet).sheet1

    def read_csv(self, name_csv: str):
        self.df = pd.read_csv(name_csv)

    def update(self):
        self.sheet.update([self.df.colums.values.tolist()]) + self.df.values.tolist()


if __name__ == '__main__':
    gs = GoogleSheet()
    gs.open()





