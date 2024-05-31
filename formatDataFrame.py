import pandas as pd
from config.listingNameDictionary import replacement_dict
from config.cleaningFees import cleaning_fee_dict

def formatDataFrame(dataFrame, selected_month, selected_year):

    # Convert date columns to MM/DD/YYYY format

    dataFrame['Start date'] = pd.to_datetime(dataFrame['Start date'], errors='coerce')
    dataFrame['End date'] = pd.to_datetime(dataFrame['End date'], errors='coerce')


    # Filter data based on selected month and year

    filteredDataFrame = dataFrame[(dataFrame['Start date'].dt.month == selected_month) & (dataFrame['Start date'].dt.year == selected_year)].copy()

    # Calculate amount of nights

    filteredDataFrame['Nights'] = (dataFrame['End date'] - dataFrame['Start date']).dt.days
    
    # Replace values in 'Listing' column using replacement dictionary

    filteredDataFrame['Listing'] = filteredDataFrame['Listing'].replace(replacement_dict, regex=True)


    # Map 'Cleaning fee' using cleaning fee dictionary

    filteredDataFrame['Cleaning fee'] = filteredDataFrame['Listing'].map(cleaning_fee_dict)


    # Map 'Cleaning fee' using cleaning fee dictionary

    # Calculate 'Tourist tax' and 'Management fee'

    filteredDataFrame['Tourist tax'] = (filteredDataFrame['Earnings']) * 0.05

    # Add columns for sales tax and VRBO fee for VRBO bookings
    filteredDataFrame['Sales tax'] = filteredDataFrame.apply(lambda row: row['Earnings'] * 0.05 if row['Platform'] == 'VRBO' else 0, axis=1)
    filteredDataFrame['VRBO fee'] = filteredDataFrame.apply(lambda row: row['Earnings'] * 0.075 if row['Platform'] == 'VRBO' else 0, axis=1)

    filteredDataFrame['Total after fees'] = filteredDataFrame['Earnings'] - (filteredDataFrame['Cleaning fee'] + filteredDataFrame['Tourist tax'] + filteredDataFrame['Sales tax'] + filteredDataFrame['VRBO fee'])
    filteredDataFrame['Management fee'] = filteredDataFrame['Total after fees'] * 0.18

    # Format monetary columns
    filteredDataFrame['Earnings'] = filteredDataFrame['Earnings'].apply(lambda x: "${:,.2f}".format(x))
    filteredDataFrame['Cleaning fee'] = filteredDataFrame['Cleaning fee'].apply(lambda x: "${:,.2f}".format(x))
    filteredDataFrame['Tourist tax'] = filteredDataFrame['Tourist tax'].apply(lambda x: "${:,.2f}".format(x))
    filteredDataFrame['Total after fees'] = filteredDataFrame['Total after fees'].apply(lambda x: "${:,.2f}".format(x))
    filteredDataFrame['Management fee'] = filteredDataFrame['Management fee'].apply(lambda x: "${:,.2f}".format(x))
    filteredDataFrame['Sales tax'] = filteredDataFrame['Sales tax'].apply(lambda x: "${:,.2f}".format(x))
    filteredDataFrame['VRBO fee'] = filteredDataFrame['VRBO fee'].apply(lambda x: "${:,.2f}".format(x))


    filteredDataFrame = filteredDataFrame.sort_values(by=['Listing', 'Start date'])

    # Select columns for the final DataFrame
    finalDataFrame = filteredDataFrame[['Listing', 'Guest name', 'Platform', 'Start date', 'End date', 'Nights', 'Earnings', 'Cleaning fee', 'Tourist tax', 'Sales tax', 'VRBO fee', 'Total after fees', 'Management fee']]

    return finalDataFrame
