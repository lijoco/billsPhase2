class User:
    def __init__(self, user_id, first_name, last_name, email, password, user_type):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.user_type = user_type

    def is_admin(self):
        return self.user_type == 'admin'

    def __repr__(self):
        return f"User(first_name={self.first_name}, email={self.email}, user_type={self.user_type})"