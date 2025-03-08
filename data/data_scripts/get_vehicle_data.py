import pandas as pd

url = "https://en.wikipedia.org/wiki/List_of_equipment_of_the_United_States_Army"
tables = pd.read_html(url)  # Extract all tables

tables = tables[3:5]

# df = tables[0]  # Select the desired table (usually the first one)
# df.to_csv("us_military_aircraft.csv", index=False)  # Save to CSV

# for table in tables:
#     print (table.head(1))

# Convert MultiIndex columns to single-level by taking the first level
cleaned_tables = []
for table in tables:
    if isinstance(table.columns, pd.MultiIndex):
        table.columns = table.columns.get_level_values(0)  # Keep only the first level
    # Drop 'Image' column
    table = table.drop('Image', axis=1)

    # Rename "Type"
    table = table.rename(columns={"Type": "Role"})
    
    cleaned_tables.append(table)

# Define column mapping for standardization
column_mapping_1 = {
    'Model': 'Type',
    'Numbers': 'Inventory'
}

column_mapping_2 = {
    'Name': 'Type',
    'Quantity': 'Inventory',
    'Details': 'Notes'
}

tables = cleaned_tables    
    

standardized_tables = []


# Rename for first
table_1 = tables[0]
new_columns = {col: column_mapping_1.get(col, col) for col in table_1.columns}
table_1 = table_1.rename(columns=new_columns)
standardized_tables.append(table_1)

# And for second
table_2 = tables[1]
new_columns = {col: column_mapping_2.get(col, col) for col in table_2.columns}
table_2 = table_2.rename(columns=new_columns)
standardized_tables.append(table_2)

for table in standardized_tables:
    # print (table.columns)
    continue

# Combine all tables
merged_table = pd.concat(standardized_tables, ignore_index=True)

# Reorder columns to a standard format
desired_columns = ['Type', 'Caliber', 'Role', 'Origin', 'Inventory', 'Notes']
merged_table = merged_table[desired_columns]

merged_table = merged_table.drop_duplicates()

merged_table.to_csv("data/intermediate_data/vehicles.csv")