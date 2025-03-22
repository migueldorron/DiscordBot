import gspread
from google.oauth2.service_account import Credentials

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file('C:/Users/34648/Desktop/PS/bot/directed-will-448512-t0-48e9d6aadf65.json', scopes=SCOPES)
sheetName="TCGP_Trading_Sheet"

def connectSheet():
    client = gspread.authorize(creds)
    connectionExcel = client.open(sheetName)
    return connectionExcel
