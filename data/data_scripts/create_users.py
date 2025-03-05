import pandas as pd
import random
import hashlib
import string

# Define reasonable clearance levels
CLEARANCE_LEVELS = ["Confidential", "Restricted", "Secret", "Top Secret"]
COUNTRIES = ["U.S.", "U.K.", "Germany", "France", "Canada", "Japan", "Australia", "Israel", "Brazil", "Russia", "China", "Egypt", "Italy", "Spain", "Mexico"]
MILITARY_BRANCHES = ["Army", "Navy", "Air Force", "Marines", "Coast Guard", "Space Force"]

# Load equipment CSV
equipment_df = pd.read_csv("data/final_data_for_sql/equipment.csv")

# Extract unique manufacturers
manufacturers_df = equipment_df[['manufacturer']].drop_duplicates()

# Assign user IDs for manufacturers
manufacturers_df["user_id"] = range(1, len(manufacturers_df) + 1)
manufacturers_df["clearance_lvl"] = [random.choice(CLEARANCE_LEVELS) for _ in range(len(manufacturers_df))]

# Assign user details for manufacturers
manufacturers_df["name"] = manufacturers_df["manufacturer"]
manufacturers_df["contact_email"] = manufacturers_df["manufacturer"].str.replace(" ", "").str.lower() + "@example.com"
manufacturers_df["country"] = [random.choice(COUNTRIES) for _ in range(len(manufacturers_df))]
manufacturers_df["salt"] = [''.join(random.choices(string.ascii_letters + string.digits, k=8)) for _ in range(len(manufacturers_df))]
manufacturers_df["password_hash"] = [hashlib.sha256((salt + "password123").encode()).hexdigest() for salt in manufacturers_df["salt"]]

# Generate all possible unique customer names
customer_names = [country + " " + branch for country in COUNTRIES for branch in MILITARY_BRANCHES]
customer_ids = list(range(len(manufacturers_df) + 1, len(manufacturers_df) + 1 + len(customer_names)))

customer_data = []
for user_id, name in zip(customer_ids, customer_names):
    country = name.split(" ")[0]  # Extract country from name
    salt = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    password_hash = hashlib.sha256((salt + "password123").encode()).hexdigest()
    customer_data.append([user_id, name, f"customer{user_id}@example.com", country, salt, password_hash, 1])

customers_df = pd.DataFrame(customer_data, columns=["user_id", "name", "contact_email", "country", "salt", "password_hash", "is_verified"])

# Combine users (manufacturers + customers)
users_df = pd.concat([manufacturers_df[['name', 'contact_email', 'country', 'salt', 'password_hash']], customers_df[['name', 'contact_email', 'country', 'salt', 'password_hash']]])

# Save to CSV files
users_df.to_csv("data/final_data_for_sql/users.csv", index=False)
manufacturers_df[['user_id', 'clearance_lvl']].to_csv("data/final_data_for_sql/manufacturers.csv", index=False)
customers_df[['user_id', 'is_verified']].to_csv("data/final_data_for_sql/customers.csv", index=False)

print("users.csv, manufacturers.csv, and customers.csv successfully created!")
