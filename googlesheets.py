from pprint import pprint
# for google-api
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
# my
import re
import time
import pickle
from Messages import Messages


# Файл, полученный в Google Developer Console
CREDENTIALS_FILE = 'creds.json'
# ID Google Sheets документа (можно взять из его URL)
spreadsheet_id = '1Hl2pCOYJjQNXaOkePnzxE-PI7L31FVTajClZasrYNDc'

# Авторизуемся и получаем service — экземпляр доступа к API
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)


class Spreadsheet:
    def __init__(self):
        self.valueNew = {}
        self.valueRanges = []
        self.requests = []
        self.service = service

    def prepare_setValues(self, cellsRange, values, majorDimension = "ROWS"):
        self.valueRanges.append({"range": cellsRange, "majorDimension": majorDimension, "values": values})

    def prepare_NewValues(self, values):
        self.valueNew["values"] = values

    def load_data(self, sheet='crypto'):
        result = service.spreadsheets().values().get(
                        spreadsheetId=spreadsheet_id,
                        range=sheet+'!A1:F100',
                        majorDimension='ROWS').execute()
        return result

    def runPrepared(self, sheet='crypto', valueInputOption = "USER_ENTERED"):
        upd1Res = {'replies': []}
        upd2Res = {'responses': []}
        try:
            if len(self.requests) > 0:
                upd1Res = self.service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id,
                                                                  body={"requests": self.requests}).execute()
            if len(self.valueRanges) > 0:
                upd2Res = self.service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id,
                                                                           body={"valueInputOption": valueInputOption,
                                                                                 "data": self.valueRanges}).execute()
            if len(self.valueNew) > 0:
                upd3Res = self.service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=sheet+'!A1', 
                                                                      valueInputOption=valueInputOption,
                                                                      insertDataOption='INSERT_ROWS',
                                                                      body=self.valueNew).execute()
        finally:
            self.requests = []
            self.valueRanges = []
        return (upd1Res['replies'], upd2Res['responses'], upd3Res['updates'])


class CryptoMember:
    def save_new_crypto_result(user_id):
        with open('{}.data'.format(user_id), 'rb') as f:
            values = pickle.load(f)
        if values:
            ss = Spreadsheet()
            ss.prepare_NewValues(values)
            ss.runPrepared()


    def searh_of_crypto(user_id):
        result = []
        text = ''

        ss = Spreadsheet()
        searh_result = ss.load_data()

        for i in searh_result['values']:
            if str(user_id) in i:
                result.append(i)

        if result:
            for i in result[:10]:
                text = text + Messages['history'].format(date=i[0], crypto_value=i[2],
                                                         crypto_name=i[1], crypto_result=i[4])
        else:
            text = 'У вас нет истории запросов'

        return text

class Jarvismember:
    def __init__(self):
        self.sheet = 'jarvis'
        self.ss = Spreadsheet()

    def save_new_jarvis_remember(self, chat_id, date, text, user_name):
        values = [[chat_id, date, text, user_name]]

        for_check = re.findall(r'\d\d', date)
        date = [int(i) for i in for_check]
        try:
            if date:
                self.ss.prepare_NewValues(values)
                self.ss.runPrepared(sheet=self.sheet)
                return True
        except:
            return False

    def load_all(self):
        # загружает все данные из таблицы для напоминаний
        result = self.ss.load_data(self.sheet)
        return result

    def new_user(self, message):
        user_id = message.from_user.id

        # чтобы принимать callback кнопки и сообщения
        try:
            # Если да, то это callback
            chat_id = message.message.chat.id
        except:
            # Если да, то это  сообщение
            chat_id = message.chat.id

        user_name = message.from_user.first_name
        result = self.ss.load_data(sheet='users')
        users = []
        for i in result['values']:
            users.append(i[2])
        if str(chat_id) not in users:
            values = [[user_id, user_name, chat_id]]
            self.ss.prepare_NewValues(values)
            self.ss.runPrepared(sheet='users')

    def load_users(self):
        result = self.ss.load_data(sheet='users')
        return result

class Budget:
    def __init__(self, sheet='budget'):
        self.sheet = sheet
        self.ss = Spreadsheet()

    def add(self, category, name, summa, user_id):
        categorys = {'entertainment': 'Развлечения', 'need': 'Незапланированные'}
        times = str(time.strftime("%d.%m.%y", time.localtime()))
        values = [[categorys[category], name, summa, user_id, times]]

        try:
            self.ss.prepare_NewValues(values)
            self.ss.runPrepared(sheet=self.sheet)
            return True
        except:
            return False

    def load_all(self):
        # загружает все данные из таблицы Бюджета
        result = self.ss.load_data(self.sheet)
        return result
