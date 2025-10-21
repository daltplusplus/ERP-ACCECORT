from sqlalchemy.orm import Session, joinedload
from src.priceList.priceList import PriceList, ItemPriceList

class PriceListRepository:
    def set_session(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(PriceList).all()

    def get_by_id(self, list_id: int):
        return self.session.query(PriceList).filter(PriceList.id == list_id).first()

    def create(self, session, price_list: PriceList):
        session.add(price_list)
        session.flush()
        session.refresh(price_list)
        return price_list

    def delete(self, session, price_list: PriceList):
        session.delete(price_list)

    def get_by_client_id(self, client_id: int):
        return self.session.query(PriceList).options(
            joinedload(PriceList.items).joinedload(ItemPriceList.product)
        ).filter(PriceList.client_id == client_id).first()
    
    def save(self, priceList):
        self.session.add(priceList)
        self.session.flush()
        self.session.refresh(priceList)
        return priceList


class ItemPriceListRepository:
    def set_session(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(ItemPriceList).all()

    def get_by_id(self, item_id: int):
        return self.session.query(ItemPriceList).filter(ItemPriceList.id == item_id).first()
    
    def get_by_product(self, product_id):
        return self.session.query(ItemPriceList).filter(ItemPriceList.product_id ==product_id ).all()
    
    def get_all_by_list_id(self, list_id):
        return self.session.query(ItemPriceList).filter(ItemPriceList.list_id ==list_id ).all()

    def create(self, item: ItemPriceList):
        self.session.add(item)
        self.session.flush()
        self.session.refresh(item)
        return item

    def update(self, item: ItemPriceList):
        merged_item = self.session.merge(item)
        self.session.refresh(merged_item)
        return merged_item

    def delete(self, item: ItemPriceList):
        self.session.delete(item)

    def save(self, item):
        self.session.add(item)
        self.session.flush()
        self.session.refresh(item)
        return item
