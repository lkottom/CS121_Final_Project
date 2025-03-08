# This script creates a PDF that is not used at all by the other code
# but can be used by someone testing the platform to map
# the equipment name to the manufacturer

import pandas as pd
from fpdf import FPDF

# Load the equipment CSV
equipment_df = pd.read_csv('data/final_data_for_sql/equipment.csv')

# Select relevant columns
equipment_manufacturer_mapping = equipment_df[['name', 'manufacturer']].copy()

# Remove duplicates to ensure unique name-manufacturer pairs
equipment_manufacturer_mapping.drop_duplicates(inplace=True)

# Initialize PDF
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("Arial", style="B", size=14)

# Title
pdf.cell(200, 10, "Equipment to Manufacturer Mapping", ln=True, align='C')
pdf.ln(10)  # Line break

# Set column headers
pdf.set_font("Arial", style="B", size=12)
pdf.cell(90, 10, "Equipment Name", border=1)
pdf.cell(90, 10, "Manufacturer Name", border=1, ln=True)

# Set font for data rows
pdf.set_font("Arial", size=10)

# Add rows to the PDF
for _, row in equipment_manufacturer_mapping.iterrows():
    pdf.cell(90, 8, row['name'], border=1)
    pdf.cell(90, 8, row['manufacturer'], border=1, ln=True)

# Save to a PDF file
pdf_output_path = 'equipment_to_manufacturer.pdf'
pdf.output(pdf_output_path)

print(f"Equipment-to-Manufacturer mapping PDF created: {pdf_output_path}")