import pandas as pd
import re
import openpyxl

df1 = pd.read_csv('reservations.csv')
df2 = pd.read_csv('reservations_lodgify.csv')

column_mapping = {
    'DateArrival': 'Start date', 
    'DateDeparture': 'End date',
    'Name': 'Guest name',
    'HouseName': 'Listing',
    'RoomRatesTotal': 'Earnings'
}

df2.rename(columns=column_mapping, inplace=True)

replacement_dict = {
    r'Beach Heaven[\s-]*Private Beach,?[\s]*Pool': 'Beach Heaven',
    r'Ocean Oasis!OceanView[\s-]*Beach/Pool': 'Ocean Oasis',
    r'Paradise Cove!30ft Dock[\s]*Pool[\s]*BBQ': 'Paradise Cove',
    r'The Purple Pelican Inn/Private[\s]*Hot Tub': 'The Purple Pelican Inn',
    r'Bliss on the Bay![\s]*Pool&Boat Ramp': 'Bliss on the Bay',
    r'Barefoot Bungalow![\s]*\+[\s]*Beach/Pool': 'Barefoot Bungalow',
    r'Dolphin Den-Pool-Boat Ramp-BBQ': 'Dolphin Den',
    r'HotTub Hideaway! PoolTable& More': 'HotTub Hideaway'
}

cleaning_fee_dict = {
    'Barefoot Bungalow': 160,
    'Beach Heaven': 200,
    'Bliss on the Bay': 150,
    'Paradise Cove': 300,
    'The Coral Cottage Inn': 140,
    'Dolphin Den': 180,
    'The Purple Pelican Inn': 120,
    'The Lazy Turtle Inn': 140,
    'Bayside Relaxing Home': 180,
    'HotTub Hideaway': 160,
    'Ocean Oasis': 0
}

# Replace values in 'Listing' column using replacement dictionary
df1['Listing'] = df1['Listing'].replace(replacement_dict, regex=True)
df2['Listing'] = df2['Listing'].replace(replacement_dict, regex=True)

# Convert date columns to datetime format
df1['Start date'] = pd.to_datetime(df1['Start date'], format='%m/%d/%Y')
df1['End date'] = pd.to_datetime(df1['End date'], format='%m/%d/%Y')

# Convert date columns from the second file to MM/DD/YYYY format
df2['Start date'] = pd.to_datetime(df2['Start date'], format='%Y-%m-%d', errors= 'coerce')
df2['End date'] = pd.to_datetime(df2['End date'], format='%Y-%m-%d', errors= 'coerce')


# Sort DataFrame by 'Listing' and 'Start date'
df1 = df1.sort_values(by=['Listing', 'Start date'])

# Extract numeric values from 'Earnings' column and convert to float
df1['Earnings'] = df1['Earnings'].str.replace(r'[^\d.]', '', regex=True).astype(float)

# Map 'Cleaning fee' using cleaning fee dictionary
df1['Cleaning fee'] = df1['Listing'].map(cleaning_fee_dict)
df2['Cleaning fee'] = df2['Listing'].map(cleaning_fee_dict)

# Calculate 'Tourist tax' and 'Management fee'
df1['Tourist tax'] = df1['Earnings'] * 0.05
df1['Total after fees'] = df1['Earnings'] - (df1['Cleaning fee'] + df1['Tourist tax'])
df1['Management fee'] = df1['Total after fees'] * 0.18

df2['Tourist tax'] = df2['Earnings'] * 0.05
df2['Total after fees'] = df2['Earnings'] - (df2['Cleaning fee'] + df2['Tourist tax'])
df2['Management fee'] = df2['Total after fees'] * 0.18

# Add 'Platform' column and set all values to 'airbnb'
df1['Platform'] = 'Airbnb'

df2['Platform'] = df2['Source']

# Extract month and year from selected_month and selected_year
selected_month = 4
selected_year = 2024

# Filter data based on selected month and year
df1 = df1[(df1['Start date'].dt.month == selected_month) & (df1['Start date'].dt.year == selected_year)]
df2 = df2[(df2['Start date'].dt.month == selected_month) & (df2['Start date'].dt.year == selected_year)]

# Format monetary columns
df1['Earnings'] = df1['Earnings'].apply(lambda x: "${:,.2f}".format(x))
df1['Cleaning fee'] = df1['Cleaning fee'].apply(lambda x: "${:,.2f}".format(x))
df1['Tourist tax'] = df1['Tourist tax'].apply(lambda x: "${:,.2f}".format(x))
df1['Management fee'] = df1['Management fee'].apply(lambda x: "${:,.2f}".format(x))

df2['Earnings'] = df2['Earnings'].apply(lambda x: "${:,.2f}".format(x))
df2['Cleaning fee'] = df2['Cleaning fee'].apply(lambda x: "${:,.2f}".format(x))
df2['Tourist tax'] = df2['Tourist tax'].apply(lambda x: "${:,.2f}".format(x))
df2['Management fee'] = df2['Management fee'].apply(lambda x: "${:,.2f}".format(x))

df2 = df2[df2['Type'] == 'Booking']

# Select columns for the final DataFrame
df1 = df1[['Listing', 'Guest name', 'Start date', 'End date', 'Earnings', 'Cleaning fee', 'Tourist tax', 'Total after fees', 'Management fee', 'Platform']]
df2 = df2[['Listing', 'Guest name', 'Start date', 'End date', 'Earnings', 'Cleaning fee', 'Tourist tax', 'Total after fees', 'Management fee',  'Platform']]

# Add 'Platform' column and map values from 'source' column

df2 = df2[df2['Platform'] != 'Airbnb']


# Merge data from df1 and df2
merged_df = pd.concat([df1, df2], ignore_index=True)

# Select only the desired columns
merged_df = merged_df[['Listing', 'Guest name', 'Start date', 'End date', 'Earnings', 'Cleaning fee', 'Tourist tax', 'Total after fees', 'Management fee', 'Platform']]
unique_listings = merged_df['Listing'].unique()

# Write each listing to a separate sheet
with pd.ExcelWriter(f'TKTTK-A-{selected_month}-{selected_year}.xlsx', engine='openpyxl') as writer:
    
    merged_df.to_excel(writer, sheet_name='Global', index=False)

    workbook = writer.book
    worksheet = writer.sheets['Global']

    for col in range(1, 11):
        col_letter = openpyxl.utils.get_column_letter(col)
        worksheet.column_dimensions[col_letter].width = 20
    
    for listing_id in merged_df['Listing'].unique():
        df_listing = merged_df[merged_df['Listing'] == listing_id]
        sanitized_sheet_name = re.sub(r'[\\/*?:\[\]]', '', f'{listing_id}')
        df_listing.to_excel(writer, sheet_name=sanitized_sheet_name, index=False)
        worksheet = writer.sheets[sanitized_sheet_name]
        for col in range(1, 11):
            col_letter = openpyxl.utils.get_column_letter(col)
            worksheet.column_dimensions[col_letter].width = 20