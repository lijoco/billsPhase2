import sqlite3
from App.model.User import User
from werkzeug.security import generate_password_hash, check_password_hash

class UserDAO:
    def __init__(self):
        self.db_path = "database.db"  # Path to the SQLite database

    def get_db_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Access rows as dictionaries
        return conn

    def create_user(self, first_name, last_name, email, password, user_type='customer'):
        conn = self.get_db_connection()
        cursor = conn.cursor()

        # Hash the password when stored
        hashed_password = generate_password_hash(password)

        try:
            cursor.execute('''
                INSERT INTO users (first_name, last_name, email, password, user_type)
                VALUES (?, ?, ?, ?, ?)
            ''', (first_name, last_name, email, hashed_password, user_type))
            conn.commit()
        except sqlite3.IntegrityError:
            # Handle duplicate email (email is unique)
            # This isn't throwing an error on screen, its just stopping duplicates.
            return False
        finally:
            conn.close()

        return True

    def get_user_by_email(self, email):
        conn = self.get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return User(
                user_id=row['user_id'],
                first_name=row['first_name'],
                last_name=row['last_name'],
                email=row['email'],
                password=row['password'],
                user_type=row['user_type']
            )
        return None

    def verify_user(self, email, password):
        user = self.get_user_by_email(email)
        if user and password == user.password:
            return user
        return None