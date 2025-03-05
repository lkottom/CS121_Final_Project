-- Drop users if they exist
DROP USER IF EXISTS 'military_admin'@'localhost';
DROP USER IF EXISTS 'military_client'@'localhost';

CREATE USER 'military_admin'@'localhost' IDENTIFIED BY 'adminpw';
CREATE USER 'military_client'@'localhost' IDENTIFIED BY 'clientpw';

-- Granting access the the admin (total access)
GRANT ALL PRIVILEGES ON military_db.* TO 'military_admin'@'localhost';

-- Granting access to the client 
-- Clients should only be able to view equipment, 
-- place orders, and view their order history
-- (this can be updated to more specific right now we are just granting 
-- access to everything for the client)
GRANT ALL PRIVILEGES ON military_db.* TO 'military_client'@'localhost';

FLUSH PRIVILEGES;