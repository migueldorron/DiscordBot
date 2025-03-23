import gspread
from google.oauth2.service_account import Credentials
import json
import os

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file(json.loads(os.getenv("GOOGLE_CREDENTIALS")), scopes=SCOPES)
sheetName="TCGP_Trading_Sheet"

def connectSheet():
    client = gspread.authorize(creds)
    connectionExcel = client.open(sheetName)
    return connectionExcel
