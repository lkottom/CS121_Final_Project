# CS 121 Final Project: Military Equipment Store Database System

## Student Information
**Student Names:** Luke Kottom, Matthew Casertano  
**Student Emails:** lkottom@caltech.edu, mcaserta@caltech.edu

## Project Description
This project implements a database system for a military equipment store. 
It allows allowing for clients (US government contractors and foreign goverments/military branches) to browse and 
purchase military equipment from manufacturers. The database system consists of two applications:


1. **Client Application (`app_client.py`)**: For customers to create accounts, browse equipment, place orders, and view order history (which is dynamically updated as manufacturers approve/reject orders).
2. **Admin Application (`app_admin.py`)**: For manufacturers to view and manage inventory, update equipment details (such as stock and price), view sales statistics, and process (approve or reject) customer orders.

## Data Source
The data for this project includes information about military equipment, manufacturers, customers, and orders all scraped from wikipedia. The equipment data is based on real-world military vehicles and aircraft with their specifications. The scraping code can found in the `data/` directory of this project. The customers and orders that are populated in the tables are generated by ChatGTP.

Wikipedia links:
1. Land Vehicles: https://en.wikipedia.org/wiki/List_of_equipment_of_the_United_States_Army
2. Aircraft: https://en.wikipedia.org/wiki/List_of_active_United_States_military_aircraft

## Setup Instructions

### Database Setup
1. Open MySQL Command Line Client (if installed to root user run):
    ```bash
    mysql --local-infile=1 -u root -p
    ```
2. Create the database:
   ```sql
   CREATE DATABASE military_db;
   USE military_db;
   ```
3. Execute the following SQL scripts in order:
   ```
   source setup.sql;
   source load-data.sql;
   source setup-passwords.sql;
   source setup-routines.sql;
   source grant-permissions.sql;
   quit;
   ```

## Running the Applications

### Client Application (For Customers)
1. Open a terminal/command prompt
2. Navigate to the directory containing the files
3. Run the command:
   ```
   python3 app_client.py
   ```
4. You can either create a new customer account or log in with an existing account from the list below with password "password123"
5. As a customer, you can:
   - Browse available equipment
   - Place orders for equipment
   - View your order history and order status (dynamically updates as admin approves orders)

## Customer Accounts for Testing
All customer accounts use the password: **password123**

- U.S. Army: customer68@example.com
- U.S. Navy: customer69@example.com
- U.S. Air Force: customer70@example.com
- U.S. Marines: customer71@example.com
- U.S. Coast Guard: customer72@example.com
- U.S. Space Force: customer73@example.com
- U.K. Army: customer74@example.com
- U.K. Navy: customer75@example.com
- U.K. Air Force: customer76@example.com
- U.K. Marines: customer77@example.com
- U.K. Coast Guard: customer78@example.com
- U.K. Space Force: customer79@example.com
- Germany Army: customer80@example.com
- Germany Navy: customer81@example.com
- Germany Air Force: customer82@example.com


### Admin Application (For Manufacturers)
1. Open a terminal/command prompt
2. Navigate to the directory containing the files
3. Run the command:
   ```
   python3 app_admin.py
   ```
4. Login using one of the manufacturer emails from the list below with password "password123"
5. As a manufacturer, you can:
   - Browse your equipment inventory
   - Update prices and stock levels
   - Add new equipment
   - View sales statistics
   - Approve or reject customer orders


## Manufacturer Accounts for Testing
All manufacturer/admin accounts use the password: **password123**

These accounts can only log in to the admin application (`app_admin.py`):

