import pandas as pd
import gspread as gspread

def push_to_google_sheets(client, jointDataFrame):
    spreadsheet = client.open('TKTTK')

    # Create a dictionary to store worksheets for each unique listing
    worksheets = {}

    # Iterate over unique listings
    for listing in jointDataFrame['Listing'].unique():
        # Filter data for the current listing
        listing_data = jointDataFrame[jointDataFrame['Listing'] == listing]
        
        # If the worksheet for the current listing doesn't exist, create it
        if listing not in worksheets:
            try:
                worksheets[listing] = spreadsheet.worksheet(listing)
            except gspread.exceptions.WorksheetNotFound:
                worksheets[listing] = spreadsheet.add_worksheet(title=listing, rows=1, cols=1)
        
        # Get the worksheet for the current listing
        worksheet = worksheets[listing]
        
        # Clear the existing data in the worksheet
        worksheet.clear()
        
        # Convert Timestamp objects to strings
        listing_data_str = listing_data.applymap(lambda x: x.strftime('%Y-%m-%d %H:%M:%S') if isinstance(x, pd.Timestamp) else x)
        
        # Update the worksheet with the data for the current listing
        worksheet.update([listing_data_str.columns.values.tolist()] + listing_data_str.values.tolist())

    # Share the spreadsheet with the specified email address
    email_address = 'heyferrius@gmail.com'
    spreadsheet.share(email_address, perm_type='user', role='writer')
