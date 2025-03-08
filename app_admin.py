"""
Student name(s): Luke Kottom, Matthew Casertano 
Student email(s): lkottom@caltech.edu, mcaserta@caltech.edu

This application provides an interface for administrators (manufacturers) of the
military equipment store database system.
The system allows manufacturers to manage their inventory, update equipment details,
view sales statistics, and process orders.
"""

import sys 
import mysql.connector
import mysql.connector.errorcode as errorcode

# Debugging flag to print errors when debugging that shouldn't be visible
# to an actual admin. ***Set to False when done testing.***
DEBUG = False

# Global varibles used to track the login state and the ids
# (these will be used in lots of functions)
current_user = None
current_user_id = None
current_manufacturer_id = None

def get_conn():
    """"
    Returns a connected MySQL connector instance, if connection is successful.
    If unsuccessful, exits.
    """
    try:
        conn = mysql.connector.connect(
          host='localhost',
          user='military_admin',
          # Find port in MAMP or MySQL Workbench GUI or with
          # SHOW VARIABLES WHERE variable_name LIKE 'port';
          port='3306',  # this may change!
          password='adminpw',
          database='military_db'
        )
        print('Successfully connected.')
        return conn
    except mysql.connector.Error as err:
        # Remember that this is specific to _database_ users, not
        # application users. So is probably irrelevant to a client in your
        # simulated program. Their user information would be in a users table
        # specific to your database; hence the DEBUG use.
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR and DEBUG:
            sys.stderr.write('Incorrect username or password when connecting to DB.\n')
        elif err.errno == errorcode.ER_BAD_DB_ERROR and DEBUG:
            sys.stderr.write('Database does not exist.\n')
        elif DEBUG:
            sys.stderr(err)
        else:
            # A fine catchall client-facing message.
            sys.stderr.write('An error occurred, please contact the administrator.\n')
        sys.exit(1)

# ----------------------------------------------------------------------
# Functions for Logging Users In/Out
# ----------------------------------------------------------------------
def login_admin():
    """
    Handles the login process for manufacturers/admins.
    All admins are already in the assumed to be in the database 
    system (you cannot create admins). Returns True if login is successful.
    False if not successful.
    """
    # global variables used to hold user inputs 
    global current_user, current_user_id, current_manufacturer_id

    print("\n--- Admin Log In ---")
    username = input('Enter admin username (your email): ')
    password = input('Enter password: ')
    
    try:
        # start the cursor
        cursor = conn.cursor()
        # Use the authenticate function from setup-passwords.sql
        sql = "SELECT authenticate(%s, %s) AS auth_result"
        cursor.execute(sql, (username, password))
        # Fetchone here because we are getting one result
        result = cursor.fetchone()
        
        # Make sure we get a result (and making sure the result is 
        # successful which would be = 1 / how the auth function was
        # designed)
        if result and result[0] == 1:
            # Here, we are getting the user_id
            sql = "SELECT user_id FROM users WHERE contact_email = %s"
            cursor.execute(sql, (username,))
            user_result = cursor.fetchone()
            
            # If there is a user result, get the username and the
            # user result
            if user_result:
                current_user = username
                current_user_id = user_result[0]
                
                # Make sure the user is a manufacturer (just for redundency)
                sql = "SELECT manufacturer_id FROM manufacturers WHERE user_id = %s"
                cursor.execute(sql, (current_user_id,))
                manufacturer_result = cursor.fetchone()
                
                if manufacturer_result:
                    current_manufacturer_id = manufacturer_result[0]
                    print(f'Login successful! Welcome {username}.')
                    return True
                else:
                    print('Access denied: User is not a manufacturer/admin.')
            else:
                print('User not found in system.')
        else:
            print('Invalid username or password.')
            
        cursor.close()
        return False
        
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr.write('An error occurred when logging in\n')
            return False

