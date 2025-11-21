from google.oauth2.service_account import Credentials
import pandas as pd
import gspread
import os
import io


# SCOPES = [
#     "https://www.googleapis.com/auth/spreadsheets.readonly",
#     "https://www.googleapis.com/auth/drive.readonly",
# ]

# # 1) Aquí GS_SERVICE_ACCOUNT_CREDS es un STRING con el JSON (no una ruta)
# json_str = os.environ["GS_SERVICE_ACCOUNT_CREDS"]

# # 2) Lo convertimos a dict de Python
# service_account_info = json.loads(json_str)  # <-- ESTO NO ES UNA RUTA

# # 3) Creamos las credenciales a partir de ese dict
# creds = Credentials.from_service_account_info(
#     service_account_info,
#     scopes=SCOPES,
# )

# # Autenticarse con gspread
# CLIENT = gspread.authorize(creds)


def download_from_gs_excel(sheet_url):
    """(igual que antes) descarga TODAS las hojas a un Excel en memoria."""
    sh = CLIENT.open_by_url(sheet_url)
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        for ws in sh.worksheets():
            values = ws.get_all_values()
            header = values[0]
            rows = values[1:]
            df = pd.DataFrame(rows, columns=header)

            sheet_name = (ws.title or "Sheet")[:31]
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    return output.getvalue()


def download_from_gs_single_sheet(sheet_url, sheet_name=None):
    """
    Descarga SOLO una hoja de un Google Sheet y la devuelve como DataFrame.
    Luego `upload_to_gcp` la subirá como CSV.
    """
    sh = CLIENT.open_by_url(sheet_url)
    ws = sh.worksheet(sheet_name) if sheet_name else sh.sheet1

    values = ws.get_all_values()
    if not values: return pd.DataFrame()

    header = values[0]
    rows = values[1:]

    return pd.DataFrame(rows, columns=header)
