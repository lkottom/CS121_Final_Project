First, flow is to create equipment.csv:
"get_air_data.py" scrapes Wikipedia for airplane data and saves it nicely
"get_vehicle_data.py" scrapes Wikipedia for vehicle data and saves it nicely
"integrate.py" takes data produced by the previous two scripts as well as the 3 AI-produced txt files in "intermediate_data" and combines them into main data source

Then, run create_users.py (makes customers.csv, manufacturers.csv, users.csv)

Finally, run create_orders.py (makes orders.csv)