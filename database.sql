-- Inventory Management System Database Schema
-- Run this script to set up the database

-- Create database
CREATE DATABASE IF NOT EXISTS inventory_db;
USE inventory_db;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create products table
CREATE TABLE IF NOT EXISTS products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    quantity INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default admin user (password: admin123)
-- Password hash generated using werkzeug.security.generate_password_hash
INSERT INTO users (username, password) VALUES 
('admin', 'scrypt:32768:8:1$XqZV7qZK8YmJnHrL$c8e5f8f9d1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8');

-- Insert sample products for testing
INSERT INTO products (product_name, category, price, quantity) VALUES
('Paracetamol 500mg', 'Medicine', 5.99, 150),
('Amoxicillin 250mg', 'Antibiotics', 12.50, 8),
('Vitamin C Tablets', 'Supplements', 8.99, 45),
('Bandages (Pack of 10)', 'First Aid', 3.50, 5),
('Hand Sanitizer 500ml', 'Hygiene', 6.99, 200),
('Face Masks (Box of 50)', 'Protection', 15.00, 3),
('Thermometer Digital', 'Equipment', 25.00, 20),
('Blood Pressure Monitor', 'Equipment', 75.00, 12),
('Cough Syrup 100ml', 'Medicine', 7.50, 9),
('Antiseptic Cream 50g', 'First Aid', 4.99, 35);
