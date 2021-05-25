from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

engine = create_engine('sqlite:///shop.db', connect_args={'check_same_thread': False})
Base = declarative_base()


class Account_data(Base):
    __tablename__= 'account_data'

    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False, unique=True)
    hashed_password = Column(Integer, nullable=False, unique=True)
    login_cookie = Column(String, nullable=True, unique=True)
    customer_email = Column(String, ForeignKey('customer.email'))


class Customer(Base):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)

    orders = relationship('Order', backref='customer')
    acc_data  = relationship('Account_data', backref='customer')


class Orderproduct(Base):
    __tablename__ = 'orderproduct'

    order_id = Column(Integer, ForeignKey('order.id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), primary_key=True)
    name = Column(String)
    price = Column(Integer)
    amount = Column(Integer)

    order = relationship("Order", backref="order_product")
    product = relationship("Product", backref="product_order")


class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)
    order_date = Column(DateTime, nullable=False, default=datetime.utcnow())
    coupon = Column(String, nullable=True)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)

    products = relationship('Product', secondary="orderproduct")


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False, unique=True)
    price = Column(Float, nullable=False)
    amount = Column(Integer)
    shu = Column(Integer)


Base.metadata.create_all(engine)  # create db
