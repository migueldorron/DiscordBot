import gspread
from google.oauth2.service_account import Credentials

# Cargar las credenciales del archivo JSON
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file('C:/Users/34648/Desktop/PS/bot/directed-will-448512-t0-48e9d6aadf65.json', scopes=SCOPES)
sheetName="Sheet_ET"

def connectSheet():
    # Autenticación con gspread
    client = gspread.authorize(creds)

    # Abrir la hoja de cálculo por su nombre
    connectionExcel = client.open(sheetName)
    return connectionExcel
