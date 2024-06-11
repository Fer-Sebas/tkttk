def organize_by_listing(finalDataFrame):
    # Group the final DataFrame by 'Listing'
    grouped_by_listing = finalDataFrame.groupby('Listing')
    
    # Create a dictionary to store DataFrames for each listing
    listings_dict = {}
    
    # Iterate over each group (listing) and store it in the dictionary
    for listing, dataFrame in grouped_by_listing:
        listings_dict[listing] = dataFrame
    
    return listings_dict