from App.dao.ProductDAO import ProductDAO

class ProductService:
    def __init__(self):
        self.dao = ProductDAO()


    def get_all_products(self):
        return self.dao.getAllProducts()

    def get_product_by_id(self, product_id):
        return self.dao.getProductById(product_id)