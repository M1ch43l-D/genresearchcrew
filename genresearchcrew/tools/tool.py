import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()

spread_sheets_id = os.getenv('SPREAD_SHEET_ID')
credentials_path = os.getenv('GOOGLE_SHEETS_CREDENTIALS_PATH')

if not spread_sheets_id:
    raise ValueError("SPREAD_SHEET_ID not set in .env file")
if not credentials_path:
    raise ValueError("GOOGLE_SHEETS_CREDENTIALS_PATH not set in .env file")

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

try:
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
    gc = gspread.authorize(credentials)
    sheet = gc.open_by_key(spread_sheets_id).sheet1
except Exception as e:
    raise ValueError(f"Failed to authenticate or open the sheet: {e}")

def log_missing_information(row, col, header, company_name, timestamp):
    print(f"Missing information at Row: {row}, Column: {col}, Column Header: '{header}', Company: '{company_name}', Timestamp: {timestamp}")

def scan_for_missing_info(sheet):
    data = sheet.get_all_values()
    if not data:
        print("No data found in the sheet")
        return

    headers = data[0]
    company_index = headers.index('Company Name') if 'Company Name' in headers else None
    for i, row in enumerate(data[1:], start=2):
        company_name = row[company_index] if company_index is not None else "Unknown"
        for j, cell in enumerate(row, start=1):
            if cell == "":
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                header = headers[j-1] if j <= len(headers) else "Unknown Header"
                log_missing_information(i, j, header, company_name, timestamp)

try:
    scan_for_missing_info(sheet)
    print("Scan complete.")
except Exception as e:
    print(f"An error occurred during the scan: {e}")
