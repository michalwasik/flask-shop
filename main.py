from flask import render_template, request, Flask
from model import *
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Session = sessionmaker(bind=engine)
session = Session()
app=Flask(__name__)


@app.route('/')
def index():
    return 'Hello world'


@app.route('/admin/delivery', methods=['GET', 'POST'])
def delivery():
    new_delivery = Product(name=request.form['product'], amount=request.form['quantity'])
    exists = session.query(Product.name).filter_by(name=new_delivery.name).first() is not None



if __name__ == '__main__':
    app.run(debug=True)