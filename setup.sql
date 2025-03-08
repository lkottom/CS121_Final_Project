DROP VIEW IF EXISTS available_equipment;
DROP VIEW IF EXISTS customer_order_history;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS equipment;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS manufacturers;
DROP TABLE IF EXISTS users;


-- Represents a user uniquely identified by a user_id with
-- their personal information and login credentials
-- Requires all  non-null values.
CREATE TABLE users (
    -- Auto-incrementing identifier for each user
    user_id         INT AUTO_INCREMENT,
    -- Full name of the user, e.g. "John Doe" or "Sarah Smart"
    name            VARCHAR(100) NOT NULL,
    -- Email address used for contact and as username, 
    -- e.g. "customer83@example.com"
    contact_email   VARCHAR(100) NOT NULL,
    -- Country of residence for the user, e.g. "U.S." or "Mexico"
    country         VARCHAR(50) NOT NULL,
    -- Random salt value for password security
    salt            CHAR(8)    NOT NULL,
    -- SHA-256 hashed password with salt
    password_hash   BINARY(64) NOT NULL,
    PRIMARY KEY (user_id)
);

-- Represents a manufacturer uniquely identified by a manufacturer_id with
-- their corresponding user information and security clearance level
-- A subclass of the users table
CREATE TABLE manufacturers (
    -- Auto-incrementing identifier for each manufacturer
    manufacturer_id INT AUTO_INCREMENT,
    -- Reference to the associated user record, e.g. user_id "2"
    user_id         INT NOT NULL,
    -- Security clearance level for the manufacturer, 
    -- e.g. "Top Secret" or "Confidential", may be NULL
    clearance_lvl   VARCHAR(50),
    PRIMARY KEY (manufacturer_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
    ON UPDATE CASCADE ON DELETE CASCADE
);

-- Represents a customer uniquely identified by a customer_id with
-- their corresponding user information and verification status
-- A subclass of the users table
CREATE TABLE customers (
    -- Auto-incrementing identifier for each customer
    customer_id     INT AUTO_INCREMENT,
    -- Reference to the associated user record, e.g. user_id "15"
    user_id         INT NOT NULL,
    -- Flag indicating whether the customer has been verified, 
    -- e.g. TRUE or FALSE
    is_verified     BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (customer_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
    ON UPDATE CASCADE ON DELETE CASCADE
);


-- Represents military equipment uniquely identified by an equipment_id with
-- its specifications, inventory information, and pricing details
-- Categorized as either Aircraft or Land Vehicle
CREATE TABLE equipment (
    -- Auto-incrementing identifier for each equipment item
    equipment_id        INT AUTO_INCREMENT,
    -- Refrence to the manufacturer who produces this equipment, 
    -- e.g. manufacturer_id 7
    manufacturer_id     INT NOT NULL,
    -- Category of military equipment, either 'Aircraft' or 'Land Vehicle'
    -- can be increased in the future
    equipment_category  ENUM('Aircraft', 'Land Vehicle') NOT NULL,
    -- Number of unit currently available in inventory, e.g. 15
    stock               INT NOT NULL DEFAULT 0,
    -- Detailed description of the equipment's capabilities and features
    description         VARCHAR(1000),
    -- Name of the equipment model, e.g. "A-10C Thunderbolt II" 
    -- or "A-29C Super Tucano"
    name                VARCHAR(100) NOT NULL,
    -- Primary function or role of the equipment, 
    -- e.g. "CAS / Attack" or "Research and development"
    specialty           VARCHAR(100),
    -- Price per unit in US Dollars, e.g. 131059034.00
    price_usd           DECIMAL(15,2) NOT NULL,
    PRIMARY KEY (equipment_id),
    FOREIGN KEY (manufacturer_id) REFERENCES manufacturers(manufacturer_id)
    ON UPDATE CASCADE ON DELETE RESTRICT
);

-- Represents customer orders uniquely identified by an order_id with
-- details about the purchased equipment, quantities, pricing, 
-- and approval status
-- All orders start with 'pending' status and require manufacturer approval
CREATE TABLE orders (
    -- Auto-incrementing identifier for each order
    order_id            INT AUTO_INCREMENT,
    -- Reference to the customer who placed the order, e.g. customer_id 33
    customer_id         INT NOT NULL,
    -- Reference to the equipment being ordered, e.g. equipment_id 125
    equipment_id        INT NOT NULL,
    -- Number of units being ordered, e.g. 49
    order_quantity      INT NOT NULL,
    -- Date and time when the order was placed, automaticaly set to current 
    -- time, e.g. 2024-11-16 17:59:38
    order_date          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- Current status of the order: 'pending', 'approved', or 'rejected'
    status              ENUM('pending', 'approved', 'rejected') 
                        DEFAULT 'pending',
    -- Total cost of the order in US Dollars, e.g. 1911437913.00
    total_amount_usd    DECIMAL(15,2) NOT NULL,
    PRIMARY KEY (order_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (equipment_id) REFERENCES equipment(equipment_id)
    ON UPDATE CASCADE ON DELETE RESTRICT
);

-- Adding indexes as specifed in the spec (with an explination of why we 
-- think that this is a good index)

-- this is useful and used in any the app_client.py 
-- place_new_order() function searches for equipment by name
-- ....WHERE e.name = %s

-- and app_admin.py display_details()
-- ....WHERE e.manufacturer_id = %s AND e.name LIKE %s

-- This index is helpful because equip names are 
-- probably be searched frequently by clients/admins

CREATE INDEX idx_equipment_name ON equipment(name);


-- This index will be used for faster filtering by status
-- app_admin.py manage_orders()
-- ...ORDER BY o.status, ...
-- and display_equipment_by_sales()
-- ...WHERE e.manufacturer_id = %s AND o.status = 'approved'..

-- This index is helpful because orders table often filters by status 
-- (pending, approved, rejected)
-- Also, sp_process_pending_orders would benefit
-- from quickly identifying pending orders (speed increase)
CREATE INDEX idx_orders_status ON orders(status);


##### HELPFUL VIEWS (I just created because i thought we may need to have in 
# the final project)

# This view shows available_equipment (stock > 0)
CREATE VIEW available_equipment AS
    SELECT e.equipment_id, e.name, e.stock, e.price_usd, u.name AS manufacturer
    FROM equipment e
    JOIN manufacturers m ON e.manufacturer_id = m.manufacturer_id
    JOIN users u ON m.user_id = u.user_id
WHERE e.stock > 0;

# This view helps to simplifing showing past orders
CREATE VIEW customer_order_history AS
SELECT 
    o.order_id,
    o.order_date,
    o.customer_id,
    e.name AS equipment_name,
    o.order_quantity,
    e.price_usd,
    (o.order_quantity * e.price_usd) AS total_cost,
    o.status
FROM orders o
JOIN equipment e ON o.equipment_id = e.equipment_id;

-- EXPLAIN SELECT * FROM equipment WHERE price_usd BETWEEN 10000000 AND 50000000;

-- CREATE INDEX idx_equipment_price ON equipment(price_usd);

-- EXPLAIN SELECT * FROM equipment WHERE price_usd BETWEEN 10000000 AND 50000000;