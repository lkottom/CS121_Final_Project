-- CLIENT APPLICATION QUERIES (placed directly in the python code
-- with the use of cursor):

-- For easy of making sure we got everything, we just went thought the python
-- code and copied over evry statement (there are some updates and inserts
-- but all the SELECTS work without errors and function as they should)

-- We just commented out the non-SELECT queries as specified in the spec, 
-- only SELECT queries should be in here (we included the others for 
-- coverage and all work as they should)


-- Control + "f" and type "equivalent to RA Expression " to see which 
-- queries are equivalent to our RA expressions

-- Query 1: Authenticate user credentials
SELECT authenticate('customer69@example.com', 'password123') AS auth_result;

-- Query 2: Get user ID after successful authentication
SELECT user_id FROM users WHERE contact_email = 'customer69@example.com';

-- Query 3: Get customer ID from user ID
SELECT customer_id FROM customers WHERE user_id = 5;

-- Query 4: Browse all available equipment
SELECT e.name, e.specialty AS role, e.price_usd AS price, u.name AS manufacturer 
FROM equipment e
JOIN manufacturers m ON e.manufacturer_id = m.manufacturer_id
JOIN users u ON m.user_id = u.user_id
ORDER BY e.name;

-- Query 5: Browse aircraft equipment only
SELECT e.name, e.specialty AS role, e.price_usd AS price, u.name AS manufacturer 
FROM equipment e
JOIN manufacturers m ON e.manufacturer_id = m.manufacturer_id
JOIN users u ON m.user_id = u.user_id
WHERE e.equipment_category = 'Aircraft'
ORDER BY e.name;

-- Query 6: Browse land vehicle equipment only
SELECT e.name, e.specialty AS role, e.price_usd AS price, u.name AS manufacturer 
FROM equipment e
JOIN manufacturers m ON e.manufacturer_id = m.manufacturer_id
JOIN users u ON m.user_id = u.user_id
WHERE e.equipment_category = 'Land Vehicle'
ORDER BY e.name;

-- Query 7: View all available equipment for ordering 
-- This is equivalent to RA Expression 2
SELECT equipment_id, name, stock, price_usd, manufacturer 
FROM available_equipment 
ORDER BY name;


-- Query 8: Get specific equipment details for placing an order
SELECT e.equipment_id, e.name, e.price_usd, e.stock, u.name AS manufacturer
FROM equipment e
JOIN manufacturers m ON e.manufacturer_id = m.manufacturer_id
JOIN users u ON m.user_id = u.user_id
WHERE e.name = 'B-2A Spirit';

-- -- Query 9: Insert a new order
-- INSERT INTO orders (customer_id, equipment_id, order_quantity, 
-- total_amount_usd)
-- VALUES (1, 1, 2, 160000000.00);

-- Query 10: Update equipment stock after an order
-- UPDATE equipment 
-- SET stock = stock - 2
-- WHERE equipment_id = 1;

-- Query 11: Get order ID of most recent order
SELECT order_id 
FROM orders 
WHERE customer_id = 1 
ORDER BY order_date DESC;

-- Query 12: View customer order history 
-- This is equivalent to RA Expression 3
SELECT order_id, order_date, equipment_name, order_quantity, 
       price_usd, total_cost, status
FROM customer_order_history
WHERE customer_id = 1
ORDER BY order_date DESC;

-- Query 13: Create a new user account
-- CALL sp_add_user('Luke Kottom', 'lk@gmail.com', 'USA', 'password123!');

-- -- Query 14: Insert new customer into customer table 
-- INSERT INTO customers (user_id, is_verified) 
-- VALUES (9, TRUE);


-- ADMIN APPLICATION QUERIES:

-- Query 15: Authenticate admin user
SELECT authenticate('lockheed@example.com', 'password123') AS auth_result;

-- Query 16: Get admin user ID
SELECT user_id FROM users 
WHERE contact_email = 'lockheed@example.com';

-- Query 17: Get manufacturer ID from user ID
SELECT manufacturer_id FROM manufacturers WHERE user_id = 1;

-- Query 18: Display equipment stock levels
SELECT e.name, e.stock, e.equipment_category 
FROM equipment e 
WHERE e.manufacturer_id = 1
ORDER BY e.stock;

-- Query 19: Display equipment details
SELECT e.name, e.equipment_category, e.specialty, e.description, 
       e.price_usd, e.stock
FROM equipment e
WHERE e.manufacturer_id = 1
ORDER BY e.name;

-- Query 20: Display equipment details for a specific name
SELECT e.name, e.equipment_category, e.specialty, e.description, 
       e.price_usd, e.stock
FROM equipment e
WHERE e.manufacturer_id = 1 AND e.name LIKE '%F-35%'
ORDER BY e.name;

-- Query 21: Display equipment by type (Aircraft)
SELECT e.name, e.specialty, e.stock, e.price_usd 
FROM equipment e
WHERE e.manufacturer_id = 1 AND e.equipment_category = 'Aircraft'
ORDER BY e.name;

-- Query 22: Display equipment by type (Land Vehicle)
SELECT e.name, e.specialty, e.stock, e.price_usd 
FROM equipment e
WHERE e.manufacturer_id = 1 AND e.equipment_category = 'Land Vehicle'
ORDER BY e.name;

-- Query 23: Display all equipment with categories
SELECT e.name, e.specialty, e.stock, e.price_usd, e.equipment_category 
FROM equipment e
WHERE e.manufacturer_id = 1
ORDER BY e.equipment_category, e.name;

-- Query 24: Add new equipment
INSERT INTO equipment (
    manufacturer_id, equipment_category, stock, 
    description, name, specialty, price_usd)
VALUES (
    1, 'Land Vehicle', 10, 
    'Advanced armored personnel carrier with enhanced protection', 
    'M113A3 APC', 'Personnel Transport', 2200000.00);

-- Query 25: Get last inserted equipment ID
SELECT LAST_INSERT_ID();

-- Query 26: List equipment for price update
SELECT equipment_id, name, price_usd 
FROM equipment 
WHERE manufacturer_id = 1
ORDER BY name;

-- -- Query 27: Update equipment price
-- UPDATE equipment 
-- SET price_usd = 85000000.00
-- WHERE equipment_id = 1 AND manufacturer_id = 1;

-- Query 28: List equipment for stock update
SELECT equipment_id, name, stock 
FROM equipment 
WHERE manufacturer_id = 1
ORDER BY name;

-- -- Query 29: Update equipment stock
-- UPDATE equipment 
-- SET stock = 8
-- WHERE equipment_id = 1 AND manufacturer_id = 1;

-- Query 30: Equipment sales statistics 
-- This is equivalent to RA Expression 1
SELECT e.name, e.equipment_category, 
       SUM(o.order_quantity) as total_units,
       SUM(o.total_amount_usd) as total_revenue
FROM equipment e
LEFT JOIN orders o ON e.equipment_id = o.equipment_id
WHERE e.manufacturer_id = 1 AND o.status = 'approved'
GROUP BY e.equipment_id
ORDER BY total_revenue DESC;

-- Query 31: View all orders for a manufacturer
SELECT o.order_id, o.order_date, u.name as customer_name, 
       e.name as equipment_name, o.order_quantity, 
       o.total_amount_usd, o.status
FROM orders o
JOIN equipment e ON o.equipment_id = e.equipment_id
JOIN customers c ON o.customer_id = c.customer_id
JOIN users u ON c.user_id = u.user_id
WHERE e.manufacturer_id = 1
ORDER BY o.status, o.order_date DESC;

-- Query 32: Get order status
SELECT status FROM orders WHERE order_id = 3;
