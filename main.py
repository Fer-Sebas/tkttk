import pandas as pd
import logging
from config.google_sheets_auth import authenticate_google_sheets
from formatting.formatDataFrame import formatDataFrame
from extraction.extract_airbnb_data import extractAirbnbReservations
from extraction.extract_lodgify_data import extractLodgifyReservations
from delivery.push_to_google_sheets import push_to_google_sheets
from input.fetch_lodgify import fetch_and_write_lodgify_data
from input.scrap_airbnb import scrapeAirbnb

# Set up logging
logging.basicConfig(level=logging.INFO)

def main():
    try:

        # Get month and year from user input
        month = int(input("Enter the desired month (MM): "))
        year = int(input("Enter the desired year (YYYY): "))


        # Authenticate Google Sheets client
        client = authenticate_google_sheets()
        logging.info("Google Sheets client authenticated successfully.")

        logging.info("Scrapping AirBnb.")
        scrapeAirbnb()
        logging.info("AirBnb data retrieved.")

        fetch_and_write_lodgify_data(year, month)
        
        # Extract data
        logging.info("Extracting Airbnb reservations...")
        dataFrame1 = extractAirbnbReservations('input/reservations.csv')
        
        logging.info("Extracting Lodgify reservations...")
        dataFrame2 = extractLodgifyReservations('input/reservations_lodgify.csv')
        
        # Concatenate data
        jointDataFrame = pd.concat([dataFrame1, dataFrame2], ignore_index=True)
        logging.info("Data concatenation complete.")
        
        # Format data
        jointDataFrame = formatDataFrame(jointDataFrame, month, year)
        logging.info("Data formatting complete.")
        
        # Push to Google Sheets
        push_to_google_sheets(client, jointDataFrame)
        logging.info("Data pushed to Google Sheets successfully.")
    
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
