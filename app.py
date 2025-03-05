"""
TODO: Student name(s): Luke Kottom, Matthew Casertano 
TODO: Student email(s): lkottom@caltech.edu, mcaserta@caltech.edu

This application provides an interface for a military equipment store database 
system.
The system allows government contractors/different governments
to look at and purchase military equipment (from the manufactures supply).
The administrators will be able to manage/update inventory and process 
customer orders.

QUESTION: I am wondering what I should do for the login part of this program?
I was thinking maybe having like the client/buyers having a password and create
it when the log in for the first time and then check the clients email and 
password everytime they log in. Kinda similar for admins and maybe include like 
an option to log in as an admin or a client. Would I add this to the login 
portion and how hard would this logic be to implement?? I could also include 
a password attribute in the customers table and then I was thinking of making 
the admins be the manufactures (and maybe add a password attribute to that 
table as well). Any feedback on these ideas are greatly appreciated, thank u!!!

"""
# TODO: Make sure you have these installed with pip3 if needed
import sys  # to print error messages to sys.stderr
import mysql.connector
# To get error codes from the connector, useful for user-friendly
# error-handling
import mysql.connector.errorcode as errorcode

# Debugging flag to print errors when debugging that shouldn't be visible
# to an actual client. ***Set to False when done testing.***
DEBUG = True

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
          user='appadmin',
          # Find port in MAMP or MySQL Workbench GUI or with
          # SHOW VARIABLES WHERE variable_name LIKE 'port';
          port='3306',  # this may change!
          password='',
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
            sys.stderr('Incorrect username or password when connecting to DB.')
        elif err.errno == errorcode.ER_BAD_DB_ERROR and DEBUG:
            sys.stderr('Database does not exist.')
        elif DEBUG:
            sys.stderr(err)
        else:
            # A fine catchall client-facing message.
            sys.stderr('An error occurred, please contact the administrator.')
        sys.exit(1)

# ----------------------------------------------------------------------
# Functions for Command-Line Options/Query Execution
# ----------------------------------------------------------------------
def browse_equipment():
    """
    This function shows available military equipment. It filters by type 
    or can display all equipment (Aircraft or Land Vehicle).
    """
    ans = input('Filter by type? (aircraft/vehicle/no): ').lower()
    # Will need to utalize this cursor during the actual SQl I think
    cursor = conn.cursor()
    
    if ans.startswith('a'):
        sql = "SELECT name, role, price FROM equipment WHERE type = 'Aircraft'"
    elif ans.startswith('v'):
        sql = "SELECT name, role, price FROM equipment WHERE type = 'Land Vehicle'"
    else:
        sql = "SELECT name, role, price FROM equipment"
    
    # This is where we have to implement the actual SQL
    print("Browse equipment functionality to be implemented")

def search_by_manufacturer():
    """
    Allows the client to search for equipment from a specific manufacturer.
    (Might need to add a list to choose from we shall see how many companies 
    we get)
    """
    manufacturer = input('Enter manufacturer name: ')
    # This is where we have to implement the actual SQL
    print("Search by manufacturer functionality to be implemented")

def place_order():
    """
    Allows verified customers to place orders for equipment.
    Needs customer verification and to check if the equipment 
    is available (enought in stock)
    When called, this will create a new order in ORDERS database if successful
    """
    # This is where we have to implement the actual SQL
    print("Order placement functionality to be implemented")

# ADMIN OPTIONS 
def view_all_orders():
    """
    Displays all orders in the system with their status and details.
    The SQL implementation will join ORDERS table with customers 
    (Which will allow admins to see the orders)
    """
    # Will need to utalize this cursor during the actual SQl I think
    # Views persist - past the session
    # Anything that outputs - I would specify the information output
    # e.g., idea of order, name of order, name  of equipment, quantity of order
    # once you catch anything that you don't need
    cursor = conn.cursor()
    sql = """
        SELECT o.order_id, c.name, e.name, o.quantity, o.status, o.total_amount
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN equipment e ON o.equipment_id = e.equipment_id
        ORDER BY o.order_date DESC
    """
    print("View all orders functionality to be implemented")

def update_inventory():
    """
    Allows admin to update inventory count for equipment.
    Will updates inventory_count in EQUIPMENT table
    """
    equipment_id = input('Enter equipment ID: ')
    new_count = input('Enter new inventory count: ')
    cursor = conn.cursor()
    sql = """
        UPDATE equipment
        SET inventory_count = %s
        WHERE equipment_id = %s
    """
    print("Update inventory functionality to be implemented")

def add_new_equipment():
    """
    Allows admin to add new equipment to the database
    WILL insert a new row into equipment table
    """
    print("-- Add New Equipment --")
    print("Enter equipment details:")
    # Implementation will collect these fields (att in equipment table)
    fields = ['name','manufacturer_id','type','role','inventory_count',
        'price','description']
    print("Add new equipment functionality to be implemented") 


# ----------------------------------------------------------------------
# Functions for Logging Users In
# ----------------------------------------------------------------------

# This is where i need some help/recommendations

# ----------------------------------------------------------------------
# Command-Line Functionality
# ----------------------------------------------------------------------
def show_options():
    """
    This function displays options users can choose in the application
    """
    # Based of my flow diagram
    print('Military Equipment Store System')
    print('What would you like to do?')
    print('  (b) - Browse available equipment')
    print('  (s) - Search by manufacturer')
    print('  (o) - Place an order')
    print('  (q) - Quit')
    print()
    while True:
        ans = input('Enter an option: ').lower()
        if ans == 'q':
            quit_ui()
        elif ans == 'b':
            browse_equipment()
        elif ans == 's':
            search_by_manufacturer()
        elif ans == 'o':
            place_order()
        else:
            print('Unknown option.')
        # Maybe add more functionality possibly 
        # (probably will have more queries)

# I am choosing to do admins in the same file. I feel like this is 
# going to make more sense and above is the admin options availible (probably 
# should have more)
def show_admin_options():
    """
    Displays options specific for administrators
    """
    print('Administrator Menu')
    print('  (v) - View all orders')
    print('  (u) - Update inventory')
    print('  (a) - Add new equipment')
    print('  (q) - Quit')
    print()
    while True:
        ans = input('Enter an option: ').lower()
        if ans == 'q':
            quit_ui()
        elif ans == 'v':
            view_all_orders()
        elif ans == 'u':
            update_inventory()
        elif ans == 'a':
            add_new_equipment()
        else:
            print('Invalid option. Please try again.')

def quit_ui():
    """
    Quits the program, printing a good bye message to the user.
    """
    print('Good bye!')
    exit()


def main():
    """
    Main function for starting things up.
    """
    show_options()


if __name__ == '__main__':
    # This conn is a global object that other functions can access.
    # You'll need to use cursor = conn.cursor() each time you are
    # about to execute a query with cursor.execute(<sqlquery>)
    conn = get_conn()
    main()
