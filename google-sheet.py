import pandas as pd
import seaborn as sns
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe

GOOGLE_OAUTH2_CONFIG_PATH = './.config/google_oauth2.json'
SHEET_KEY = '1T0o8tSV4VBsCTMlmGNaQXCWAus4-a_N9KOdQ8apIHBg'
SCOPE = [
'https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive',
]

def connect_to_goods_oauth2():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_OAUTH2_CONFIG_PATH, SCOPE)
    gc = gspread.authorize(credentials)

    return gc.open_by_key(SHEET_KEY)

def select_tab_by_tab_name(tab_name):
    sh = connect_to_goods_oauth2()
    worksheet = sh.worksheet(tab_name)

    return worksheet

def get_data_from_sheet(tab_name):
    worksheet = select_tab_by_tab_name(tab_name)
    df = pd.DataFrame(data = worksheet.get_all_records())

    return df
def add_data_to_sheet(tab_name,data):
    worksheet = select_tab_by_tab_name(tab_name)
    set_with_dataframe(worksheet, data)
    return get_data_from_sheet(tab_name)

def load_titanic_data():
    return sns.load_dataset('titanic')

if __name__ == '__main__':
    print(add_data_to_sheet('시트1',load_titanic_data()))