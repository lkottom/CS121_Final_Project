DROP FUNCTION IF EXISTS make_salt;
DROP PROCEDURE IF EXISTS sp_add_user;
DROP FUNCTION IF EXISTS authenticate;
DROP PROCEDURE IF EXISTS sp_change_pw;

-- Fixing an error here, make DETERMINISTIC to load properly 

-- NOTE: we are using our "users" table as a replacement for the user_info 
-- table, it is the same functionality exactly but in our ER and code we 
-- designate the user_info as users

DELIMITER !
CREATE FUNCTION make_salt(num_chars INT)
RETURNS VARCHAR(20) DETERMINISTIC
BEGIN
    DECLARE salt VARCHAR(20) DEFAULT '';

    -- Don't want to generate more than 20 characters of salt.
    SET num_chars = LEAST(20, num_chars);

    -- Generate the salt!  Characters used are ASCII code 32 (space)
    -- through 126 ('z').
    WHILE num_chars > 0 DO
        SET salt = CONCAT(salt, CHAR(32 + FLOOR(RAND() * 95)));
        SET num_chars = num_chars - 1;
    END WHILE;

    RETURN salt;
END !
DELIMITER ;

DELIMITER !
-- Increasing the new_name so that emails can be taken in 
CREATE PROCEDURE sp_add_user(new_name VARCHAR(100), new_email VARCHAR(100),
    new_country VARCHAR(50), new_password VARCHAR(20)
)
BEGIN
    DECLARE salt_val CHAR(8);

    -- Salt values are always 8 characters long
    SET salt_val = make_salt(8);

    -- Insert user with generated salt and hashed password
    INSERT INTO users (name, contact_email, country, salt, password_hash)
    VALUES (new_name, new_email, new_country, salt_val, 
        SHA2(CONCAT(salt_val, new_password), 256)
    );

END !
DELIMITER ;

DELIMITER !
CREATE FUNCTION authenticate(name VARCHAR(100), password VARCHAR(20))
RETURNS TINYINT DETERMINISTIC
BEGIN
    -- Declaring varibles to use later
    DECLARE user_salt CHAR(8);
    DECLARE stored_hash BINARY(64);
    DECLARE user_exists INT;

    -- First, we see if the user is actually in the table
      SELECT COUNT(*) INTO user_exists FROM users 
      WHERE users.contact_email = name;

      -- If they do not exist, return 0
      IF user_exists = 0 THEN
        RETURN 0;
      END IF;

      -- If they do exist, take the salt and the hash and move to the varibles
      -- above
      SELECT salt, password_hash INTO user_salt, stored_hash
      FROM users
      WHERE users.contact_email = name;

      -- Check if the given password (after we salt and hash it)
      -- matches the stored hash for that user
      IF stored_hash = SHA2(CONCAT(user_salt, password), 256) THEN
        RETURN 1; -- Success -> return 1
      ELSE
        RETURN 0; -- Failed -> return 0
      END IF;
END !
DELIMITER ;

DELIMITER !
CREATE PROCEDURE sp_change_pw(username VARCHAR(100), new_password VARCHAR(20))
BEGIN
  -- The vars we will use later 
  DECLARE salt_value CHAR(8);
  DECLARE user_exists INT;
  
  -- Same user name checking as above
  SELECT COUNT(*) INTO user_exists FROM users 
  WHERE users.contact_email = username;
  
  -- Only do the following if the user actually exists
  IF user_exists = 1 THEN
    -- Make sure to generate a new salt value
    SET salt_value = make_salt(8);
    
    -- Then, we make sure to update that users 
    -- salt and password hash
    UPDATE users
    SET salt = salt_value,
        password_hash = SHA2(CONCAT(salt_value, new_password), 256)
    WHERE users.contact_email = username;
  END IF;
END !
DELIMITER ;
