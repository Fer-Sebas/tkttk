import pandas as pd
import re
import openpyxl

df = pd.read_csv('reservations.csv')

replacement_dict = {
    r'Beach Heaven[\s-]*Private Beach,?[\s]*Pool': 'Beach Heaven',
    r'Ocean Oasis!OceanView[\s-]*Beach/Pool': 'Ocean Oasis',
    r'Paradise Cove!30ft Dock[\s]*Pool[\s]*BBQ': 'Paradise Cove',
    r'The Purple Pelican Inn/Private[\s]*Hot Tub': 'The Purple Pelican Inn',
    r'Bliss on the Bay![\s]*Pool&Boat Ramp': 'Bliss on the Bay',
    r'Barefoot Bungalow![\s]*\+[\s]*Beach/Pool': 'Barefoot Bungalow',
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

df['Listing'] = df['Listing'].replace(replacement_dict, regex=True)

df['Start date'] = df['Start date'].str.extract(r'(\d{1,2}/\d{1,2}/\d{4})')
df['End date'] = df['End date'].str.extract(r'(\d{1,2}/\d{1,2}/\d{4})')

df['Start date'] = pd.to_datetime(df['Start date'], format='%m/%d/%Y')
df['End date'] = pd.to_datetime(df['End date'], format='%m/%d/%Y')

df = df.sort_values(by=['Listing', 'Start date'])

df['Guest name'] = df['Guest name'] 

df['Earnings'] = df['Earnings'].str.extract(r'(\d+\.\d+)').astype(float)

df['Cleaning fee'] = df['Listing'].map(cleaning_fee_dict)

df['Tourist tax'] = df['Earnings'] * 0.05

df['Management fee'] = (df['Earnings'] - df['Cleaning fee']) * 0.18


selected_month = 4
selected_year = 2024
df = df[(df['Start date'].dt.month == selected_month) & (df['Start date'].dt.year == selected_year)]

df['Earnings'] = df['Earnings'].apply(lambda x: "${:,.2f}".format(x))
df['Cleaning fee'] = df['Cleaning fee'].apply(lambda x: "${:,.2f}".format(x))
df['Tourist tax'] = df['Tourist tax'].apply(lambda x: "${:,.2f}".format(x))
df['Management fee'] = df['Management fee'].apply(lambda x: "${:,.2f}".format(x))


df = df[['Listing', 'Guest name', 'Start date', 'End date',  'Earnings', 'Cleaning fee', 'Tourist tax', 'Management fee']]

with pd.ExcelWriter(f'TKTTK-A-{selected_month}-{selected_year}.xlsx', engine='openpyxl') as writer:
    
    df.to_excel(writer, sheet_name='Global', index=False)

    workbook = writer.book
    worksheet = writer.sheets['Global']

    for col in range(1, 11):
        
        col_letter = openpyxl.utils.get_column_letter(col)
        worksheet.column_dimensions[col_letter].width = 20
    
    for listing_id in df['Listing'].unique():
        
        df_listing = df[df['Listing'] == listing_id]
        
        sanitized_sheet_name = re.sub(r'[\\/*?:\[\]]', '', f'{listing_id}')
        
        df_listing.to_excel(writer, sheet_name=sanitized_sheet_name, index=False)

        worksheet = writer.sheets[sanitized_sheet_name]
        for col in range(1, 11):
            col_letter = openpyxl.utils.get_column_letter(col)
            worksheet.column_dimensions[col_letter].width = 20
