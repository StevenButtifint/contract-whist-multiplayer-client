from googleapiclient.discovery import build
from google.oauth2 import service_account


SERVICE_ACCOUNT_FILE = 'keys/default_key.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1Bh1UzXg5d5iBrd8pP-wwsz2lzTHw6uDzSd1U62FYDA0'

credentials = None
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()


# read Google Sheets data through API
def getSheetData():
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="p1!a1:c5").execute()
    values = result.get('values', [])
    return values


# write Google Sheets data through API
def setSheetData(data):
    request = sheet.values().update(spreadsheetId=SPREADSHEET_ID,
                                range="p1!a1", valueInputOption="USER_ENTERED",
                                body={"values":data}).execute()


values = getSheetData()

data = [["new Data"]]

setSheetData(data)


print(values)

