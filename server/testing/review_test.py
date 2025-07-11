from app import app, db
from server.models import Customer, Item, Review

class TestReview:
    '''Review model in models.py'''

    def test_can_be_instantiated(self):
        '''can be invoked to create a Python object.'''
        r = Review()
        assert r
        assert isinstance(r, Review)

    def test_has_comment(self):
        '''can be instantiated with a comment attribute.'''
        r = Review(comment='great product!')
        assert r.comment == 'great product!'

    def test_can_be_saved_to_database(self):
        '''can be added to a transaction and committed to review table with comment column.'''
        with app.app_context():
            assert 'comment' in Review.__table__.columns

            # Ensure customer & item exist
            customer = Customer.query.first()
            item = Item.query.first()

            if not customer or not item:
                customer = Customer(name="Alice")
                item = Item(name="Laptop", price=999.99)
                db.session.add_all([customer, item])
                db.session.commit()

            # Retrieve fresh instances to guarantee valid IDs
            customer = db.session.query(Customer).filter_by(name="Alice").first()
            item = db.session.query(Item).filter_by(name="Laptop").first()

            # Create a valid Review entry with assigned foreign keys
            r = Review(comment="great!", customer_id=customer.id, item_id=item.id)
            db.session.add(r)
            db.session.commit()

            assert hasattr(r, 'id')
            assert db.session.query(Review).filter_by(id=r.id).first()

    def test_is_related_to_customer_and_item(self):
        '''has foreign keys and relationships'''
        with app.app_context():
            assert 'customer_id' in Review.__table__.columns
            assert 'item_id' in Review.__table__.columns

            # Create valid instances with required attributes
            c = Customer(name="Bob")
            i = Item(name="Smartphone", price=799.99)
            db.session.add_all([c, i])
            db.session.commit()

            # Create valid Review entry
            r = Review(comment='great!', customer=c, item=i)
            db.session.add(r)
            db.session.commit()

            # Check foreign keys
            assert r.customer_id == c.id
            assert r.item_id == i.id
            # Check relationships
            assert r.customer == c
            assert r.item == i
            assert r in c.reviews
            assert r in i.reviews
