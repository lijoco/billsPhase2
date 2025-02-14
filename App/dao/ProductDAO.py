from App.model.Product import Product
import sqlite3

class ProductDAO:
    def __init__(self):
        self.db_path ="database.db"  # This sets the path

    # Establishes connection to DB
    def get_db_connection(self):
        conn = sqlite3.connect(self.db_path)  # Opens connection to path above
        conn.row_factory = sqlite3.Row  # Rather than indexing, this lets you select by column name
        return conn  # return connection

    def getAllProducts(self):
        conn = self.get_db_connection()  # that's doing everything outlined in the above function. Establishing connection to DB
        cursor = conn.cursor()  # Creates a cursor? I don't really know but its in all his tutorial material. Guessing it's how to select stuff.
        cursor.execute("SELECT * FROM products")  # watch this cause it selects everything so if I add a column it might mess it up
        rows = cursor.fetchall()  # fetchall returns what was selected by the cursor
        conn.close()

        # Creates an empty list and loops through DB to populate it.
        products = []
        for row in rows:
            product = Product(
                product_id=row['id'],
                name=row['name'],
                price=row['price'],
                description=row['description'],
                image_url=f"images/{row['name'].replace(' ', '_').lower()}.jpg"  # Constructs url dynamically. filenames must follow this pattern or else the image doesn't load and it uses the back-up image instead
            )
            products.append(product)
        return products

    def getProductById(self, id):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()

        # If ID is found return the product
        if row:
            return Product(
                product_id=row['id'],
                name=row['name'],
                price=row['price'],
                description=row['description'],
                image_url=f"images/{row['name'].replace(' ', '_').lower()}.jpg")

        return None
