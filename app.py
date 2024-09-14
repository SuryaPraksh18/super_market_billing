from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

# Import models from the models.py file
from models import Product, Customer, Transaction

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Admin dashboard
@app.route('/admin')
def admin():
    products = Product.query.all()
    return render_template('admin.html', products=products)

# Add a product (Admin function)
@app.route('/add_product', methods=['POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        stock = int(request.form['stock'])
        new_product = Product(name=name, price=price, stock=stock)
        db.session.add(new_product)
        db.session.commit()
        flash("Product added successfully!")
        return redirect(url_for('admin'))

# Billing page
@app.route('/billing')
def billing():
    products = Product.query.all()
    return render_template('billing.html', products=products)

# Update Cart
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.json
    product = Product.query.filter_by(id=data['product_id']).first()
    if product:
        transaction = Transaction(product_id=product.id, quantity=data['quantity'], total_price=product.price * data['quantity'])
        db.session.add(transaction)
        db.session.commit()
        return jsonify({"status": "success", "total_price": transaction.total_price})

# Reports Page
@app.route('/reports')
def reports():
    transactions = Transaction.query.all()
    return render_template('reports.html', transactions=transactions)

if __name__ == '__main__':
    app.run(debug=True)
