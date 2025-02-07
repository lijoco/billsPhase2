class Product:
    def __init__(self, castle_id, name, price, description, image_url):
        self.castle_id = castle_id
        self.name = name
        self.price = float(price)
        self.description = description
        self.image_url = image_url

    def __repr__(self):
        return f"Product(castle_id={self.castle_id}, name={self.name}, price={self.price}, description={self.description}, image_url={self.image_url})"