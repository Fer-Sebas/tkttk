import pandas as pd

column_mapping = {
    'DateArrival': 'Start date', 
    'DateDeparture': 'End date',
    'Name': 'Guest name',
    'HouseName': 'Listing',
    'TotalAmount': 'Earnings',
    'SourceText': 'Platform',
}

def extractLodgifyReservations(csv_file):

    # Read the CSV file
    df = pd.read_csv(csv_file)

    # Rename columns using column mapping
    df.rename(columns=column_mapping, inplace=True)

    # Filter out rows where 'Type' is not 'Booking'
    df = df[df['Type'] == 'Booking']

    df = df[df['Platform'] != 'Airbnb']

    df['Earnings'] = df['Earnings'].astype(float)

    # Select columns for the final DataFrame
    df = df[['Listing', 'Guest name', 'Start date', 'End date', 'Earnings', 'Platform']]

    return df
