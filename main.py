import pandas as pd

from config.google_sheets_auth import authenticate_google_sheets
from formatDataFrame import formatDataFrame
from extract_airbnb_data import extractAirbnbReservations
from extract_lodgify_data import extractLodgifyReservations
from push_to_google_sheets import push_to_google_sheets

client = authenticate_google_sheets()

# month = int(input("Enter the desired month (as a number): "))
# year = int(input("Enter the desired year: "))

month = 6
year = 2024

dataFrame1 = extractAirbnbReservations('reservations.csv')
dataFrame2 = extractLodgifyReservations('reservations_lodgify.csv')

jointDataFrame = pd.concat([dataFrame1, dataFrame2], ignore_index=True)

jointDataFrame = formatDataFrame(jointDataFrame, month, year)

push_to_google_sheets(client, jointDataFrame)