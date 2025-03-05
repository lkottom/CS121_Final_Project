-- Sample data for testing

-- Insert test users (manufacturers and customers)
INSERT INTO users (name, contact_email, country, salt, password_hash) 
VALUES 
('Lockheed Martin', 'lm@example.com', 'USA', 'abcd1234', SHA2(CONCAT('abcd1234', 'password123'), 256)),
('Boeing Defense', 'boeing@example.com', 'USA', 'efgh5678', SHA2(CONCAT('efgh5678', 'password123'), 256)),
('Russian Armaments', 'ra@example.com', 'Russia', 'ijkl9012', SHA2(CONCAT('ijkl9012', 'password123'), 256)),
('European Defense Group', 'edg@example.com', 'Germany', 'mnop3456', SHA2(CONCAT('mnop3456', 'password123'), 256)),
('US Government', 'usgov@example.com', 'USA', 'qrst7890', SHA2(CONCAT('qrst7890', 'password123'), 256)),
('UK Ministry of Defence', 'ukmod@example.com', 'UK', 'uvwx1234', SHA2(CONCAT('uvwx1234', 'password123'), 256)),
('India Defense Ministry', 'india@example.com', 'India', 'yzab5678', SHA2(CONCAT('yzab5678', 'password123'), 256)),
('Japan Self-Defense Forces', 'jsdf@example.com', 'Japan', 'cdef9012', SHA2(CONCAT('cdef9012', 'password123'), 256));

-- Insert manufacturers (linking to users)
INSERT INTO manufacturers (user_id, clearance_lvl) 
VALUES 
(1, 'Top Secret'),
(2, 'Top Secret'),
(3, 'Confidential'),
(4, 'Secret');

-- Insert customers (linking to users)
INSERT INTO customers (user_id, is_verified) 
VALUES 
(5, TRUE),
(6, TRUE),
(7, TRUE),
(8, TRUE);

-- Insert equipment (aircraft)
INSERT INTO equipment (manufacturer_id, equipment_category, stock, description, name, specialty, price_usd) 
VALUES 
(1, 'Aircraft', 5, 'Advanced stealth fighter jet with superior air-to-air combat capabilities', 'F-35 Lightning II', 'Fighter Jet', 80000000.00),
(1, 'Aircraft', 3, 'Long-range heavy bomber with stealth capabilities', 'B-2 Spirit', 'Bomber', 950000000.00),
(2, 'Aircraft', 8, 'Multirole combat helicopter for battlefield transport and attack missions', 'AH-64 Apache', 'Attack Helicopter', 35000000.00),
(2, 'Aircraft', 6, 'Maritime patrol aircraft for anti-submarine warfare and surveillance', 'P-8 Poseidon', 'Maritime Patrol', 125000000.00),
(3, 'Aircraft', 4, 'Transport helicopter used for troop movement and supply delivery', 'Mi-17', 'Transport Helicopter', 15000000.00),
(4, 'Aircraft', 7, 'Tactical airlift aircraft capable of operating from rough airfields', 'A400M Atlas', 'Transport Aircraft', 145000000.00);

-- Insert equipment (land vehicles)
INSERT INTO equipment (manufacturer_id, equipment_category, stock, description, name, specialty, price_usd) 
VALUES 
(1, 'Land Vehicle', 12, 'Main battle tank with advanced armor and targeting systems', 'M1A2 Abrams', 'Main Battle Tank', 8000000.00),
(2, 'Land Vehicle', 15, 'Infantry fighting vehicle with amphibious capabilities', 'Bradley IFV', 'Infantry Fighting Vehicle', 4500000.00),
(3, 'Land Vehicle', 20, 'Heavily armed and armored personnel carrier', 'BTR-90', 'Armored Personnel Carrier', 3200000.00),
(4, 'Land Vehicle', 10, 'Mobile artillery system with extended range', 'PzH 2000', 'Self-propelled Howitzer', 4700000.00),
(3, 'Land Vehicle', 14, 'Modern main battle tank with reactive armor', 'T-90', 'Main Battle Tank', 4500000.00),
(4, 'Land Vehicle', 8, 'Armored reconnaissance vehicle with advanced sensors', 'Fennek', 'Reconnaissance Vehicle', 2100000.00);

-- Insert some sample orders
INSERT INTO orders (customer_id, equipment_id, order_quantity, order_date, status, total_amount_usd) 
VALUES 
(1, 1, 2, '2023-10-15 09:30:00', 'approved', 160000000.00),
(1, 7, 3, '2023-11-20 14:45:00', 'approved', 24000000.00),
(2, 3, 4, '2023-12-05 11:20:00', 'pending', 140000000.00),
(3, 5, 2, '2024-01-10 16:15:00', 'rejected', 30000000.00),
(3, 9, 5, '2024-02-08 10:30:00', 'approved', 16000000.00),
(4, 6, 1, '2024-03-01 13:45:00', 'pending', 145000000.00);