import os
import requests
import csv
from datetime import datetime

def fetch_and_write_lodgify_data(year, month):
    # Validate the input year and month format
    try:
        datetime.strptime(f"{year}-{month}-01", "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please enter the year in YYYY format and the month in MM format.")
        return
    
    # Define the URL and headers
    period_start = f"{year}-{month}-01"
    url = f"https://api.lodgify.com/v1/reservation?offset=0&limit=50&status=booked&trash=false&periodStart={period_start}"
    headers = {
        "accept": "application/json",
        "X-ApiKey": "2XpoSQnYKXhqrMxYREigJuAIAIH6q9b4WbD37kbWzcn6+fBxA6aROagi6R14MJpV"
    }
    
    # Make the request
    response = requests.get(url, headers=headers)
    
    # Check if request was successful
    if response.status_code != 200:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return
    
    # Parse the JSON response
    data = response.json()
    
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define the CSV file path
    csv_file = os.path.join(script_dir, f'reservations_lodgify.csv')
    
    # Open the CSV file for writing
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write the header row
        header = [
            'arrival', 'departure', 'property_name', 'guest_name', 'status', 'source_text',
            'total_amount',
        ]
        writer.writerow(header)
        
        # Write the data rows, filtering out rows where source is AirbnbIntegration or property_name is (Not available)
        for item in data['items']:
            if item['source'] != 'AirbnbIntegration' and item['property_name'] != '(Not available)' and item['guest']['name'] is not None:
                row = [
                    item['arrival'],
                    item['departure'],
                    item['property_name'],
                    item['guest']['name'],
                    item['status'],
                    item['source_text'],
                    item['total_amount'],
                ]
                writer.writerow(row)
    
    print(f"Data has been written to {csv_file}")