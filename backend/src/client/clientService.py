from src.client.client import Client
from src.client.clientRepository import ClientRepository
from src.priceList.priceListService import PriceListService
from src.priceList.priceList import PriceList

class ClientService:
    def __init__(self, repository: ClientRepository, priceListService: PriceListService):
        self.repository = repository
        self.priceListService = priceListService

    def list_clients(self, session):
        self.repository.set_session(session)
        return self.repository.get_all()

    def get_client(self, session, client_id: int):
        self.repository.set_session(session)
        return self.repository.get_by_id(client_id)

    def create_client(self, name: str, address: str, phone: str, session):
        self.repository.set_session(session)
        client = Client(name=name)
        client.adress = address
        client.phone = phone
        
        self.priceListService.create_price_list(session,client=client)
        self.repository.save(client)
        return client

    def update_client(self, client_id: int, name: str = None, address: str = None, phone: str = None):
        with self.uow_factory() as uow:
            self.repository.set_session(uow.session)
            client = self.repository.get_by_id(client_id)
            if not client:
                return None
            if name:
                client.name = name
            if address:
                client.adress = address
            if phone:
                client.phone = phone
            self.repository.update(client)
            return client

    def delete_client(self, client_id: int):
        with self.uow_factory() as uow:
            self.repository.set_session(uow.session)
            client = self.repository.get_by_id(client_id)
            if not client:
                return None
            self.repository.delete(client)
            return client

    def get_client_prices(self,session, client_id: int):
        return self.priceListService.get_price_list_by_client_id(client_id=client_id, session=session).items
