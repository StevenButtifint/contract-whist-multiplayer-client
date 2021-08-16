from googleapiclient.discovery import build
from google.oauth2 import service_account


SERVICE_ACCOUNT_FILE = 'keys/default_key.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1Bh1UzXg5d5iBrd8pP-wwsz2lzTHw6uDzSd1U62FYDA0'

credentials = None
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()


