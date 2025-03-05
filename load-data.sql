SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE manufacturers;
TRUNCATE TABLE customers;
TRUNCATE TABLE users;
TRUNCATE TABLE equipment;
TRUNCATE TABLE orders;
SET FOREIGN_KEY_CHECKS = 1;

LOAD DATA LOCAL INFILE 'data/final_data_for_sql/users.csv'
INTO TABLE users
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(name,contact_email,country,salt,password_hash);

LOAD DATA LOCAL INFILE 'data/final_data_for_sql/manufacturers.csv'
INTO TABLE manufacturers
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(user_id, clearance_lvl);


LOAD DATA LOCAL INFILE 'data/final_data_for_sql/customers.csv'
INTO TABLE customers
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(user_id, is_verified);

LOAD DATA LOCAL INFILE 'data/final_data_for_sql/equipment.csv'
INTO TABLE equipment
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(name, equipment_id, equipment_category, specialty, price_usd, 
@dummy, manufacturer_id, stock, description);

LOAD DATA LOCAL INFILE 'data/final_data_for_sql/orders.csv'
INTO TABLE orders
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(customer_id, equipment_id, order_quantity, order_date, status, 
total_amount_usd);