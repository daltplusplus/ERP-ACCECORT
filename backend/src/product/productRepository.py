from sqlalchemy.orm import Session
from src.product.product import Product

class ProductRepository:
    def set_session(self, session):
        self.session = session

    def create(self, product):
        self.session.add(product)
        self.session.flush() 
        self.session.refresh(product)
        return product

    def get_all(self):
        return self.session.query(Product).all()

    def get_by_id(self, product_id):
        return self.session.query(Product).get(product_id)

    def update(self, product):
        self.session.merge(product)
        return product

    def delete(self, product):
        self.session.delete(product)

    def save(self, product):
        self.session.add(product)
        self.session.flush()
        self.session.refresh(product)
        return product