- Fairchild: fairchild@example.com  
- Sierra Nevada Corporation: sierranevadacorporation@example.com  
- Lockheed Martin: lockheedmartin@example.com  
- Rockwell International: rockwellinternational@example.com  
- Northrop Grumman: northropgrumman@example.com  
- Boeing: boeing@example.com  
- Beechcraft: beechcraft@example.com  
- De Havilland Canada: dehavillandcanada@example.com  
- McDonnell Douglas & Boeing: mcdonnelldouglas&boeing@example.com  
- Learjet: learjet@example.com  
- Gulfstream: gulfstream@example.com  
- CASA: casa@example.com  
- Bell & Boeing: bell&boeing@example.com  
- McDonnell Douglas: mcdonnelldouglas@example.com  
- General Dynamics: generaldynamics@example.com  
- Sikorsky: sikorsky@example.com  
- AgustaWestland: agustawestland@example.com  
- General Atomics: generalatomics@example.com  
- Composite Engineering: compositeengineering@example.com  
- Bombardier: bombardier@example.com  
- AeroVironment: aerovironment@example.com  
- DZYNE Technologies: dzynetechnologies@example.com  
- Raytheon: raytheon@example.com  
- Cessna: cessna@example.com  
- Cirrus: cirrus@example.com  
- Raytheon & Beechcraft: raytheon&beechcraft@example.com  
- Boeing & Saab: boeing&saab@example.com  
- Bell: bell@example.com  
- Pilatus: pilatus@example.com  
- Alenia Aeronautica: aleniaaeronautica@example.com  
- Mil Moscow Helicopter Plant: milmoscowhelicopterplant@example.com  
- Airbus Eurocopter: airbuseurocopter@example.com  
- Prioria Robotics: prioriarobotics@example.com  
- MMIST: mmist@example.com  
- FLIR: flir@example.com  
- Airbus: airbus@example.com  
- Bell Boeing: bellboeing@example.com  
- Kaman: kaman@example.com  
- Boeing Insitu: boeinginsitu@example.com  
- Skydio: skydio@example.com  
- McDonnell Douglas, Northrop Grumman & Boeing: mcdonnelldouglas,northropgrumman&boeing@example.com  
- BAE Systems: baesystems@example.com  
- Various: various@example.com  
- Elbit Systems: elbitsystems@example.com  
- L3Harris: l3harris@example.com  
- Textron: textron@example.com  
- Navistar: navistar@example.com  
- Oshkosh Defense: oshkoshdefense@example.com  
- Force Protection: forceprotection@example.com  
- AM General: amgeneral@example.com  
- GM Defense: gmdefense@example.com  
- Polaris: polaris@example.com  
- Hagglunds: hagglunds@example.com  
- Caterpillar: caterpillar@example.com  
- Aardvark Clear Mine Ltd: aardvarkclearmineltd@example.com  
- DCD Protected Mobility: dcdprotectedmobility@example.com  
- Hydrema: hydrema@example.com  

## Application Workflow

### Admin (Manufacturer) Workflow
1. Log in to the admin application
2. Browse equipment inventory
3. Update equipment details or add new equipment
4. View sales statistics
5. Manage orders (approve or reject)

### Client (Customer) Workflow
1. Create an account or log in
2. Browse available equipment
3. Place orders for equipment
4. View order history to check order status

## Notes
- **Important:** A complete list of all equipment available for manufacturing is provided in the PDF file: `equipment_to_manufacturer.pdf`. This provides the data on which manufacturer makes which piece of equipment (useful for referencing which manufacturer to log in as to approve a specific order) 
- Administrator accounts are pre-configured in the database and cannot be created manually (can add this functionality in future iterations).
- All passwords are encrypted using MySQL's password hashing functions.
- When an order is rejected, the system automatically returns the stock to the inventory through a database trigger that we made.
- The system makes sure to set up and check for proper authentication controls to make sure the security of the database is strong.

## File Structure
- `app_client.py`: Client-side application for customers
- `app_admin.py`: Admin-side application for manufacturers
- `setup.sql`: Creates the database tables
- `load-data.sql.sql`: Populates the database with sample data
- `setup-passwords.sql`: Sets up password hashing and authentication functions
- `setup-routines.sql`: Creates stored procedures, functions, and triggers
- `grant-permissions.sql`: Give the client and admin proper permissions

## Future Work

If we had more time, we would focus on the following improvements:

- **User Verification System**: We would like to implement a verification process requiring official government credentials to ensure that only legitimate users can create accounts and access the platform. Our current system automatically verifies every user (after they create an account) and this addition would improve security. 

- **Expanding the Web Scraper**: We also would like to extend our web scraper to also pull images of military equipment from Wikipedia. These images could then be placed into our database and displayed in the application. We think this would be a very neat addition and would be helpful when selecting the right equipment.

- **Enhanced Sales Analytics**: We also want to implement improved sales statistics features by providing more detailed breakdowns for the sales by each company (in the admin application). Right now we are only displaying total say and this feature would all manufacturers to view sales by specific timeframes such as last month, week, or day. This option would allow them to have better data and make better predictions on what equipment is doing well. 

