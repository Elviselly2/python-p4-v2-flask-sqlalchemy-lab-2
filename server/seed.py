#!/usr/bin/env python3

from app import app, db
from models import Customer, Review, Item  # ✅ Ensure correct import path

with app.app_context():  # ✅ Ensures Flask is properly linked to SQLAlchemy
    # Clear previous entries
    db.session.query(Review).delete()
    db.session.query(Customer).delete()
    db.session.query(Item).delete()

    # Seed Customers
    customer1 = Customer(name='Tal Yuri')
    customer2 = Customer(name='Raha Rosario')
    customer3 = Customer(name='Luca Mahan')
    db.session.add_all([customer1, customer2, customer3])
    db.session.commit()

    # Seed Items
    item1 = Item(name='Laptop Backpack', price=49.99)
    item2 = Item(name='Insulated Coffee Mug', price=9.99)
    item3 = Item(name='6 Foot HDMI Cable', price=12.99)
    db.session.add_all([item1, item2, item3])
    db.session.commit()

    # Seed Reviews with Correct Foreign Keys
    review1 = Review(comment="zipper broke the first week", customer_id=customer1.id, item_id=item1.id)
    review2 = Review(comment="love this backpack!", customer_id=customer2.id, item_id=item1.id)
    review3 = Review(comment="coffee stays hot for hours!", customer_id=customer1.id, item_id=item2.id)
    review4 = Review(comment="best coffee mug ever!", customer_id=customer3.id, item_id=item2.id)
    review5 = Review(comment="cable too short", customer_id=customer3.id, item_id=item3.id)

    db.session.add_all([review1, review2, review3, review4, review5])
    db.session.commit()
