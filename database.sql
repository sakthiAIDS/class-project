-- ============================================================================
-- Food Donation Management System — MySQL Schema
-- ============================================================================
-- This project runs on SQLite by default (zero setup, perfect for VS Code).
-- Use this file ONLY if your college specifically requires MySQL.
--
-- Setup:
--   1) CREATE DATABASE food_donation_db;  (or run this whole file)
--   2) In config.py, set USE_MYSQL = True and fill in your credentials
--   3) pip install pymysql
--   4) Run: python app.py   (SQLAlchemy will create tables automatically)
--      OR import this file directly using: mysql -u root -p food_donation_db < database.sql
-- ============================================================================

CREATE DATABASE IF NOT EXISTS food_donation_db;
USE food_donation_db;

-- ----------------------------------------------------------------------------
-- Users (donors, NGOs, volunteers, admin)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    phone VARCHAR(20),
    address VARCHAR(255),
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'donor',           -- donor | ngo | volunteer | admin
    category VARCHAR(30) DEFAULT 'Individual',            -- Restaurant/Hotel/.../NGO/Volunteer/Individual
    logo_path VARCHAR(255),
    is_approved BOOLEAN DEFAULT TRUE,
    is_active BOOLEAN DEFAULT TRUE,
    pickup_success_rate FLOAT DEFAULT 90.0,
    latitude FLOAT DEFAULT 11.3410,
    longitude FLOAT DEFAULT 77.7172,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ----------------------------------------------------------------------------
-- Food Donations
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS donations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    donation_code VARCHAR(20) NOT NULL UNIQUE,
    donor_id INT NOT NULL,
    ngo_id INT,
    food_name VARCHAR(120) NOT NULL,
    category VARCHAR(30) NOT NULL,
    quantity VARCHAR(50),
    meals_count INT DEFAULT 0,
    prep_time DATETIME,
    expiry_time DATETIME,
    pickup_address VARCHAR(255),
    latitude FLOAT DEFAULT 11.3410,
    longitude FLOAT DEFAULT 77.7172,
    contact_person VARCHAR(120),
    contact_phone VARCHAR(20),
    instructions TEXT,
    image_path VARCHAR(255),
    status VARCHAR(30) DEFAULT 'created',    -- created/accepted/volunteer_assigned/picked_up/delivered/completed/expired
    priority VARCHAR(10) DEFAULT 'Normal',   -- High / Normal
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    accepted_at DATETIME,
    picked_up_at DATETIME,
    delivered_at DATETIME,
    completed_at DATETIME,
    FOREIGN KEY (donor_id) REFERENCES users(id),
    FOREIGN KEY (ngo_id) REFERENCES users(id)
);

-- ----------------------------------------------------------------------------
-- Donation Images (extra photos per donation)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS donation_images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    donation_id INT NOT NULL,
    image_path VARCHAR(255) NOT NULL,
    FOREIGN KEY (donation_id) REFERENCES donations(id)
);

-- ----------------------------------------------------------------------------
-- Volunteers
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS volunteers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    phone VARCHAR(20),
    vehicle VARCHAR(50) DEFAULT 'Two Wheeler',
    is_available BOOLEAN DEFAULT TRUE,
    ngo_id INT,
    FOREIGN KEY (ngo_id) REFERENCES users(id)
);

-- ----------------------------------------------------------------------------
-- Pickup Requests
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS pickup_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    donation_id INT NOT NULL,
    ngo_id INT NOT NULL,
    volunteer_id INT,
    status VARCHAR(30) DEFAULT 'assigned',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (donation_id) REFERENCES donations(id),
    FOREIGN KEY (ngo_id) REFERENCES users(id),
    FOREIGN KEY (volunteer_id) REFERENCES volunteers(id)
);

-- ----------------------------------------------------------------------------
-- Notifications
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(150) NOT NULL,
    message VARCHAR(255),
    type VARCHAR(30) DEFAULT 'info',
    is_read BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- ----------------------------------------------------------------------------
-- Reports (saved report snapshots)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    report_type VARCHAR(20),
    total_donations INT DEFAULT 0,
    total_meals INT DEFAULT 0,
    food_saved_kg FLOAT DEFAULT 0,
    generated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ----------------------------------------------------------------------------
-- Default admin account (password: admin123 — change after first login)
-- Note: this hash must be regenerated by seed_data.py or the app;
-- inserting a real Werkzeug hash here isn't practical in raw SQL.
-- Simplest path: run `python seed_data.py` after pointing config.py at MySQL.
-- ----------------------------------------------------------------------------
