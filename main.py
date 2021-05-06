from flask import render_template, request, Flask, make_response, session, redirect, url_for, flash
from model import *
from sqlalchemy.orm import sessionmaker
import hashlib
from my_schema import product_schema, customer_schema, login_schema
from secrets import token_hex
# from datetime import datetime


Session = sessionmaker(bind=engine)
session = Session()
app = Flask(__name__)
# secret_key generated using token_hex(16)
app.secret_key = '75e958ab19d6a176852e31c0a7a2dd18'


@app.route('/admin/delivery', methods=['GET', 'POST'])
def delivery():
    if request.method == 'POST':
        data = request.form.to_dict()
        print(data)
        data.setdefault('price', 0)
        valid_data = product_schema.validate(data)
        print(valid_data)
        if 'choice-radio' in data:
            add_new_product(valid_data)
        else:
            update_product_quantity(valid_data)
    return render_template('inventory.html')


def add_new_product(data):
    new_product = Product(name=data['product'], amount=data['quantity'], price=data['price'])
    session.add(new_product)
    session.commit()


def update_product_quantity(data):
    old_product = session.query(Product).filter_by(name=data['product']).first()
    old_product.amount += data['quantity']
    session.commit()


@app.route('/create_account', methods=['GET', 'POST'])
def new_customer():
    if request.method == 'POST':
        data = request.form.to_dict()
        valid_customer = customer_schema.validate(data)
        add_new_customer(valid_customer)
        return redirect(url_for('login'))
    return render_template('create_account.html')


# os.urandom(16)
my_salt = b'\xef\xd8\xb1-\xaa\xe8]\xf8H\x9eErS\xb5~\x13'


def get_hashed_pw(password, salt=my_salt):
    salted_pw = password.encode('utf-8') + salt
    return hashlib.sha256(salted_pw).hexdigest()


def add_new_customer(data):
    customer = Customer(first_name=data['fname'], last_name=data['lname'], email=data['email'])
    password = get_hashed_pw(data['password'])
    login_data = Account_data(login=data['login'], hashed_password=password, customer_email=customer.email)
    session.add(customer)
    session.add(login_data)
    session.commit()


def index_page(cookie=None):
    all_items = session.query(Product).all()
    res = make_response(render_template('index.html', data=all_items))
    if cookie:
        res.set_cookie('cookie_token', cookie)
    return res


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form.to_dict()
        valid_login = login_schema.validate(data)
        client = session.query(Account_data).filter_by(login=valid_login['login']).first()
        if client:
            pw_match = password_check(valid_login['password'], client.hashed_password)
            if pw_match:
                cookie_token = token_hex(16)
                client.login_cookie = cookie_token
                session.commit()
                flash('Successfully logged in')
                res = make_response(redirect('/'))
                res.set_cookie('cookie_token', cookie_token)
            else:
                res = make_response('Wrong password')
        else:
            res = make_response('Wrong login')
        return res
    return render_template('login.html')


@app.route('/logout')
def logout():
    res = make_response(redirect(url_for('login')))
    res.set_cookie('cookie_token', '', expires=0)
    return res


def password_check(password, og_password):
    return get_hashed_pw(password) == og_password


@app.route('/', methods=['GET', 'POST'])
def items():
    if request.method == 'POST':
        cookie_token = request.cookies.get('cookie_token')
        client = session.query(Account_data).filter_by(login_cookie=cookie_token).first()
        if not client:
            return redirect(url_for('login'))
        data = request.form.to_dict()
        data = {k: v for k, v in data.items() if v}
        purchase(data, client.customer_email)
    return index_page()


def purchase(items, email):
    user_id = session.query(Customer).filter_by(email=email).first().id
    products = session.query(Product).filter(Product.name.in_(items)).all()
    order = Order(customer_id=user_id, products=products)
    session.add(order)
    session.commit()
    for name in items:
        product = session.query(Product).filter_by(name=name).first()
        new_order = session.query(Orderproduct).filter_by(product_id=product.id, order_id=order.id).first()
        if product.amount < int(items[name]):
            flash(f'Max amount of {name} is {items[name]}')
            return index_page()
        product.amount -= int(items[name])
        new_order.amount = items[name]
        new_order.name = product.name
        new_order.price = product.price
        session.commit()

# to do:
#     - cookie expire date
#     - cookie token unique


if __name__ == '__main__':
    app.run(debug=True)
