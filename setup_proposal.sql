-- DROP TABLE IF EXISTS orders;
-- DROP TABLE IF EXISTS equipment;
-- DROP TABLE IF EXISTS customers;
-- DROP TABLE IF EXISTS manufacturers;

-- -- Manufacturers table (this would be like Lockheed Martin, Boeing)
-- CREATE TABLE manufacturers (
--     manufacturer_id   INT AUTO_INCREMENT,
--     name             VARCHAR(100) NOT NULL,
--     country          VARCHAR(50) NOT NULL,
--     PRIMARY KEY (manufacturer_id)
-- );

-- -- Customers table (for example: government contractors, agencies)
-- CREATE TABLE customers (
--     customer_id      INT AUTO_INCREMENT,
--     name            VARCHAR(100) NOT NULL,
--     email           VARCHAR(100) NOT NULL,
--     country         VARCHAR(50) NOT NULL,
--     is_verified     BOOLEAN DEFAULT FALSE,
--     PRIMARY KEY (customer_id)
-- );

-- -- Military equipment table (Will be like F16/hummvee)
-- CREATE TABLE equipment (
--     equipment_id     INT AUTO_INCREMENT,
--     manufacturer_id  INT NOT NULL,
--     name            VARCHAR(100) NOT NULL,
--     type            ENUM('Aircraft', 'Land Vehicle') NOT NULL,
--     role            VARCHAR(100) NOT NULL,
--     year_introduced INT,
--     inventory_count INT NOT NULL DEFAULT 0,
--     price           DECIMAL(15,2) NOT NULL,
--     description     TEXT,
--     PRIMARY KEY (equipment_id),
--     FOREIGN KEY (manufacturer_id) 
--     -- Need the refereces here because of the foreign key constraint and 
--     -- need for on update and on deletes

--     -- We are using RESTRICT here because it prevents the deltion of a manu
--     -- if they have equipment in the database (dont want to delete all 
--     -- the equ orders they have)
--     REFERENCES manufacturers(manufacturer_id)
--     ON UPDATE CASCADE ON DELETE RESTRICT
-- );

-- -- Orders table (what we use when a customer wants to buy equipement)
-- CREATE TABLE orders (
--     order_id        INT AUTO_INCREMENT,
--     customer_id     INT NOT NULL,
--     equipment_id    INT NOT NULL,
--     quantity       INT NOT NULL,
--     order_date     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     status         ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
--     total_amount   DECIMAL(15,2) NOT NULL,
--     PRIMARY KEY (order_id),
--     -- Same logic for RESTRICT, prevents deletion of customers or equipment 
--     -- that have associated orders (protects order history)
--     FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
--     ON UPDATE CASCADE ON DELETE RESTRICT,
--     FOREIGN KEY (equipment_id) REFERENCES equipment(equipment_id)
--     ON UPDATE CASCADE ON DELETE RESTRICT
-- );


DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS equipment;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS manufacturers;
DROP TABLE IF EXISTS users;

-- Users table (superclass to manufacturers/client)
CREATE TABLE users (
    user_id         INT AUTO_INCREMENT,
    name            VARCHAR(100) NOT NULL,
    contact_email   VARCHAR(100) NOT NULL,
    country         VARCHAR(50) NOT NULL,
    salt CHAR(8)    NOT NULL,
    password_hash   BINARY(64) NOT NULL, 
    PRIMARY KEY (user_id)
);
-- Manufacturers table (subclass of users)
CREATE TABLE manufacturers (
    manufacturer_id INT AUTO_INCREMENT,
    user_id         INT NOT NULL,
    clearance_lvl   VARCHAR(50),
    PRIMARY KEY (manufacturer_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
    ON UPDATE CASCADE ON DELETE CASCADE
);

-- Customers table (subclass of users)
CREATE TABLE customers (
    customer_id     INT AUTO_INCREMENT,
    user_id         INT NOT NULL,
    is_verified     BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (customer_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
    ON UPDATE CASCADE ON DELETE CASCADE
);

-- Military equipment table
CREATE TABLE equipment (
    equipment_id        INT AUTO_INCREMENT,
    manufacturer_id     INT NOT NULL,
    equipment_category  ENUM('Aircraft', 'Land Vehicle') NOT NULL,
    stock               INT NOT NULL DEFAULT 0,
    description         VARCHAR(1000),
    name                VARCHAR(100) NOT NULL,
    specialty           VARCHAR(100),
    price_usd           DECIMAL(15,2) NOT NULL,
    PRIMARY KEY (equipment_id),
    FOREIGN KEY (manufacturer_id) REFERENCES manufacturers(manufacturer_id)
    ON UPDATE CASCADE ON DELETE RESTRICT
);

-- Orders table
CREATE TABLE orders (
    order_id            INT AUTO_INCREMENT,
    customer_id         INT NOT NULL,
    equipment_id        INT NOT NULL,
    order_quantity      INT NOT NULL,
    order_date          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status              ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    total_amount_usd    DECIMAL(15,2) NOT NULL,
    PRIMARY KEY (order_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (equipment_id) REFERENCES equipment(equipment_id)
    ON UPDATE CASCADE ON DELETE RESTRICT
);