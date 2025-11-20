from google.oauth2.service_account import Credentials
import pandas as pd
import gspread
import os


# CREDS_JSON = os.getenv("GS_SERVICE_ACCOUNT_CREDS")
CREDS_JSON = "creds.json"


def download_from_gs(sheet_url, sheet_names=None):

    # Crear credenciales
    creds = Credentials.from_service_account_file(
        CREDS_JSON,
        scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
    )

    # Autenticarse con gspread
    client = gspread.authorize(creds)

    # Abrir la hoja por URL o por nombre
    spreadsheet = client.open_by_url(sheet_url)

    if sheet_names: 
        sheet_1 = spreadsheet.worksheet(sheet_names[0])
        sheet_2 = spreadsheet.worksheet(sheet_names[1])
        values_1 = sheet_1.get_all_values()
        values_2 = sheet_2.get_all_values()
        df_1 = pd.DataFrame(values_1[1:], columns=values_1[0])
        df_2 = pd.DataFrame(values_2[1:], columns=values_2[0])
        return df_1, df_2
    
    else:          
        sheet = spreadsheet.get_worksheet(0)  # Abrir la primera hoja
        values = sheet.get_all_values()
        # trimmed = [row[:3] for row in values]
        df = pd.DataFrame(values[1:], columns=values[0])
        return df
