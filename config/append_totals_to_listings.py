import pandas as pd

def append_totals_to_listings(listings_dict):
    for listing, dataFrame in listings_dict.items():
        # Calculate totals for columns 'Nights' to 'Management fee'
        totals = dataFrame.loc[:, 'Nights':'Management fee'].sum()
        
        # Append a new row with the totals to the DataFrame
        totals['Listing'] = listing  # Add the listing name to the totals row
        dataFrame = dataFrame.append(totals, ignore_index=True)
        
        # Update the DataFrame in the dictionary
        listings_dict[listing] = dataFrame
        
    return listings_dict