from src.priceList.priceList import ItemPriceList, PriceList
from src.priceList.priceListRepository import ItemPriceListRepository, PriceListRepository
from src.product.productService import ProductService
from src.client.client import Client

class ItemPriceListService:
    def __init__(self, repository: ItemPriceListRepository):
        self.repository = repository

    def list_items(self, session):
        self.repository.set_session(session)
        return self.repository.get_all()

    def get_item(self, item_id: int, session):
        self.repository.set_session(session)
        return self.repository.get_by_id(item_id)

    def create_item(self, price_list: PriceList, product, price: float, session):
        self.repository.set_session(session)
        item = ItemPriceList(list=price_list, product=product, price=price)
        self.repository.save(item)
        return item

    def update_item_price(self,session, item_id: int, new_price: float):
        self.repository.set_session(session)
        item = self.repository.get_by_id(item_id)
        if not item:
            return None
        item.price = new_price
        self.repository.update(item)
        return item
    
    def global_increase_by_percentage(self,session, percentage: int):
        self.repository.set_session(session)
        items = self.repository.get_all()

        for item in items:
            item.price = item.price * (1.0 + percentage/100.0)
            self.repository.update(item)
        return items

    def delete_item(self, item_id: int, session):
        self.repository.set_session(session)
        item = self.repository.get_by_id(item_id)
        if not item:
            return None
        self.repository.delete(item)
        return item
    
    


class PriceListService:
    def __init__(self, priceListRepository: PriceListRepository, 
                 itemPriceListService: ItemPriceListService, productService: ProductService):
        self.priceListRepository = priceListRepository
        self.itemPriceListService = itemPriceListService
        self.productService = productService

    def list_price_lists(self, session):
        self.priceListRepository.set_session(session)
        return self.priceListRepository.get_all(session)

    def get_price_list(self, list_id: int):
        with self.uow_factory() as uow:
            self.priceListRepository.set_session(uow.session)
            return self.priceListRepository.get_by_id(list_id)

    def create_price_list(self,session, client: Client):
        self.priceListRepository.set_session(session)

        price_list = PriceList(client=client)
        self.priceListRepository.save(price_list)

        # Crear items con la misma sesión
        products = self.productService.list_products(session)
        for p in products:
            self.itemPriceListService.create_item(price_list, p, 0, session=session)

        return price_list

    def delete_price_list(self, list_id: int):
        with self.uow_factory() as uow:
            self.priceListRepository.set_session(uow.session)
            price_list = self.priceListRepository.get_by_id(list_id)
            if not price_list:
                return None
            self.priceListRepository.delete(price_list)
            return price_list

    def get_price_list_by_client_id(self, session, client_id: int):
        self.priceListRepository.set_session(session)
        return self.priceListRepository.get_by_client_id(client_id)

    def get_items(self, list_id: int):
        with self.uow_factory() as uow:
            self.priceListRepository.set_session(uow.session)
            price_list = self.priceListRepository.get_by_id(list_id)
            if not price_list:
                return None
            return price_list.items
        
    def add_product_to_all(self, session, product):
        self.priceListRepository.set_session(session)
        lists = self.list_price_lists(session)
        for list in lists:
            self.itemPriceListService.create_item(list, product, 0, session)
        return lists
