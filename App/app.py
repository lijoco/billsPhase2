# This is the current version 07/02/2025 00:44 Everything works

# May need to remove username from user DAO

from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from service.ProductService import ProductService
from model.forms import RegistrationForm, LoginForm
import sqlite3
import io

app = Flask(__name__)
FLASK_DEBUG = False
app.config['SECRET_KEY'] = 'some_long_random_string'


productService = ProductService()
@app.route('/')
def index():  # put application's code here
    products = productService.get_all_products()
    return render_template('index.html', products = products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = productService.get_product_by_id(product_id)
    return render_template('ProductDetails.html', product=product)

@app.route('/about')
def about():
    return render_template('about.html')

# Route for user registration, displaying the form and handling submission
# Not working fully just yet. Included it so you can see where I'm going with things for the second project.
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)

# Route for user login, displaying the form and handling submission
# Not working fully just yet. Included it to show additional features.
# Sample log in details: email: admin@blog.com password: password
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/adminHomepage')
def adminhp():
    return render_template('adminHomepage.html')

@app.route('/basket')
def basket():
    return render_template('basket.html')

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Access rows as dictionaries
    return conn

# Home page to display all items
@app.route('/adminCRUD')
def adminCRUD():
    conn = get_db_connection()
    products = conn.execute('SELECT id, name, price, description FROM products').fetchall()
    conn.close()
    return render_template('adminCRUD.html', products=products)

# Add or Edit an item
@app.route('/edit/<int:id>', methods=('GET', 'POST'))
@app.route('/add', methods=('GET', 'POST'), defaults={'id': None})
def edit(id):
    conn = get_db_connection()

    # If editing, fetch item
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
            conn.execute('INSERT INTO products (name, price = ?, description, image) VALUES (?, ?, ?, ?)',
                         (name, price, description, image_data))

        conn.commit()
        conn.close()
        return redirect(url_for('adminCRUD'))

    conn.close()
    return render_template('edit.html', product=product)

# Delete an item
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM products WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('adminCRUD'))

# Fetch image from database
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
