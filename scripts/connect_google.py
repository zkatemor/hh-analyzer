import schedule # problem for python3.8
from clickhouse_driver import Client
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# not tested...
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
client = Client(host='localhost', user='default', password='', port='9000', database='')
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
gc = gspread.authorize(credentials)


def update_sheet():
    print('Updating cell at', datetime.now())
    columns = []
    for item in client.execute('describe table headhunter.vacancies_short'):
        columns.append(item[0])
    vacancies = client.execute('SELECT * FROM headhunter.vacancies_short')
    df_vacancies = pd.DataFrame(vacancies, columns=columns)
    df_vacancies.to_csv('vacancies_short.csv', index=False)
    content = open('vacancies_short.csv', 'r').read()
    gc.import_csv('1ZWS2kqraPa4i72hzp0noU02SrYVo0teD7KZ0c3hl-UI', content.encode('utf-8'))


update_sheet()
schedule.every().day.at("11:11").do(update_sheet)
while True:
    schedule.run_pending()
