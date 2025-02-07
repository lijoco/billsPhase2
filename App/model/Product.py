class Product:
    def __init__(self, product_id, name, price, description, image_url):
        self.product_id = product_id
        self.name = name
        self.price = float(price)
        self.description = description
        self.image_url = image_url

    def __repr__(self):
        return f"Product(castle_id={self.product_id}, name={self.name}, price={self.price}, description={self.description}, image_url={self.image_url})"