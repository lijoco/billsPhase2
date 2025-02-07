# This is the current version 07/02/2025 00:44 Everything works
from flask import Flask, render_template, request, redirect, url_for, flash
from service.ProductService import ProductService
from model.forms import RegistrationForm, LoginForm

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
    print(f"Rendering ProductDetails.html for product_id: {product_id}")
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

if __name__ == '__main__':
    app.run(debug=True)
