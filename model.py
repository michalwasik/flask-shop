from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

engine = create_engine('sqlite:///shop.db', connect_args={'check_same_thread': False})
Base = declarative_base()


class Customer(Base):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    orders = relationship('Order', backref='customer')


class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    order_date = Column(DateTime, nullable=False, default=datetime.utcnow())
    coupon = Column(String)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    products = relationship('Product', secondary='Association')


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    price = Column(Integer, nullable=False)
    amount = Column(Integer)


class Association(Base):
    __tablename__ = 'association'
    order_id = Column(Integer, ForeignKey('order.id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), primary_key=True)

# Base.metadata.create_all(engine)  create db
