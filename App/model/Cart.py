from Product import Product
from User import User

class LineItem:
    def __init__(self, product, quantity):
        """
        Represents an item in a shopping basket or order.
        """
        if not isinstance(product, Product):
            raise ValueError("LineItem must reference a Product.")
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        self.product = product
        self.quantity = quantity
        self.total_price = self.product.price * self.quantity

    def __repr__(self):
        return f"LineItem(Product: {self.product.name}, Quantity: {self.quantity}, Total: ${self.total_price:.2f})"

class Basket:
    def __init__(self):
        """
        Represents a user's shopping basket.
        """
        self.items = []

    def add_item(self, product, quantity):
        """Adds an item to the basket."""
        self.items.append(LineItem(product, quantity))

    def remove_item(self, product_id):
        """Removes an item from the basket."""
        self.items = [item for item in self.items if item.product.product_id != product_id]

    def calculate_total(self):
        """Calculates the total price of items in the basket."""
        return sum(item.total_price for item in self.items)

    def get_number_of_items(self):
        return len(self.items)

    def __repr__(self):
        return f"Basket({self.items})"

class Transaction:
    def __init__(self, transaction_id, user, basket):
        """
        Represents a completed transaction.
        """
        if not isinstance(user, User):
            raise ValueError("Transaction must reference a User.")
        if not isinstance(basket, Basket):
            raise ValueError("Transaction must reference a Basket.")
        self.transaction_id = transaction_id
        self.user = user
        self.basket = basket
        self.total_amount = basket.calculate_total()

    def __repr__(self):
        return f"Transaction(ID: {self.transaction_id}, User: {self.user.first_name}, Total: ${self.total_amount:.2f})"
