import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

class GoogleSheetTool:
    def __init__(self):
        load_dotenv()
        
        self.spread_sheets_id = os.getenv('SPREAD_SHEET_ID')
        self.credentials_path = os.getenv('GOOGLE_SHEETS_CREDENTIALS_PATH')

        if not self.spread_sheets_id:
            raise ValueError("SPREAD_SHEET_ID not set in .env file")
        if not self.credentials_path:
            raise ValueError("GOOGLE_SHEETS_CREDENTIALS_PATH not set in .env file")

        self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(self.credentials_path, self.scope)
        self.gc = gspread.authorize(self.credentials)
        self.sheet = self.gc.open_by_key(self.spread_sheets_id).sheet1

    def read_data(self):
        """Read data from the Google Sheet and return as a list of dictionaries."""
        try:
            data = self.sheet.get_all_records()
            print("Data read successfully from Google Sheet.")
            return data
        except Exception as e:
            raise ValueError(f"Failed to read data from the sheet: {e}")

    def write_data(self, data):
        """Write data to the Google Sheet, clearing existing content."""
        try:
            if data:
                rows = [list(data[0].keys())]  # Header
                for row in data:
                    rows.append(list(row.values()))

                self.sheet.insert_rows(rows, 1)
                print("Data written successfully to Google Sheet.")
            else:
                print("No data to write.")
        except Exception as e:
            raise ValueError(f"Failed to write data to the sheet: {e}")

# Example usage with a research agent
if __name__ == "__main__":
    # Initialize GoogleSheetTool
    google_sheet_tool = GoogleSheetTool()

    # Example data retrieved by a research agent
    research_data = [
        {
            'Title': 'Remote Python Developer',
            'Company': 'TechCorp',
            'Location': 'Remote',
            'Posted': '2024-05-14',
            'Application Link': 'https://techcorp.com/jobs/remote-python-developer'
        },
        {
            'Title': 'Full Stack Developer',
            'Company': 'Innovatech',
            'Location': 'Remote',
            'Posted': '2024-05-13',
            'Application Link': 'https://innovatech.com/jobs/full-stack-developer'
        },
    ]

    # Write research data to Google Sheet
    google_sheet_tool.write_data(research_data)

    # Read data from Google Sheet
    data = google_sheet_tool.read_data()
    print("Data read from Google Sheet:", data)
