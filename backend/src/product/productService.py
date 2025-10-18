from src.product.product import Product
from src.product.productRepository import ProductRepository

class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def list_products(self, session):
        self.repository.set_session(session)
        return self.repository.get_all()

    def get_product(self,session, product_id: int):
        self.repository.set_session(session)
        return self.repository.get_by_id(product_id)

    def create_product(self,session, name: str):
        product = Product(name=name)
        self.repository.set_session(session)
        self.repository.create(product)
        return product  

    def update_product(self, session, product_id: int, name: str):
        self.repository.set_session(session)
        product = self.repository.get_by_id(product_id)
        if not product:
            return None
        product.name = name
        self.repository.update(product)
        return product

    def delete_product(self, session, product_id: int):
        self.repository.set_session(session)
        product = self.repository.get_by_id(product_id)
        if not product:
            return None
        self.repository.delete(product)
        
        return product
