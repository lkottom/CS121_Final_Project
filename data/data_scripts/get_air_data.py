import pandas as pd

url = "https://en.wikipedia.org/wiki/List_of_active_United_States_military_aircraft"
tables = pd.read_html(url)  # Extract all tables

tables = tables[0:2] + tables[3:7] # only take tables which are the aircraft tables

# df = tables[0]  # Select the desired table (usually the first one)
# df.to_csv("us_military_aircraft.csv", index=False)  # Save to CSV

# Define column mapping for standardization
column_mapping = {
    'Aircraft': 'Type',
    'Introduced/IOC': 'Introduced',
    'Total': 'Inventory'
}

# Function to standardize columns in a dataframe
def standardize_columns(df):
    # Create a copy of the dataframe to avoid modifying the original
    df = df.copy()
    
    # Drop 'In service' column if it exists
    if 'In service' in df.columns:
        df = df.drop('In service', axis=1)
    
    # Rename columns based on mapping
    new_columns = {col: column_mapping.get(col, col) for col in df.columns}
    df = df.rename(columns=new_columns)
    
    return df

# Standardize column names in all valid tables
standardized_tables = [standardize_columns(table) for table in tables]

# Combine all tables
merged_table = pd.concat(standardized_tables, ignore_index=True)

# Reorder columns to a standard format
desired_columns = ['Type', 'Manufacturer', 'Origin', 'Propulsion', 'Role', 
                  'Control', 'Introduced', 'Inventory', 'Notes']
merged_table = merged_table[desired_columns]

merged_table = merged_table.drop_duplicates()

merged_table.to_csv("data/intermediate_data/aircraft.csv")