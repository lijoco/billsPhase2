from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session
from service.ProductService import ProductService
from dao.UserDAO import UserDAO
from model.forms import RegistrationForm, LoginForm
import sqlite3
import io

app = Flask(__name__)
app.config['SECRET_KEY'] = 'some_long_random_string'  # Required for session management
app.config['FLASK_DEBUG'] = False  # Debug mode

# Initialize services and DAOs
product_service = ProductService()
user_dao = UserDAO()

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Access rows as dictionaries
    return conn

# Decorator to restrict access to admins
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is logged in and is an admin
        if 'user_type' not in session or session['user_type'] != 'admin':
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('index'))  # Redirect to home page or login page
        return f(*args, **kwargs)
    return decorated_function

# Route to Index
@app.route('/')
def index():
    products = product_service.get_all_products()
    return render_template('index.html', products=products)

# Route to Product Detail Page
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = product_service.get_product_by_id(product_id)
    return render_template('ProductDetails.html', product=product)

# Route to About Page
@app.route('/about')
def about():
    return render_template('about.html')

# Route for User Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if user_dao.create_user(form.first_name.data, form.last_name.data, form.email.data, form.password.data, user_type='customer'):
            flash(f'Account created for {form.first_name.data} {form.last_name.data}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Email already in use. Account creation failed. Please try again.', 'danger')
    return render_template('register.html', title='Register', form=form)

# Route for User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = user_dao.get_user_by_email(form.email.data)

        if user and user.password == form.password.data:  # Check if user exists and password matches
            # Store user information in the session
            session['user_id'] = user.user_id
            session['first_name'] = user.first_name
            session['user_type'] = user.user_type  # Store user type

            if user.user_type == 'customer':
                flash('You have been logged in as a customer!', 'success')
                return redirect(url_for('index'))
            elif user.user_type == 'admin':
                flash('You have been logged in as an admin!', 'success')
                return redirect(url_for('adminhp'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', title='Login', form=form)

# Route to Log out
@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

# Route to Admin Homepage
@app.route('/adminHomepage')
@admin_required  # Restrict access to admins
def adminhp():
    conn = get_db_connection()
    products = conn.execute('SELECT id, name, price, description FROM products').fetchall()
    conn.close()
    return render_template('adminHomepage.html', products=products)

# Route to Basket Page
@app.route('/basket')
def basket():
    return render_template('basket.html')

# Route to Add or Edit an Item
@app.route('/edit/<int:id>', methods=('GET', 'POST'))
@app.route('/add', methods=('GET', 'POST'), defaults={'id': None})
def edit(id):
    conn = get_db_connection()

    # Fetch product if editing
    product = None
    if id:
        product = conn.execute('SELECT * FROM products WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        image = request.files['image']

        image_data = None
        if image and image.filename != '':
            image_data = image.read()  # Convert file to BLOB

        if id:  # Update existing item
            if image_data:
                conn.execute('UPDATE products SET name = ?, price = ?, description = ?, image = ? WHERE id = ?',
                             (name, price, description, image_data, id))
            else:
                conn.execute('UPDATE products SET name = ?, price = ?, description = ? WHERE id = ?',
                             (name, price, description, id))
        else:  # Insert new item
            conn.execute('INSERT INTO products (name, price, description, image) VALUES (?, ?, ?, ?)',
                         (name, price, description, image_data))

        conn.commit()
        conn.close()
        return redirect(url_for('adminCRUD'))

    conn.close()
    return render_template('edit.html', product=product)

# Route to Delete an Item
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM products WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('adminCRUD'))

# Route to Fetch Image from Database
@app.route('/image/<int:id>')
def get_image(id):
    conn = get_db_connection()
    product = conn.execute('SELECT image FROM products WHERE id = ?', (id,)).fetchone()
    conn.close()

    if product and product['image']:
        return send_file(io.BytesIO(product['image']), mimetype='image/jpeg')
    return '', 404  # Return 404 if no image is found

if __name__ == '__main__':
    app.run(debug=True)