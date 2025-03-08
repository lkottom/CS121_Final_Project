-- Part I. Procedural SQL
-- Partner project: +1 function used

-- Good to drop existing functions, procedures, and triggers to avoid errors
DROP FUNCTION IF EXISTS calculate_customer_spending;
DROP FUNCTION IF EXISTS check_equipment_availability;
DROP PROCEDURE IF EXISTS sp_process_pending_orders;
DROP TRIGGER IF EXISTS trg_update_stock_on_reject;

-- UDF 1: Calculate total spending by a customer
-- This will return the total amout spent by a customer (on the orders that
-- have actually been approved)
DELIMITER !
CREATE FUNCTION calculate_customer_spending(cust_id INT) 
RETURNS DECIMAL(15,2) DETERMINISTIC
BEGIN
    -- Varibale the will store the total
    DECLARE total DECIMAL(15,2);
    
    -- Making sure we sum up only the approved orders
    SELECT SUM(total_amount_usd) INTO total
    FROM orders
    WHERE customer_id = cust_id AND status = 'approved';
    
    -- If we get nothing (NULL), then they havent spent any money
    IF total IS NULL THEN
        RETURN 0.00;
    ELSE
        RETURN total;
    END IF;
END !
DELIMITER ;

-- UDF 2: Check if equipment has enough in stock stock
-- This will return 1 if there is enough equ in stock, it will return 
-- 0 otherwise
DELIMITER !
CREATE FUNCTION check_equipment_availability(equip_id INT, quantity INT) 
RETURNS TINYINT DETERMINISTIC
BEGIN
    -- Varible to hold the avail stock 
    DECLARE available_stock INT;
    
    SELECT stock INTO available_stock
    FROM equipment
    WHERE equipment_id = equip_id;
    
    -- If there is enough stock, return 1
    IF available_stock >= quantity THEN
        RETURN 1; 
    ELSE
        RETURN 0; 
    END IF;
END !
DELIMITER ;


-- Procedure: This procedure will process pending orders for a manufacturer
-- in a nice way (changes all pending orders for a manufacturer to approved 
-- status so they don't have to go in a manually do it)
DELIMITER !
CREATE PROCEDURE sp_process_pending_orders(manufacturer_id INT)
BEGIN
    -- Update all pending orders to be approved
    UPDATE orders o
    JOIN equipment e ON o.equipment_id = e.equipment_id
    SET o.status = 'approved'
    WHERE e.manufacturer_id = manufacturer_id AND o.status = 'pending';
    
    -- Then, we want to return as result how many orders were actually process 
    SELECT CONCAT('Processed ', ROW_COUNT(), ' pending orders') AS result;
END !
DELIMITER ;


-- Trigger: This trigger auto updates the stock of an equip when order status 
-- changes to reject (making sure // as direct from MySQL docs)
DELIMITER !
DELIMITER //
CREATE TRIGGER trg_update_stock_on_reject
AFTER UPDATE ON orders
FOR EACH ROW
BEGIN
    IF NEW.status = 'rejected' AND OLD.status != 'rejected' THEN
        UPDATE equipment
        SET stock = stock + NEW.order_quantity
        WHERE equipment_id = NEW.equipment_id;
    END IF ;
END//

-- Go back to the right delimiter so we can keep entering in terminals
DELIMITER ;


