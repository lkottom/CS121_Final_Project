"""
Student name(s): Luke Kottom, Matthew Casertano 
Student email(s): lkottom@caltech.edu, mcaserta@caltech.edu

This application provides an interface for a military equipment store database 
system.
The system allows government contractors/different governments
to look at and purchase military equipment (from the manufactures supply).
The administrators will be able to manage/update inventory and process 
customer orders.
"""

import sys 
import mysql.connector
import mysql.connector.errorcode as errorcode

# Debugging flag to print errors when debugging that shouldn't be visible
# to an actual client. ***Set to False when done testing.***
DEBUG = False

# Global varibles used to track the login state and the ids
# (these will be used in lots of functions)
current_user = None
current_user_id = None
current_customer_id = None

# ----------------------------------------------------------------------
# SQL Utility Functions
# ----------------------------------------------------------------------
def get_conn():
    """"
    Returns a connected MySQL connector instance, if connection is successful.
    If unsuccessful, exits.
    """
    try:
        conn = mysql.connector.connect(
          host='localhost',
          user='military_client',
          # Find port in MAMP or MySQL Workbench GUI or with
          # SHOW VARIABLES WHERE variable_name LIKE 'port';
          port='3306',  # this may change!
          password='clientpw',
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
def login_or_create_user():
    """
    Handles the login/create account process. Prompts user if they have an 
    exisiting account. Returns True if login is successful.
    False if not successful.
    """
    # global varibles (will be used to hold user inputs)
    global current_user, current_user_id, current_customer_id

    
    # Ask the user if the have an accout
    print("\n--- Log In/Create Account ---")
    ans = input('Do you have an existing account? (y/n): ')
    
    # If they do, have them input the 'y' and get the username and password
    if ans.lower().startswith('y'):
        # Existing user path
        username = input('Enter username (your email): ')
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
                # user result (id is the 0 index of the current_user_id)
                if user_result:
                    current_user = username
                    current_user_id = user_result[0]
                    
                    # Make sure the user is a customer (just for redundency)
                    sql = "SELECT customer_id FROM customers WHERE user_id = %s"
                    cursor.execute(sql, (current_user_id,))
                    customer_result = cursor.fetchone()
                    
                    if customer_result:
                        current_customer_id = customer_result[0]
                    
                    print(f'Login successful! Welcome {username}.')
                    return True
                else:
                    print('User not found in system.')
            else:
                print('Invalid username or password.')
            # Make sure to close the cursor here
            cursor.close()
            return False
        # Error handling (doing exactly how it was given)
        except mysql.connector.Error as err:
            if DEBUG:
                sys.stderr(err)
                sys.exit(1)
            else:
                sys.stderr.write('An error occurred when logging in\n')
                return
    
    elif ans.lower().startswith('n'):
        # If answer is no, we need to create a new user
        return create_new_user()
    # Otherwise, prompt the user to choose again
    else:
        print("Invalid choice. Please try again.")
        return False

def create_new_user():
    """
    Creates a new user account that will be a customer. Prompts for a username, 
    the password, name, and country. 
    Returns True if account creation is successful. 
    False if not successful.
    """
    print("\n--- Create Account ---")
    # the prompting of everything needed for our table
    username = input("Enter email (will be your username): ")
    password = input("Create password: ")
    name = input("Enter your full name: ")
    country = input("Enter your country: ")

    try:
        cursor = conn.cursor()
        # First, we want add the user_info for authentication
        # Using the CALL here to execute a stored MySQL procedure
        sql = "CALL sp_add_user(%s, %s, %s, %s)"
        cursor.execute(sql, (name, username, country, password))
        # Making sure to commit/finalize the adding of the user
        conn.commit()

        # get the id (auto increment) of the last row that was inserted 
        # (which would be the new account just created)
        # Found this in the offical MySQL docs and is very useful for pulling 
        # the last user_id entered
        cursor.execute("SELECT LAST_INSERT_ID()")
        user_id = cursor.fetchone()[0]

        # Now, insert into the customers table using the retrieved user_id
        sql = "INSERT INTO customers (user_id, is_verified) VALUES (%s, TRUE)"
        cursor.execute(sql, (user_id,))
        # Commit the changes (make the finalized in the table) 
        conn.commit()
        # Printing statements to help sepcify success
        print("Account created successfully!")
        print("Please login again to continue")
        cursor.close()
        return login_or_create_user()
    
    # Error handling
    except mysql.connector.Error as err:
            if DEBUG:
                sys.stderr(err)
                sys.exit(1)
            else:
                sys.stderr.write('An error occurred when creating a new user\n')
                return False
            
   

def logout():
    """
    Logs out the current user and returns to the login screen.
    Returns false if not logged in
    """
    global current_user, current_user_id, current_customer_id
    
    if current_user:
        print(f"Logging out user: {current_user}")
        current_user = None
        current_user_id = None
        current_customer_id = None
        
        # Then, we return to the login screen
        return login_or_create_user()
    else:
        print("No user is currently logged in.")
        return False

# ----------------------------------------------------------------------
# Functions for Command-Line Options/Query Execution
# ----------------------------------------------------------------------

def browse_equipment():
    """
    This function shows available military equipment. It filters by type
    (Aircraft or Land Vehicle) or can display all equipment. The results 
    will be sorted by name.
    """
    print("\n--- 1. Browse Equipment ---")
    valid_options = ['aircraft', 'vehicle', 'all']
    # Make sure the user chooses the right option (looping to give them 
    # the flexibility to enter again of they did it wrong)
    while True:
        ans = input('Filter by type? (aircraft/vehicle/all): ').lower()
        if ans in valid_options:
            break  
        print("Invalid input. Please enter 'aircraft', 'vehicle', or 'all'.")


    # Sql queries that join tables and return the right result (mostly copy and 
    # paste with small changes )
    if ans == 'aircraft':
        sql = """
        SELECT e.name, e.specialty AS role, e.price_usd AS price, u.name AS manufacturer 
        FROM equipment e
        JOIN manufacturers m ON e.manufacturer_id = m.manufacturer_id
        JOIN users u ON m.user_id = u.user_id
        WHERE e.equipment_category = 'Aircraft'
        ORDER BY e.name
        """
    elif ans == 'vehicle':
        sql = """
        SELECT e.name, e.specialty AS role, e.price_usd AS price, u.name AS manufacturer 
        FROM equipment e
        JOIN manufacturers m ON e.manufacturer_id = m.manufacturer_id
        JOIN users u ON m.user_id = u.user_id
        WHERE e.equipment_category = 'Land Vehicle'
        ORDER BY e.name
        """
    else:
        sql = """
        SELECT e.name, e.specialty AS role, e.price_usd AS price, u.name AS manufacturer 
        FROM equipment e
        JOIN manufacturers m ON e.manufacturer_id = m.manufacturer_id
        JOIN users u ON m.user_id = u.user_id
        ORDER BY e.name
        """
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        # Get all the rows (because we want to show all the equp)
        rows = cursor.fetchall()
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr.write('An error occurred when searching for available equipment.\n')
            return
    # Make sure we get a result
    if not rows: 
        print('No results found.')
    else:
        print("\n--- Display Equipment List ---")
        if ans == 'aircraft':
            print('Aircraft equipment in the database:')
        elif ans == 'vehicle':
            print('Land vehicle equipment in the database:')
        else:
            print('All equipment in the database:')

        # Displaying the rows to the users (could make this look nicer later) 
        for row in rows:
            name, role, price, manufacturer = row
            print(f"Equipment Name: {name} | Role: {role} | Price: ${price:,.2f} | Manufacturer: {manufacturer}")

    # Now, we want to give the user to option ot either place and order 
    # or return to the main menu and select another option (by choosing 1 or 2)
    while True:
        print("\nOptions:")
        print("1. Place new order")
        print("2. Return to main menu")
        choice = input("Enter your choice (1-2): ")
        if choice == '1':
            place_new_order()
            break
        elif choice == '2':
            return
        else:
            print("Invalid choice. Please try again.")

def place_new_order():
    """
    Allows verified customers to place orders for equipment.
    """
    global current_customer_id
    print("\n--- 2. Place New Order ---")

    # Using our view that will show all the available equ and stock
    # (we created this view in the setup)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT equipment_id, name, stock, price_usd, manufacturer FROM available_equipment ORDER BY name")
        equipment_list = cursor.fetchall()
        
        # Error in case there is no equipment to buy (which will likely not 
        # happend but is smart to check for)
        if not equipment_list:
            print("No equipment available for order.")
            return
        else:
            print("\nAvailable Equipment:")
            for eq in equipment_list:
                eq_id, name, stock, price, manufacturer = eq
                print(f"ID: {eq_id} | Name: {name} | Stock: {stock}| Price: ${price:,.2f} | Manufacturer: {manufacturer}")
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr.write('An error occurred when viewing equipment')
            return

    # Enter the equipment id that the user wants to buy
    print("\n--- Select Equipment ---")
    equipment_name = input('Enter equipment name to order (or Enter to exit): ')
    
    try:
        cursor = conn.cursor()
        # Getting the equipment details in sql
        sql = """
            SELECT e.equipment_id, e.name, e.price_usd, e.stock, u.name AS manufacturer
            FROM equipment e
            JOIN manufacturers m ON e.manufacturer_id = m.manufacturer_id
            JOIN users u ON m.user_id = u.user_id
            WHERE e.name = %s
            """
        cursor.execute(sql, (equipment_name,))
        # Get the row
        equipment = cursor.fetchone()
        
        if not equipment:
            print(f"Equipment with name '{equipment_name}' not found.")
            return
        
        # A tuple of the id, name, price, stock, and manutacturer    
        eq_id, name, price, stock, manufacturer = equipment
        
        # If there is no stock, say so
        if stock <= 0:
            print(f"Sorry, {name} is out of stock.")
            return
        
        # Enter quantity (making sure we tell the max availible)
        print("\n---Enter Quantity ---")
        quantity_str = input(f'Enter quantity to order (max {stock}): ')
        
        try:
            # Convert to an int (because input is a string)
            quantity = int(quantity_str)
            if quantity <= 0:
                print("Quantity must be a greater than 0.")
                return
            # Check if quantity is in stock (again, using a view we set up)
            print("\n--- Check if Quantity in Stock ---")
            sql = """SELECT check_equipment_availability(%s, %s)"""
            cursor.execute(sql, (eq_id, quantity))
            is_available = cursor.fetchone()[0]
            # If it is 0, there means there is not enought stock left 
            if is_available == 0:  
                print(f"Insufficient stock. Only {stock} units available.")
                # Allow the customer to have the option to choose less items
                # (the max that is in stock because they went over ->
                # most likely option)
                quantity_retry = input(f"Would you like to order {stock} units instead? (y/n): ")
                if quantity_retry.lower().startswith('y'):
                    quantity = stock
                else:
                    return
            
            # Calculate total amount (this is in usd)
            total_amount = quantity * price
            
            # Confirm order details with print statements
            print("\n--- Confirm Order Details ---")
            print(f"Equipment: {name}")
            print(f"Manufacturer: {manufacturer}")
            print(f"Quantity: {quantity}")
            print(f"Price per unit: ${price:,.2f}")
            print(f"Total amount: ${total_amount:,.2f}")

            # Make sure they want to confirm the order
            confirm = input("Confirm order? (y/n): ")
            
            if confirm.lower().startswith('y'):
                # After they confirmed, add the orcer to the database
                sql = """
                    INSERT INTO orders (customer_id, equipment_id, order_quantity, total_amount_usd)
                    VALUES (%s, %s, %s, %s)
                    """
                cursor.execute(sql, (current_customer_id, eq_id, quantity, total_amount))
                
                # Making sure we update the equpment stock (this can be reverted 
                # if the admin rejects the order)
                sql = """
                    UPDATE equipment 
                    SET stock = stock - %s 
                    WHERE equipment_id = %s
                    """
                cursor.execute(sql, (quantity, eq_id))
                # Commit the changes
                conn.commit()
                print("Order placed successfully!")
                
                # Getting the order ID, so that we can report it
                # it to the customer later
                sql = """
                SELECT order_id FROM orders 
                WHERE customer_id = %s 
                ORDER BY order_date DESC
                """
                cursor.execute(sql, (current_customer_id,))
                # Get the result so we can process later
                order_result = cursor.fetchone()
                
                if order_result:
                    # The id is stored in the 0th index
                    print(f"Your order ID is: {order_result[0]}")
                # Making sure no unread resutls remain (we can
                # discard them -> was an error of unread resutls but this fixed
                # it)
                cursor.fetchall()
            
                print("Thank you for your order!")
                # Now, we want to give the user to option t0 either place another order 
                # or return to the main menu and select another option (by choosing 1 or 2)
                place_another = True
                while place_another:
                    print("\nOptions:")
                    print("1. Place another order")
                    print("2. Return to main menu")
                    choice = input("Enter your choice (1-2): ")
                    if choice == '1':
                        break 
                    elif choice == '2':
                        place_another = False 
                    else:
                        print("Invalid choice. Please try again.")
                # If the place another flag is True, reloop
                if place_another:
                    return place_new_order()
                return
            
            else:
                print("Order cancelled.")
                
        except ValueError:
            print("Please enter a valid number for quantity.")
    # Error handling 
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            print("An error occurred while processing your order.")
    finally:
        cursor.close()

def view_order_history():
    """
    Allows customers to view their order history. They can also dynamically 
    check if the admin has approved or rejected their order when they refresh 
    the their order history
    """
    global current_customer_id

    # THis allows for dynamic updating so that the user can refresh and 
    # see that there order is all good and either approved or rejectd 
    # From the MySQL docs and after some testing it auto updates which is 
    # what i was looking for
    conn.autocommit = True

    while True:
        print("\n--- 3. View Order History ---")
        
        try:
            # Get the spending data (using our function in routines)
            cursor = conn.cursor()
            cursor.execute("SELECT calculate_customer_spending(%s)", (current_customer_id,))
            total_spending = cursor.fetchone()[0]
            print(f"Your total approved order spending: ${total_spending:.2f}\n")
            
            # Get the order hist with this query 
            sql = """
                SELECT order_id, order_date, equipment_name, order_quantity, 
                price_usd, total_cost, status
                FROM customer_order_history
                WHERE customer_id = %s
                ORDER BY order_date DESC
                """
            cursor.execute(sql, (current_customer_id,))
            rows = cursor.fetchall()
            
            if not rows:
                print('You have no order history.')
            else:
                print('Your order history (newest first):')
                # Displaying the order history in the format we have been doing 
                for row in rows:
                    (order_id, order_date, equipment, quantity, _, total, status) = row
                    print(f"Order ID: {order_id} | Order Date: {order_date} | Equipment name: {equipment} | Quantity: {quantity} | Total: ${total} | Status: {status}")
            
            cursor.close() 
        # Error handling for debuggin 
        except mysql.connector.Error as err:
            if DEBUG:
                sys.stderr(err)
                sys.exit(1)
            else:
                print("An error occurred when retrieving order history.") 
        
        # Options after displaying the order history (giving the user the 
        # ability to refresh the data)
        print("\nOptions:")
        print("1. Refresh order history")
        print("2. Return to main menu")
        choice = input("Enter choice (1-2): ")
        
        if choice == "1":
            print("\nRefreshing order history...\n")
            # We want to refresh/restart the loop and get fresh data
            continue
        else:
            break


# ----------------------------------------------------------------------
# Command-Line Functionality
# ----------------------------------------------------------------------
def show_options():
    """
    This function displays options users can choose in the application. The 
    user has 4 options and the ability to quit. 
    """
    # Based of our flow diagram (making sure to keep all the options that we 
    # indicated)
    while True:
        print("\n--- Main Menu ---")
        print('Military Equipment Store System')
        print('What would you like to do?')
        print('  (1) - Browse available equipment')
        print('  (2) - Place new order')
        print('  (3) - View order history')
        print('  (4) - Logout')
        print('  (q) - Quit')
        print()
        
        ans = input('Enter an option: ')
        if ans == 'q':
            quit_ui()
        elif ans == '1':
            browse_equipment()
        elif ans == '2':
            place_new_order()
        elif ans == '3':
            view_order_history()
        elif ans == '4':
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
        if login_or_create_user():
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
