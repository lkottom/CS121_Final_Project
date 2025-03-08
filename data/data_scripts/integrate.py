import pandas as pd
import numpy as np
import csv
import random
import re

manufacturer_mapping = {
    "Fairchild Republic": "Fairchild",
    "Fairchild-Dornier": "Fairchild",
    "de Havilland Canada": "De Havilland Canada",
    "McDonnell Douglas/Boeing": "McDonnell Douglas & Boeing",
    "Bell, Boeing": "Bell & Boeing",
    "McDonnell Douglas": "McDonnell Douglas",
    "McDonnell Douglas / Northrop Grumman / Boeing": "McDonnell Douglas, Northrop Grumman & Boeing",
    "General Dynamics": "General Dynamics",
    "Raytheon/Beechcraft": "Raytheon & Beechcraft",
    "Boeing / Saab": "Boeing & Saab",
    "Sikorsky Aircraft": "Sikorsky",
    "Boeing Insitu": "Boeing Insitu",
    "Leonardo Helicopter": "AgustaWestland",
    "Lockheed": "Lockheed Martin",
    "Northrop": "Northrop Grumman",
    "Grumman": "Northrop Grumman",
    "MD Helicopter": "McDonnell Douglas",
    "Eurocopter": "Airbus Eurocopter",
    "Teledyne FLIR": "FLIR"
}

def parse_descriptions(description_file):
    """Parse equipment descriptions from text file."""
    descriptions = {}
    with open(description_file, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            # Match pattern like: "0. A-10C Thunderbolt II: Description text..."
            parts = line.split(':', 1)
            if len(parts) < 2:
                continue
                
            header, description = parts
            # Extract the index number from the header
            index_parts = header.split('.', 1)
            if len(index_parts) < 2:
                continue
                
            try:
                index = int(index_parts[0])
                # Clean description to remove brackets and parentheses and their contents
                cleaned_desc = re.sub(r'\[[^\]]*\]', '', description.strip())
                cleaned_desc = re.sub(r'\([^)]*\)', '', cleaned_desc)
                descriptions[index] = cleaned_desc
            except ValueError:
                continue
    
    return descriptions

def get_random_price():
    """Generate a random price between 10 million and 200 million USD."""
    return random.randint(10000000, 200000000)

def clean_text(text):
    """Remove quotes, backslashes, pipes, and content within brackets and parentheses."""
    if pd.isna(text):
        return 'Unknown'
    
    # Remove content within brackets like [33] using regex
    text = re.sub(r'\[[^\]]*\]', '', text)
    
    # Remove content within parentheses like (example) using regex
    text = re.sub(r'\([^)]*\)', '', text)
    
    # Remove quotes, backslashes, and pipes
    text = text.replace('"', '').replace("'", '').replace('\\', '').replace('|', '')
    
    return text.strip() or 'Unknown'

def combine_equipment_data():
    """Combine aircraft and vehicle data into a single dataset."""
    # Read the CSV files
    aircraft_df = pd.read_csv('data/intermediate_data/aircraft.csv')
    vehicles_df = pd.read_csv('data/intermediate_data/vehicles.csv')
    
    # Read the descriptions
    aircraft_descriptions = parse_descriptions('data/intermediate_data/aircraft_descriptions.txt')
    vehicle_descriptions = parse_descriptions('data/intermediate_data/vehicle_description.txt')

    print (vehicle_descriptions)
    
    # Read vehicle manufacturers
    with open('data/intermediate_data/vehicle_manufacturer.txt', 'r') as file:
        manufacturers = [clean_text(line.strip()) for line in file if line.strip()]
    
    # Initialize the combined dataframe
    combined_data = []
    
    # Process aircraft
    for idx, aircraft in aircraft_df.iterrows():
        manufacturer = clean_text(aircraft['Manufacturer'])
        if manufacturer == "Unknown": continue # Just skip where unknown

        manufacturer = manufacturer_mapping.get(manufacturer, manufacturer)

        combined_data.append({
            'name': clean_text(aircraft['Type']),
            'equipment_id': idx + 1,
            'equipment_category': 'Aircraft',
            'specialty': clean_text(aircraft['Role']),
            'price_usd': get_random_price(),
            'manufacturer': manufacturer,
            'manufacturer_id': None, # placeholder
            'stock': random.randint(1, 100),
            'description': clean_text(aircraft_descriptions.get(idx, 'No description available'))
        })
    
    # Process vehicles
    for idx, vehicle in vehicles_df.iterrows():
        
        # Get manufacturer from index
        manufacturer = manufacturers[idx] if idx < len(manufacturers) else 'Unknown'

        manufacturer = clean_text(manufacturer)

        manufacturer = manufacturer_mapping.get(manufacturer, manufacturer)
        
        combined_data.append({
            'equipment_id': len(aircraft_df) + idx + 1,
            'name': clean_text(vehicle['Type']),
            'equipment_category': 'Land Vehicle',
            'specialty': clean_text(vehicle['Role']),
            'price_usd': get_random_price(),
            'manufacturer': manufacturer,
            'manufacturer_id': None, # placeholder
            'stock': random.randint(1, 1000),
            'description': clean_text(vehicle_descriptions.get(idx, 'No description available'))
        })
    
    # Convert to DataFrame
    combined_df = pd.DataFrame(combined_data)

    # Add ID
    combined_df['manufacturer_id'] = combined_df.groupby('manufacturer').ngroup() + 1

    # Lastly, remove duplicates
    combined_df.drop_duplicates(subset=['name'], keep='first', inplace=True)

    quote_columns = {'name', 'specialty', 'manufacturer', 'description'} # columns to add quotes to (since they have commas)
    
    # Custom CSV writing to quote only the description column
    with open('data/final_data_for_sql/equipment.csv', 'w', newline='') as f:
        # Write the header row
        f.write(','.join(combined_df.columns) + '\n')
        
        # Write each data row with quotes only on the description field
        for _, row in combined_df.iterrows():
            row_values = [f'"{value}"' if column in quote_columns else str(value) for column, value in zip(combined_df.columns, row)]
            f.write(','.join(row_values) + '\n')
    
    print(f"Combined dataset created with {len(combined_df)} records.")
    print(f"- Aircraft: {len(aircraft_df)}")
    print(f"- Vehicles: {len(vehicles_df)}")
    
    return combined_df

# Example usage
if __name__ == "__main__":
    combined_df = combine_equipment_data()
    
    # Display sample of the combined dataset
    print("\nSample of combined dataset:")
    print(combined_df.head())
    
    # Display statistics
    print("\nCategory distribution:")
    print(combined_df['equipment_category'].value_counts())
    
    print("\nPrice statistics (USD):")
    print(combined_df['price_usd'].describe())
    
    print("\nTop manufacturers by count:")
    print(combined_df['manufacturer'].value_counts().head(10))
    
    print("\nStock statistics:")
    print(combined_df.groupby('equipment_category')['stock'].describe())