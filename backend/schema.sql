-- Pyrites Grill MySQL Database Schema Definition
-- Compatible with Amazon RDS MySQL 8.0+

CREATE DATABASE IF NOT EXISTS `pyrites_grill` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `pyrites_grill`;

-- 1. Restaurant Tables Schema
DROP TABLE IF EXISTS `bookings`;
DROP TABLE IF EXISTS `restaurant_tables`;
DROP TABLE IF EXISTS `menu_items`;

CREATE TABLE `restaurant_tables` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `table_number` VARCHAR(20) NOT NULL UNIQUE,
    `capacity` INT NOT NULL,
    `location_zone` VARCHAR(50) NOT NULL,
    INDEX `idx_table_capacity` (`capacity`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. Menu Items Schema
CREATE TABLE `menu_items` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL,
    `category` VARCHAR(50) NOT NULL,
    `description` TEXT NOT NULL,
    `price_inr` INT NOT NULL,
    `image_url` VARCHAR(500) NOT NULL,
    `is_available` TINYINT(1) DEFAULT 1 NOT NULL,
    INDEX `idx_menu_category` (`category`),
    INDEX `idx_menu_available` (`is_available`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. Bookings Schema
CREATE TABLE `bookings` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `booking_reference` VARCHAR(20) NOT NULL UNIQUE,
    `customer_name` VARCHAR(100) NOT NULL,
    `customer_email` VARCHAR(120) NOT NULL,
    `customer_phone` VARCHAR(20) NOT NULL,
    `booking_date` DATE NOT NULL,
    `booking_time` TIME NOT NULL,
    `guest_count` INT NOT NULL,
    `special_requests` TEXT,
    `status` VARCHAR(20) DEFAULT 'CONFIRMED' NOT NULL,
    `table_id` INT NOT NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_bookings_table` FOREIGN KEY (`table_id`) REFERENCES `restaurant_tables` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX `idx_booking_ref` (`booking_reference`),
    INDEX `idx_customer_email` (`customer_email`),
    INDEX `idx_booking_date_status` (`booking_date`, `status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Initial Seed Data: Restaurant Tables
INSERT INTO `restaurant_tables` (`table_number`, `capacity`, `location_zone`) VALUES
('T-01', 2, 'Patio Terrace'),
('T-02', 2, 'Patio Terrace'),
('T-03', 2, 'Main Dining Room'),
('T-04', 2, 'Main Dining Room'),
('T-05', 4, 'Main Dining Room'),
('T-06', 4, 'Main Dining Room'),
('T-07', 4, 'Main Dining Room'),
('T-08', 4, 'Window Lounge'),
('T-09', 6, 'Main Dining Room'),
('T-10', 6, 'Private Alcove'),
('T-11', 6, 'Private Alcove'),
('T-12', 8, 'Private Alcove'),
('T-13', 8, 'Chef\'s Table VIP');

-- Initial Seed Data: Menu Items
INSERT INTO `menu_items` (`name`, `category`, `description`, `price_inr`, `image_url`, `is_available`) VALUES
('Pyrites Signature Ribeye Steak (350g)', 'Grills', 'Prime Aged Angus Ribeye grilled over hickory charcoal with rosemary butter & smoked sea salt.', 1499, 'https://images.unsplash.com/photo-1558030006-450675393462?auto=format&fit=crop&w=800&q=80', 1),
('Fire-Kissed Rosemary Lamb Chops', 'Grills', 'Tender New Zealand lamb chops marinated in garlic, mint, and woodfire smoke.', 1299, 'https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=800&q=80', 1),
('Smoked Bourbon BBQ Pork Ribs', 'Grills', 'Slow-cooked full rack of baby back ribs glazed with homemade bourbon BBQ sauce.', 1199, 'https://images.unsplash.com/photo-1529193591184-b1d58069ecdd?auto=format&fit=crop&w=800&q=80', 1),
('Charcoal Grilled Tandoori Salmon', 'Grills', 'Fresh Atlantic salmon fillet infused with aromatic Indian spices and grilled to perfection.', 1099, 'https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=800&q=80', 1),
('Smoked Wagyu Truffle Burger', 'Burgers', 'Double Wagyu beef patty, black truffle aioli, aged cheddar, and caramelized onions on brioche.', 749, 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=800&q=80', 1),
('Pyrites Monster Bacon Cheeseburger', 'Burgers', 'Flame-grilled Angus patty, crispy smoked bacon, melted gouda, pickles, and signature house sauce.', 649, 'https://images.unsplash.com/photo-1586190848861-99aa4a171e90?auto=format&fit=crop&w=800&q=80', 1),
('Charred Garlic Butter Prawns', 'Starters', 'Jumbo tiger prawns seared on open flames with roasted garlic butter and fresh herbs.', 599, 'https://images.unsplash.com/photo-1565680018434-b513d5e5fd47?auto=format&fit=crop&w=800&q=80', 1),
('Truffle & Parmesan Hand-Cut Fries', 'Sides', 'Crispy russet potato fries tossed in white truffle oil, grated parmesan, and sea salt.', 299, 'https://images.unsplash.com/photo-1573080496219-bb080dd4f877?auto=format&fit=crop&w=800&q=80', 1),
('Pyrites Smoked Old Fashioned', 'Drinks', 'Bourbon, angostura bitters, orange peel, smoked under oakwood smoke glass.', 499, 'https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?auto=format&fit=crop&w=800&q=80', 1);
