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
    cookie_expired = Column(DateTime, nullable=True)
    customer_email = Column(String, ForeignKey('customer.email'))


class Customer(Base):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)

    orders = relationship('Order', backref='customer')
    acc_data  = relationship('Account_data', backref='customer')


class Association(Base):
    __tablename__ = 'association'

    order_id = Column(Integer, ForeignKey('order.id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), primary_key=True)
    quantity = Column(Integer)

    order = relationship("Order", backref="order_associations")
    product = relationship("Product", backref="product_associations")


class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)
    order_date = Column(DateTime, nullable=False, default=datetime.utcnow())
    coupon = Column(String, nullable=True)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)

    products = relationship('Product', secondary="association")


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    price = Column(Integer, nullable=False)
    amount = Column(Integer)


Base.metadata.create_all(engine)  # create db
