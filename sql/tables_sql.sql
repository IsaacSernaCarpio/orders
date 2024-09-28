USE           orders;

-- DROP TABLE product;
-- TRUNCATE TABLE product;
CREATE TABLE product(
	id INT PRIMARY KEY AUTO_INCREMENT, 
    product_key VARCHAR(150) UNIQUE,
    product_description VARCHAR(255),
    unit_of_measure VARCHAR(150),
    unit_price DECIMAL(10, 2) DEFAULT 0.0,
    id_image VARCHAR(50),
    stock INT,
    product_active BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