def logout():
    """
    Logs out the current user and returns to the login screen.
    Returns false if not logged in
    """
    global current_user, current_user_id, current_manufacturer_id
    
    if current_user:
        print(f"Logging out admin: {current_user}")
        # Makign sure to reset all our global varibels so they are ready for 
        # a new user
        current_user = None
        current_user_id = None
        current_manufacturer_id = None
        
        # Then, we return to the login screen
        return login_admin()
    else:
        print("No admin is currently logged in.")
        return False

# ----------------------------------------------------------------------
# Functions for Command-Line Options/Query Execution
# ----------------------------------------------------------------------

def browse_equipment():
    """
    This function allows manufacturers to view equipment in the database.
    The admins can filter by type, view details, stock, or function.
    """
    print("\n--- 1. Browse Equipment ---")
    
    print("\nBrowse Equipment Options:")
    print("1. Display Stock")
    print("2. Display Details")
    print("3. Display by Type")
    print("4. Return to main menu")
    
    choice = input("Enter choice (1-4): ")
    
    if choice == '1':
        display_stock()
    elif choice == '2':
        display_details()
    elif choice == '3':
        display_by_type()
    elif choice == '4':
        return
    else:
        print("Invalid choice. Please try again.")
        browse_equipment()

def display_stock():
    """
    Displays current stock levels for all equipment from the manufacturer.
    Pressing enter will return them back to the menu
    """
    print("\n--- Display Stock ---")
    
    try:
        # Start the cursor, like we always do
        cursor = conn.cursor()
        sql = """
        SELECT e.name, e.stock, e.equipment_category 
        FROM equipment e 
        WHERE e.manufacturer_id = %s
        ORDER BY e.stock
        """
        cursor.execute(sql, (current_manufacturer_id,))
        rows = cursor.fetchall()
        # Same display format as usual
        if not rows:
            print("You don't have any equipment in the database.")
        else:
            print("\nCurrent Stock Levels (lowest to highest):")
            for row in rows:
                name, stock, category = row
                print(f"Equipment Name: {name} | Stock: {stock} | Category: {category}")
                
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            print("An error occurred while retrieving stock information.")
            
    finally:
        cursor.close()
        
    input("\nPress Enter to return to browse menu...")
    browse_equipment()

def display_details():
    """
    Displays detailed information about equipment. Will display the name, 
    catagory, function, description, price, and stock for a specific equipment.
    Pressing enter will return them back to the menu
    """
    print("\n--- Display Details ---")
    
    equipment_name = input("Enter equipment name (or 'all' for all equipment): ")
    
    try:
        cursor = conn.cursor()
        
        # If they want to see all their equ, display it using select
        if equipment_name.lower() == 'all':
            sql = """
            SELECT e.name, e.equipment_category, e.specialty, e.description, 
                   e.price_usd, e.stock
            FROM equipment e
            WHERE e.manufacturer_id = %s
            ORDER BY e.name
            """
            cursor.execute(sql, (current_manufacturer_id,))
        # display the specific equ details 
        else:
            sql = """
            SELECT e.name, e.equipment_category, e.specialty, e.description, 
                   e.price_usd, e.stock
            FROM equipment e
            WHERE e.manufacturer_id = %s AND e.name LIKE %s
            ORDER BY e.name
            """
            # Making sure we put it in the proper LIKE format
            cursor.execute(sql, (current_manufacturer_id, f"%{equipment_name}%"))
            
        rows = cursor.fetchall()
        
        if not rows:
            print(f"No equipment found matching '{equipment_name}'.")
        else:
            # Printing the resutls in a nice and clear format
            print("\nEquipment Details:")
            for row in rows:
                name, category, specialty, description, price, stock = row
                print(f"Name: {name}")
                print(f"Category: {category}")
                print(f"Function: {specialty}")
                print(f"Description: {description}")
                print(f"Price: ${price:,.2f}")
                print(f"Stock: {stock}\n")

    # Error handling
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            print("An error occurred while retrieving equipment details.")
            
    finally:
        cursor.close()
        
    input("\nPress Enter to return to browse menu...")
    browse_equipment()

