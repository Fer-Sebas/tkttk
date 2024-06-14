import pandas as pd
import gspread
import logging

def push_to_google_sheets(client, jointDataFrame):
    try:
        # Open the spreadsheet
        spreadsheet = client.open('TKTTK')
        logging.info("Spreadsheet opened successfully.")
        
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
                    logging.info(f"Worksheet for listing '{listing}' found.")
                except gspread.exceptions.WorksheetNotFound:
                    worksheets[listing] = spreadsheet.add_worksheet(title=listing, rows=1, cols=1)
                    logging.info(f"Worksheet for listing '{listing}' created.")
            
            # Get the worksheet for the current listing
            worksheet = worksheets[listing]
            
            # Clear the existing data in the worksheet
            worksheet.clear()
            logging.info(f"Worksheet for listing '{listing}' cleared.")
            
            # Convert Timestamp objects to strings
            listing_data_str = listing_data.applymap(lambda x: x.strftime('%Y-%m-%d %H:%M:%S') if isinstance(x, pd.Timestamp) else x)
            
            # Update the worksheet with the data for the current listing
            worksheet.update([listing_data_str.columns.values.tolist()] + listing_data_str.values.tolist())
            logging.info(f"Worksheet for listing '{listing}' updated with new data.")
            
            # Calculate totals for each column
            totals = listing_data.apply(lambda x: x.sum() if pd.api.types.is_numeric_dtype(x) else '')
            
            # Convert int64 objects to regular integers for JSON serialization
            totals = totals.apply(lambda x: int(x) if pd.api.types.is_numeric_dtype(x) else x)
            
            # Convert Timestamp objects in totals to strings
            totals_str = totals.apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S') if isinstance(x, pd.Timestamp) else x)
            
            # Append totals as a new row at the end of the worksheet
            worksheet.append_row(totals_str.values.tolist())
            logging.info(f"Totals row added to worksheet for listing '{listing}'.")

        
    except Exception as e:
        logging.error(f"An error occurred while pushing data to Google Sheets: {e}")

# Set up logging
logging.basicConfig(level=logging.INFO)
