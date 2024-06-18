import pandas as pd

column_mapping = {
    'arrival': 'Start date', 
    'departure': 'End date',
    'guest_name': 'Guest name',
    'property_name': 'Listing',
    'total_amount': 'Earnings',
    'source_text': 'Platform',
}

def extractLodgifyReservations(csv_file):

    # Read the CSV file
    df = pd.read_csv(csv_file)

    # Rename columns using column mapping
    df.rename(columns=column_mapping, inplace=True)

    df['Earnings'] = df['Earnings'].astype(float)

    # Select columns for the final DataFrame
    df = df[['Listing', 'Guest name', 'Start date', 'End date', 'Earnings', 'Platform']]

    return df
