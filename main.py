from flask import render_template, request, Flask
from model import *
from sqlalchemy.orm import sessionmaker
from schema import Schema, And, Or, Optional, Use
from datetime import datetime

Session = sessionmaker(bind=engine)
session = Session()
app=Flask(__name__)


@app.route('/')
def index():
    return 'Hello world'


@app.route('/admin/delivery', methods=['GET', 'POST'])
def delivery():
    if request.method == 'POST':
        new_item = False
        data = request.form.to_dict()
        if 'choice-radio' in data:
            new_item = True
            data.pop('choice-radio')
        product_schema = Schema({'product': str, 'quantity': And(Use(int), lambda n: n > 0),
                                 Optional('price'): Use(float)})
        valid_data = product_schema.validate(data)
        print(valid_data)
        if new_item:
            add_new_product(valid_data)
        else:
            pass
    return render_template('inventory.html')


def add_new_product(data):
    new_product = Product(name=data['product'], amount=data['quantity'], price=data['price'])
    session.add(new_product)
    session.commit()


def update_product_quantity(data):
    pass


if __name__ == '__main__':
    app.run(debug=True)