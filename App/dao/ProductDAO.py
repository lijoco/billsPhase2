from App.model.Product import Product
import sqlite3

class ProductDAO:
    def __init__(self):
        # self.products = [
        #     Product(1, "Princess Castle", 100.00, "Pink", "images/princess_castle.jpg"),
        #     Product(2, "Plain Castle", 50.00, "Plain Castle", "images/plain_castle.jpg"),
        #     Product(3, "Obstacle Course", 120.00, "Obstacle Course", "images/obstacle_course.jpg"),
        #     Product(4, "McCastle", 99.99, "I'm Lovin' It", "images/mc_castle.jpg"),
        #     Product(5, "Boxing Ring", 80.00, "The Mayweather", "images/boxing_ring.jpg"),
        #     Product(6, "Biker Kid Castle", 90.00, "Badass Slide", "images/biker_kid_castle.jpg"),
        #     Product(7, "Big Slide", 120.00, "Big Creepy Slide", "images/big_slide.jpg"),
        #     Product(8, "Balls", 9.99, "Multi-colored Balls", "images/balls.jpg")
        # ]
        self.db_path ="database.db"

    def get_db_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def getAllProducts(self):
        # return self.products
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        conn.close()

        # this might be wrong, come back if broken
        products = []
        for row in rows:
            product = Product(
                product_id=row['id'],
                name=row['name'],
                price=row['price'],
                description=row['description'],
                image_url=f"images/{row['name'].replace(' ', '_').lower()}.jpg"
            )
            products.append(product)
        return products

    def getProductById(self, id):
        # for product in self.products:
        #     if product.product_id== id:
        #         return product
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return Product(
                product_id=row['id'],
                name=row['name'],
                price=row['price'],
                description=row['description'],
                image_url=f"images/{row['name'].replace(' ', '_').lower()}.jpg"
            )

        return None
