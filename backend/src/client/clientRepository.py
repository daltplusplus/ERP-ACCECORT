from sqlalchemy.orm import Session
from src.client.client import Client 

class ClientRepository:

    def set_session(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(Client).all()

    def get_by_id(self, list_id: int):
        return self.session.query(Client).filter(Client.id == list_id).first()

    def create(self, client: Client):
        self.session.add(client)
        self.session.flush()
        self.session.refresh(client)
        return client

    def delete(self, client: Client):
        self.session.delete(client)

    def save(self, client):
        self.session.add(client)
        self.session.flush()
        self.session.refresh(client)
        return client
