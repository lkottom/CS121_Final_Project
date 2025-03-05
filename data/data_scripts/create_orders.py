import pandas as pd
import random
from datetime import datetime, timedelta

# Load customers and equipment data
customers_df = pd.read_csv("data/final_data_for_sql/customers.csv")
equipment_df = pd.read_csv("data/final_data_for_sql/equipment.csv")

# Ensure customers and equipment have valid IDs
num_customers = len(customers_df["user_id"].tolist())
print (num_customers)
customer_ids = set(range(1, num_customers))

equipment_data = equipment_df[["equipment_id", "price_usd", "equipment_category"]].dropna()
equipment_ids = set(equipment_data["equipment_id"].tolist())

# Generate random orders
num_orders = 300
orders = []

for _ in range(num_orders):
    customer_id = random.choice(list(customer_ids))
    equipment = equipment_data.sample(1).iloc[0]  # Convert from DataFrame to Series

    equipment_id = int(equipment["equipment_id"])
    price_usd = float(equipment["price_usd"])
    category = equipment["equipment_category"]
    
    # Select order quantity based on category
    order_quantity = random.randint(1, 50) if category == "Aircraft" else random.randint(1, 500)

    total_amount = order_quantity * price_usd
    
    # Generate a random order date within the past 2 years
    days_offset = random.randint(0, 730)  # 730 days = 2 years
    order_date = datetime.now() - timedelta(days=days_offset)
    order_date_str = order_date.strftime("%Y-%m-%d %H:%M:%S")

    # Random order status
    status = random.choice(["pending", "approved", "rejected"])

    orders.append([customer_id, equipment_id, order_quantity, order_date_str, status, total_amount])

# Convert to DataFrame
orders_df = pd.DataFrame(orders, columns=["customer_id", "equipment_id", "order_quantity", "order_date", "status", "total_amount_usd"])

# Save to CSV
orders_df.to_csv("data/final_data_for_sql/orders.csv", index=False)

print("✅ orders.csv successfully created with", len(orders_df), "orders!")