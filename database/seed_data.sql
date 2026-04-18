-- Seed data for testing

INSERT INTO users (username, email, password, role) VALUES
('admin', 'admin@inventory.local', 'hashed_password_here', 'admin'),
('manager', 'manager@inventory.local', 'hashed_password_here', 'manager'),
('staff', 'staff@inventory.local', 'hashed_password_here', 'staff');

INSERT INTO products (name, description, price, sku, quantity, category) VALUES
('Laptop', 'High-performance laptop for business', 85000, 'SKU001', 15, 'Electronics'),
('Mouse', 'Wireless mouse', 2500, 'SKU002', 50, 'Accessories'),
('Keyboard', 'Mechanical keyboard', 5000, 'SKU003', 30, 'Accessories'),
('Monitor', '27-inch HD monitor', 25000, 'SKU004', 8, 'Electronics'),
('Desk Lamp', 'LED desk lamp', 3500, 'SKU005', 25, 'Office Supplies'),
('Notebook', 'A4 notebook', 150, 'SKU006', 200, 'Stationery'),
('Pen Set', 'Set of 10 pens', 500, 'SKU007', 100, 'Stationery'),
('USB Cable', 'High-speed USB 3.0 cable', 800, 'SKU008', 75, 'Accessories');