def display_by_type():
    """
    Displays equipment filtered by type (Aircraft or Land Vehicle). Will show
    Name, Function, Stock, Price (and category if applicable for all). 
    Pressing enter will return them back to the menu
    """
    print("\n--- Display by Type ---")
    
    print("Equipment Types:")
    print("1. Aircraft")
    print("2. Land Vehicle")
    print("3. All Types")
    
    choice = input("Enter choice (1-3): ")
    
    try:
        cursor = conn.cursor()
        
        # Case work for selecting a aircraft or a land vehicle
        if choice == '1':
            category = 'Aircraft'
            sql = """
            SELECT e.name, e.specialty, e.stock, e.price_usd 
            FROM equipment e
            WHERE e.manufacturer_id = %s AND e.equipment_category = 'Aircraft'
            ORDER BY e.name
            """
            cursor.execute(sql, (current_manufacturer_id,))
        elif choice == '2':
            category = 'Land Vehicle'
            sql = """
            SELECT e.name, e.specialty, e.stock, e.price_usd 
            FROM equipment e
            WHERE e.manufacturer_id = %s AND e.equipment_category = 'Land Vehicle'
            ORDER BY e.name
            """
            cursor.execute(sql, (current_manufacturer_id,))
        elif choice == '3':
            category = 'All'
            sql = """
            SELECT e.name, e.specialty, e.stock, e.price_usd, e.equipment_category 
            FROM equipment e
            WHERE e.manufacturer_id = %s
            ORDER BY e.equipment_category, e.name
            """
            cursor.execute(sql, (current_manufacturer_id,))
        else:
            print("Invalid choice.")
            display_by_type()
            return
            
        rows = cursor.fetchall()
        
        if not rows:
            print(f"No {category} equipment found in database.")
        else:
            print(f"\n{category} Equipment:")
            
            # If the above choice is "all", we show the category coloumn 
            if choice == '3':  
                for row in rows:
                    name, specialty, stock, price, eq_category = row
                    print(f"Name: {name} | Function: {specialty} | Stock: {stock} | Price: ${price:,.2f} | Category: {eq_category}")
            else:
                for row in rows:
                    name, specialty, stock, price = row
                    print(f"Name: {name} | Function: {specialty} | Stock: {stock} | Price: ${price:,.2f}")
                
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            print("An error occurred while retrieving equipment by type.")
            
    finally:
        cursor.close()
        
    input("\nPress Enter to return to browse menu...")
    browse_equipment()


def update_equipment():
    """
    This function allows manufacturers to update equipment details.
    The admins are allowed to add new equipment or update price 
    of existing equipment (could add more support later).
    """
    print("\n--- 2. Update Equipment ---")
    
    print("\nUpdate Equipment Options:")
    print("1. Add New Equipment")
    print("2. Update Price")
    print("3. Update Stock")
    print("4. Return to main menu")
    
    choice = input("Enter choice (1-4): ")
    
    if choice == '1':
        add_equipment()
    elif choice == '2':
        update_price()
    elif choice == '3':
        update_stock()
    elif choice == '4':
        return
    else:
        print("Invalid choice. Please try again.")
        update_equipment()

