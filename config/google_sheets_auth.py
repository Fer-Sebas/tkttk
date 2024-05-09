import gspread
from oauth2client.service_account import ServiceAccountCredentials

def authenticate_google_sheets():
    # Define the scope
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/spreadsheets'
    ]

    # Load credentials
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)

    # Authenticate with Google Sheets API
    client = gspread.authorize(creds)
    return client 
