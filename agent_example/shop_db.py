import sqlite3

# Connect to SQLite (creates the DB file if it doesn't exist)
conn = sqlite3.connect("shop.db")
cursor = conn.cursor()

# Drop existing tables if they exist
cursor.executescript(
    """
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;
"""
)

# Create tables
cursor.executescript(
    """
CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    order_date TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
"""
)

# Insert dummy customers
customers = [
    ("Alice Johnson", "alice@example.com"),
    ("Bob Smith", "bob@example.com"),
    ("Charlie Brown", "charlie@example.com"),
]
cursor.executemany("INSERT INTO customers (name, email) VALUES (?, ?);", customers)

# Insert dummy products
products = [
    ("Laptop", 1200.00),
    ("Phone", 800.00),
    ("Headphones", 150.00),
    ("Keyboard", 75.00),
]
cursor.executemany("INSERT INTO products (name, price) VALUES (?, ?);", products)

# Insert dummy orders
orders = [
    (1, "2025-06-01"),
    (2, "2025-06-01"),
    (1, "2025-06-02"),
]
cursor.executemany(
    "INSERT INTO orders (customer_id, order_date) VALUES (?, ?);", orders
)

# Insert dummy order items
order_items = [
    (1, 1, 1),  # Order 1: Laptop x1
    (1, 3, 2),  # Order 1: Headphones x2
    (2, 2, 1),  # Order 2: Phone x1
    (3, 4, 1),  # Order 3: Keyboard x1
    (3, 3, 1),  # Order 3: Headphones x1
]
cursor.executemany(
    "INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?);",
    order_items,
)


conn.commit()
conn.close()


print("Database created and populated successfully!")