def add_equipment():
    """
    Allows manufacturers to add new equipment to the database.
    Pressing enter will return them back to the menu
    """
    print("\n--- Add Equipment ---")
    
    try:
        # Make sure we get the equ name 
        name = input("Enter equipment name: ")
        while True:
            category = input("Enter equipment category (Aircraft/Land Vehicle): ")
            # looping to provide flexibility
            if category in ['Aircraft', 'Land Vehicle']:
                break
            print("Invalid category. Please enter 'Aircraft' or 'Land Vehicle'.")
        
        specialty = input("Enter equipment function/specialty: ")
        description = input("Enter equipment description: ")
        
        # Error checking to make sure we have a valid price entered (which 
        # must be greater than 0 usd)
        while True:
            try:
                price = float(input("Enter price (USD): "))
                if price <= 0:
                    print("Price must be greater than zero.")
                else:
                    break
            except ValueError:
                print("Please enter a valid number for price.")
                
        # Make sure that they do not give negative stock (they can add 0 and 
        # then update later)
        while True:
            try:
                stock = int(input("Enter initial stock: "))
                if stock < 0:
                    print("Stock cannot be negative.")
                else:
                    break
            except ValueError:
                print("Please enter a valid number for stock.")
                
        # Confirm details (making sure to show it) before adding to database
        print("\n--- Confirm Equipment Details ---")
        print(f"Name: {name}")
        print(f"Category: {category}")
        print(f"Function: {specialty}")
        print(f"Description: {description}")
        print(f"Price: ${price:,.2f}")
        print(f"Stock: {stock}")
        
        confirm = input("\nConfirm adding this equipment? (y/n): ")
        # If they confirmed the details, we want to add it to the database
        if confirm.lower().startswith('y'):
            cursor = conn.cursor()
            
            sql = """
            INSERT INTO equipment (manufacturer_id, equipment_category, stock, 
                                  description, name, specialty, price_usd)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (current_manufacturer_id, category, stock, 
                                description, name, specialty, price))
            conn.commit()
            
            print(f"\nEquipment '{name}' added successfully!")
            
            # Making sure to get the equipment id (just to display it to the
            # admin in case they would want it and 
            # for verification purposes and help debuggin)
            cursor.execute("SELECT LAST_INSERT_ID()")
            equipment_id = cursor.fetchone()[0]
            print(f"Equipment ID: {equipment_id}")
            
        else:
            print("Equipment addition cancelled.")
    # Error handling
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            print("An error occurred while adding equipment.")
    
    input("\nPress Enter to return to update menu...")
    update_equipment()

def update_price():
    """
    Allows manufacturers to update the price of existing equipment.
    Pressing enter will return them back to the menu
    """
    print("\n--- Update Price ---")
    
    try:
        cursor = conn.cursor()
        
        # First, we wna to show all equipment from this manufacturer
        # (helpful when they are selecting a piece of equipment)
        sql = """
        SELECT equipment_id, name, price_usd 
        FROM equipment 
        WHERE manufacturer_id = %s
        ORDER BY name
        """
        cursor.execute(sql, (current_manufacturer_id,))
        equipment_list = cursor.fetchall()
        
        # If they don't have any equ, they cant update the price
        if not equipment_list:
            print("You don't have any equipment to update.")
            return
        # show all the equ
        print("\nYour Equipment:")
        for eq in equipment_list:
            eq_id, name, price = eq
            print(f"ID: {eq_id} | Name: {name} | Current Price (USD): ${price:,.2f}")
            
        # We allow the admin to enter the equipment ID to update
        while True:
            try:
                eq_id = int(input("\nEnter the ID of equipment to update (0 to cancel): "))
                if eq_id == 0:
                    print("Price update cancelled.")
                    return
                    
                # Check if this ID exists and belongs to this manufacturer
                # (just an extra check to be safe)
                found = False
                for item in equipment_list:
                    if item[0] == eq_id:
                        found = True
                        current_price = item[2]
                        equipment_name = item[1]
                        break
                        
                if found:
                    break
                print(f"Equipment with ID {eq_id} not found in your inventory.")
                
            except ValueError:
                print("Please enter a valid ID number.")
                
        # Finally, we can enter the new price (making sure it is non negative)
        while True:
            try:
                new_price = float(input(f"Enter new price for '{equipment_name}' (current: ${current_price:,.2f}): "))
                if new_price <= 0:
                    print("Price must be greater than zero.")
                else:
                    break
            except ValueError:
                print("Please enter a valid number for price.")
                
        # Confirm price update (just good practice and making a big chjange)
        print(f"\nUpdate price of '{equipment_name}' from ${current_price:,.2f} to ${new_price:,.2f}?")
        confirm = input("Confirm update? (y/n): ")
        
        if confirm.lower().startswith('y'):
            sql = """
            UPDATE equipment 
            SET price_usd = %s 
            WHERE equipment_id = %s AND manufacturer_id = %s
            """
            cursor.execute(sql, (new_price, eq_id, current_manufacturer_id))
            conn.commit()
            print(f"Price updated successfully for '{equipment_name}'.")

        else:
            print("Price update cancelled.")
    
    # Error handling
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            print("An error occurred while updating equipment price.")
    
    input("\nPress Enter to return to update menu...")
    update_equipment()

def update_stock():
    """
    Allows manufacturers to add or remove stock from existing equipment stock.
    Pressing enter will return them back to the menu
    """
    print("\n--- Update Stock ---")
    # Folloing the same logic as price just for stock
    try:
        cursor = conn.cursor()
        
        sql = """
        SELECT equipment_id, name, stock 
        FROM equipment 
        WHERE manufacturer_id = %s
        ORDER BY name
        """
        cursor.execute(sql, (current_manufacturer_id,))
        equipment_list = cursor.fetchall()
        
        if not equipment_list:
            print("You don't have any equipment to update.")
            return
            
        print("\nYour Equipment:")
        for eq in equipment_list:
            eq_id, name, stock = eq
            print(f"ID: {eq_id} | Name: {name} | Current Stock: {stock}")
            
        while True:
            try:
                eq_id = int(input("\nEnter the ID of equipment to update stock (0 to cancel): "))
                if eq_id == 0:
                    print("Stock update cancelled.")
                    return
                    
                # Check if this ID exists and belongs to this manufacturer (just 
                # robost error checking)
                found = False
                for item in equipment_list:
                    if item[0] == eq_id:
                        found = True
                        current_stock = item[2]
                        equipment_name = item[1]
                        break
                        
                if found:
                    break
                print(f"Equipment with ID {eq_id} not found in your inventory.")
                
            except ValueError:
                print("Please enter a valid ID number.")
                
        # Then, we prompt the admin if they want to add or remove stock
        # easier to seperate into case work
        print("\nUpdate stock operation:")
        print("1. Add stock")
        print("2. Remove stock")
        stock_choice = input("Enter choice (1-2): ")
        
        if stock_choice not in ['1', '2']:
            print("Invalid choice. Stock update cancelled.")
            return
            
        # Now, we add or remove stock based on what we want to do 
        while True:
            try:
                if stock_choice == '1':
                    quantity = int(input(f"Enter quantity to add to '{equipment_name}' stock: "))
                    if quantity <= 0:
                        print("Quantity must be a positive number.")
                    else:
                        break
                # Error checking and making sure they cant go below the current stock
                else: 
                    quantity = int(input(f"Enter quantity to remove from '{equipment_name}' stock: "))
                    if quantity <= 0:
                        print("Quantity must be a positive number.")
                    elif quantity > current_stock:
                        print(f"Cannot remove {quantity} units. Current stock is only {current_stock}.")
                    else:
                        break
            except ValueError:
                print("Please enter a valid number.")
                
        # Calculate new stock level (simple add and subtract)
        if stock_choice == '1':
            new_stock = current_stock + quantity
            action = "added"
        else: 
            new_stock = current_stock - quantity
            action = "removed"
            
        # Make sure they allow them to confirm 
        print(f"\nUpdate stock of '{equipment_name}' from {current_stock} to {new_stock} units?")
        print(f"({quantity} units will be {action})")
        confirm = input("Confirm update? (y/n): ")
        
        # Finally we update the stock 
        if confirm.lower().startswith('y'):
            sql = """
            UPDATE equipment 
            SET stock = %s 
            WHERE equipment_id = %s AND manufacturer_id = %s
            """
            cursor.execute(sql, (new_stock, eq_id, current_manufacturer_id))
            conn.commit()
            
            if cursor.rowcount > 0:
                print(f"Stock updated successfully for '{equipment_name}'.")
                print(f"New stock level: {new_stock} units")
            else:
                print("Update failed. Please try again.")
        else:
            print("Stock update cancelled.")
            
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            print("An error occurred while updating equipment stock.")
    
    input("\nPress Enter to return to update menu...")
    update_equipment()

def view_sales_statistics():
    """
    This function allows manufacturers to view sales statistics (total sales 
    of approved orders).
    """
    print("\n--- 3. Sales Statistics ---")
    # This could have more selections like month or something in future 
    # iterations 
    print("\nSales Statistics Options:")
    print("1. Display Equipment by Total Sales")
    print("2. Return to main menu")
    
    choice = input("Enter choice (1-2): ")
    
    if choice == '1':
        display_equipment_by_sales()
    elif choice == '2':
        return
    else:
        print("Invalid choice. Please try again.")
        view_sales_statistics()

def display_equipment_by_sales():
    """
    Displays equipment ranked by total sales. The status of the order 
    must be approved to count.
    """
    print("\n--- Equipment by Total Sales ---")
    
    try:
        cursor = conn.cursor()
        sql = """
        SELECT e.name, e.equipment_category, 
               SUM(o.order_quantity) as total_units,
               SUM(o.total_amount_usd) as total_revenue
        FROM equipment e
        LEFT JOIN orders o ON e.equipment_id = o.equipment_id
        WHERE e.manufacturer_id = %s AND o.status = 'approved'
        GROUP BY e.equipment_id
        ORDER BY total_revenue DESC
        """
        cursor.execute(sql, (current_manufacturer_id,))
        rows = cursor.fetchall()
        
        if not rows:
            print("No sales data available.")
        else:
            print("\nEquipment Sales Summary:")
            for row in rows:
                name, category, units, revenue = row
                # If there are no sales yet, make sure to set those to zero
                # (so when printing we know what is going on)
                if units is None:
                    units = 0
                    revenue = 0
                print(f"Equipment: {name} | Category: {category} | Units Sold: {units} | Total Revenue: ${revenue:,.2f}")
                
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            print("An error occurred while retrieving sales statistics.")
            
    finally:
        cursor.close()
        
    input("\nPress Enter to return to sales statistics menu...")
    view_sales_statistics()

def manage_orders():
    """
    Function that allows manufacturers to view and update order status (
    from pending to either approve, approve all or reject).
    Shows all orders and allows admin to approve or reject any order.
    """
    print("\n--- 4. Manage Orders ---")
    # Again, the autocommit like the first file to see updates live 
    # with the manufactures refresh
    conn.autocommit = True

    try:
        cursor = conn.cursor()
        
        # Get all orders for equipment manufactured by this manufacturer
        # making sure to join all the tables
        sql = """
        SELECT o.order_id, o.order_date, u.name as customer_name, 
               e.name as equipment_name, o.order_quantity, 
               o.total_amount_usd, o.status
        FROM orders o
        JOIN equipment e ON o.equipment_id = e.equipment_id
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN users u ON c.user_id = u.user_id
        WHERE e.manufacturer_id = %s
        ORDER BY o.status, o.order_date DESC
        """
        cursor.execute(sql, (current_manufacturer_id,))
        orders = cursor.fetchall()
        
        if not orders:
            print("No orders found for your equipment.")
            return
            
        # Show the orders (the pending ones are the most important so those go 
        # first)
        print("\nAll Orders (Pending First):")
        for order in orders:
            order_id, date, customer, equipment, quantity, total, status = order
            print(f"Order ID: {order_id} | Date: {date} | Customer: {customer} | Equipment: {equipment} | Quantity: {quantity} | Total: ${total} | Status: {status}")
        
        # Then, we ask the manu what order they want to update (0 will get them back to the main menu)
        order_id = input("\nEnter Order ID to update status (0 to return to main menu): ")
        if order_id == '0':
            return
            
        try:
            # Input comes in as string so convert to int
            order_id = int(order_id)
            # First, we gotta make sure the order exists
            cursor.execute("SELECT status FROM orders WHERE order_id = %s", (order_id,))
            status_result = cursor.fetchone()
            # Error handling (shoulnt happen just go to check/hope they enter a 
            # valid id)
            if not status_result:
                print(f"Order ID {order_id} not found.")
                return
                
            current_status = status_result[0]
            print(f"\nCurrent status: {current_status}")
            
            # Give them 4 options to change the order (approve, reject, approval all, 
            # or  no change)
            print("\nUpdate status to:")
            print("1. Approve")
            print("2. Reject")
            # Adding the option to approve all order using our 
            # new procedure in routines 
            print("3. Approve all pending orders")
            print("4. No change")
            
            
            choice = input("Enter choice (1-4): ")
            
            if choice == '1': 
                sql = """UPDATE orders SET status = 'approved' WHERE order_id = %s"""
                cursor.execute(sql, (order_id,))
                conn.commit()
                print(f"Order {order_id} approved.")
            elif choice == '2':
                # The trigger will handle the rejection of an order here, no
                # need to do in the python
                sql = """UPDATE orders SET status = 'rejected' WHERE order_id = %s"""
                cursor.execute(sql, (order_id,))
                conn.commit()
                print(f"Order {order_id} rejected.")
            elif choice == '3':
                cursor = conn.cursor()
                # Call the stored procedure (making sure to use the CALL command)
                cursor.execute("CALL sp_process_pending_orders(%s)", (current_manufacturer_id,))
                # Getting the result
                result = cursor.fetchone()
                if result:
                    print(result[0])
                # If there are more result sets, we have to make sure to 
                # process them (making sure to process all them and use nextset 
                # so that it skips to the next set/MySQL documentation)
                while cursor.nextset():
                    result = cursor.fetchone()
                    if result:
                        print(result[0])
                conn.commit()
                print("All pending orders processed.")

            elif choice == '4':
                print("No changes made to order status.")
            else:
                print("Invalid choice. No changes made.")
                
        except ValueError:
            print("Please enter a valid Order ID.")
            
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            print("An error occurred while managing orders.")
    finally:
        cursor.close()
        
    input("\nPress Enter to return to main menu...")

# ----------------------------------------------------------------------
# Command-Line Functionality
# ----------------------------------------------------------------------
def show_options():
    """
    This function displays options administrators can choose in the application.
    They admins have 5 options and the ability to quit
    """
    while True:
        print("\n--- Admin Main Menu ---")
        print('Military Equipment Store Admin System')
        print('What would you like to do?')
        print('  (1) - Browse equipment')
        print('  (2) - Update equipment')
        print('  (3) - View sales statistics')
        print('  (4) - Manage orders')
        print('  (5) - Logout')
        print('  (q) - Quit')
        print()
        
        ans = input('Enter an option: ')
        if ans == 'q':
            quit_ui()
        elif ans == '1':
            browse_equipment()
        elif ans == '2':
            update_equipment()
        elif ans == '3':
            view_sales_statistics()
        elif ans == '4':
            manage_orders()
        elif ans == '5':
            logged_in = logout()
            if not logged_in:
                return
        else:
            print('Unknown option.')
    
def quit_ui():
    """
    Quits the program, printing a "good bye" message to the user.
    """
    print('Good bye!')
    sys.exit(0)


def main():
    """
    Main function for starting things up.
    """
    print("Welcome to the Military Equipment Store System")
    
    # Start with login menu (and loop until they actually want to quit
    # and press 'q') 
    while True:
        if login_admin():
            break  
        else:
            # Giving the user the ability to try to log in again
            retry = input("Login failed. Press 'q' to quit or Enter to try again.")
            if retry.lower() == 'q':
                quit_ui()  
    # After we logged in, show the options they can choose from 
    show_options()



if __name__ == '__main__':
    # This conn is a global object that other functions can access.
    # You'll need to use cursor = conn.cursor() each time you are
    # about to execute a query with cursor.execute(<sqlquery>)
    conn = get_conn()
    main()