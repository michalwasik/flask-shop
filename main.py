from flask import render_template, request, Flask, make_response, session, redirect, url_for
from model import *
from sqlalchemy.orm import sessionmaker
import hashlib
from my_schema import product_schema, customer_schema, login_schema

# from datetime import datetime


Session = sessionmaker(bind=engine)
session = Session()
app = Flask(__name__)


@app.route('/admin/delivery', methods=['GET', 'POST'])
def delivery():
    if request.method == 'POST':
        data = request.form.to_dict()
        data.setdefault('price', 0)
        valid_data = product_schema.validate(data)
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form.to_dict()
        valid_login = login_schema.validate(data)
        client = session.query(Account_data).filter_by(login=valid_login['login']).first()
        if client:
            pw_match = password_check(valid_login['password'], client.hashed_password)
            if pw_match:
                res = make_response('Successfully logged in!')
                res.set_cookie('username', bytes(client.id))
                print(type(client.id), client.login)
            else:
                res = make_response('Wrong password')
        else:
            res = make_response('Wrong login')
        return res

    return render_template('login.html')


def password_check(password, og_password):
    return get_hashed_pw(password) == og_password

@app.route('/')
def items():
    all_items = session.query(Product).all()
    return render_template('index.html', data=all_items)


if __name__ == '__main__':
    app.run(debug=True)
