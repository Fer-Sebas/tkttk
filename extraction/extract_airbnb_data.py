import pandas as pd

def extractAirbnbReservations(csv_file):

    # Read the CSV file
    df = pd.read_csv(csv_file)

    df = df[df['Status'] != 'Canceled by guest']
    df = df[df['Status'] != 'Canceled by Airbnb']

    # Add 'Platform' column and set all values to 'airbnb'
    df['Platform'] = 'Airbnb'

    df['Earnings'] = df['Earnings'].str.replace('$', '', regex=False)
    df['Earnings'] = df['Earnings'].str.replace(',', '', regex=False).astype(float)

    # Select columns for the final DataFrame
    df = df[['Listing', 'Guest name', 'Start date', 'End date', 'Earnings', 'Platform']]

    return df
