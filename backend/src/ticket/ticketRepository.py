from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, func, desc
from src.ticket.ticket import Ticket, ItemTicket 
from src.client.client import Client

class TicketRepository:
    def set_session(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(Ticket).all()

    def get_by_id(self, ticket_id: int):
        return self.session.query(Ticket).options(
            joinedload(Ticket.items).joinedload(ItemTicket.itemPriceList)
        ).filter(Ticket.id == ticket_id).first()
    
    def get_by_client_id(self, client_id: int):
        return self.session.query(Ticket).options(
            joinedload(Ticket.items).joinedload(ItemTicket.itemPriceList)
        ).filter(Ticket.client_id == client_id).all()

    def save(self, ticket: Ticket):
        self.session.add(ticket)
        self.session.flush()
        self.session.refresh(ticket)
        return ticket

    def delete(self, ticket: Ticket):
        self.session.delete(ticket)

    def update(self, ticket):
        existing = self.get_by_id(ticket.id)
        if not existing:
            raise ValueError(f"Producto con id={ticket.id} no existe")
        
        updated = self.session.merge(ticket)   # sincroniza los cambios
        self.session.flush()
        self.session.refresh(updated)
        return updated
    
    def get_by_month_and_client(self, since, until, client_id):
        return (
            self.session.query(Ticket)
            .options(
                joinedload(Ticket.items)
                    .joinedload(ItemTicket.itemPriceList)
            )
            .filter(
                Ticket.client_id == client_id,
                Ticket.date.between(since, until)
            )
            .order_by(desc(Ticket.date))
            .all()
        )


    
    def get_by_month(self, since, until):
        return self.session.query(Ticket).options(
            joinedload(Ticket.items).joinedload(ItemTicket.itemPriceList)
        ).filter(Ticket.date.between(since, until)).order_by(desc(Ticket.date)).all()
    

class ItemTicketRepository:
    def set_session(self, session):
        self.session = session

    def create(self, item: ItemTicket):
        self.session.add(item)
        self.session.flush()
        self.session.refresh(item)
        return item
    
    def delete(self, item: ItemTicket):
        self.session.delete(item)