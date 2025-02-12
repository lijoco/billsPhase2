import sqlite3
import os
from App.model.Product import Product

# Path to the directory containing images
IMAGE_DIR = os.path.join(os.path.dirname(__file__), 'static', 'images')

# Debugging: Check if the image directory exists
if not os.path.exists(IMAGE_DIR):
    print(f"Error: Image directory does not exist: {IMAGE_DIR}")
else:
    print(f"Image directory found: {IMAGE_DIR}")

# Sample data (Item name, description, and corresponding image filename)
sample_data = [
    Product(1, "Princess Castle", 100.00, "Pink", "princess_castle.jpg"),
    Product(2, "Plain Castle", 50.00, "Plain Castle", "plain_castle.jpg"),
    Product(3, "Obstacle Course", 120.00, "Obstacle Course", "obstacle_course.jpg"),
    Product(4, "Mc Castle", 99.99, "I'm Lovin' It", "mc_castle.jpg"),
    Product(5, "Boxing Ring", 80.00, "The Mayweather", "boxing_ring.jpg"),
    Product(6, "Biker Kid Castle", 90.00, "Badass Slide", "biker_kid_castle.jpg"),
    Product(7, "Big Slide", 120.00, "Big Creepy Slide", "big_slide.jpg"),
    Product(8, "Balls", 9.99, "Multi-colored Balls", "balls.jpg")
]

# Function to read an image file and return binary data
def get_image_blob(image_filename):
    image_path = os.path.join(IMAGE_DIR, image_filename)
    if os.path.exists(image_path):
        with open(image_path, "rb") as file:
            return file.read()
    return None  # Return None if the image file does not exist

# Initialize the database
def initialize_database():
    try:
        # Connect to SQLite database (creates the file if it doesn't exist)
        db_path = os.path.abspath('database.db')
        print(f"Database file path: {db_path}")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Create table with an image BLOB field
        cursor.execute('''CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price FLOAT NOT NULL,
            description TEXT NOT NULL,
            image BLOB
        )''')

        # Debugging: Check if table creation was successful
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='products';")
        table_check = cursor.fetchone()
        if table_check:
            print("Table 'products' exists.")
        else:
            print("Table 'products' does not exist.")

        # Clear existing data (optional)
        cursor.execute("DELETE FROM products")

        # Insert sample data with images
        for product in sample_data:
            name = product.name
            price = product.price
            description = product.description
            image_filename = product.image_url

            image_blob = get_image_blob(image_filename)
            if image_blob:
                cursor.execute('''INSERT INTO products (name, price, description, image)
                VALUES (?, ?, ?, ?)''' , (name, price, description, image_blob))
            else:
                print(f"Warning: Image '{image_filename}' not found in {IMAGE_DIR}")

        # Commit changes and close connection
        conn.commit()
        conn.close()
        print("Database initialized with sample data.")
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")

if __name__ == "__main__":
    initialize_database()

    # Test - don't use * cause it prints out the BLOB too and its unreadable
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, price, description FROM products")
        rows = cursor.fetchall()
        print("Below is the DB:")
        for row in rows:
            print(row)
        conn.close()
    except sqlite3.Error as e:
        print(f"Error querying the database: {e}")

    db_path = os.path.abspath('database.db')
    print(f"Using database: {db_path}")

