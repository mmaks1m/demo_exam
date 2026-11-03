# models.py - ФИНАЛЬНАЯ версия
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)  # Автоинкремент через IDENTITY в БД
    role = Column(String(50))
    full_name = Column(String(100))
    login = Column(String(100))
    password = Column(String(100))
    
    orders = relationship("Order", back_populates="user")

class PickupPoint(Base):
    __tablename__ = 'pickup_points'
    
    id = Column(Integer, primary_key=True, index=True)  # Автоинкремент через IDENTITY в БД
    address = Column(String(255))
    
    orders = relationship("Order", back_populates="pickup_point")

class Product(Base):
    __tablename__ = 'items'
    
    article = Column("item_number", String(20), primary_key=True, index=True)
    name = Column(String(100))
    unit = Column("unit_measurement", String(20))
    price = Column("cost", Integer)
    supplier = Column("provider", String(100))
    manufacturer = Column(String(100))
    category = Column("item_category", String(50))
    discount = Column("current_discount", Integer)
    stock_quantity = Column("quantity_stock", Integer)
    description = Column(Text)
    image_path = Column("photo", String(255))
    
    order_items = relationship("OrderItem", back_populates="product")

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column("order_number", Integer, primary_key=True, index=True)  # Автоинкремент через IDENTITY в БД
    user_id = Column("id_user", Integer, ForeignKey('users.id'))
    order_date = Column(DateTime)
    delivery_date = Column(DateTime)
    pickup_point_id = Column("id_pickup_point", Integer, ForeignKey('pickup_points.id'))
    receive_code = Column("receipt_code", Integer)
    status = Column("order_status", String(20))
    
    user = relationship("User", back_populates="orders")
    pickup_point = relationship("PickupPoint", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = 'orders_items'

    order_id = Column("order_number", Integer, ForeignKey('orders.order_number'), primary_key=True)
    product_article = Column("item_number", String(20), ForeignKey('items.item_number'), primary_key=True)
    quantity = Column(Integer)

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")
