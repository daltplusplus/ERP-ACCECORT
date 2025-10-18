# src/service/ticket_service.py

from src.ticket.ticket import Ticket, ItemTicket, TicketState, TicketDTO, ItemTicketDTO
from src.ticket.ticketRepository import TicketRepository, ItemTicketRepository
from src.client.clientService import ClientService
from datetime import datetime


class ItemTicketService:
    def __init__(self, item_repo: ItemTicketRepository):
        self.item_repo = item_repo
       

    def create_item(self, session, itemDTO : ItemTicketDTO, ticket: Ticket):
        item = ItemTicket(ticket, itemDTO.itemPriceListId, itemDTO.amount, itemDTO.unitPrice, itemDTO.subtotal)
        item.name = itemDTO.name
        self.item_repo.set_session(session)
        return self.item_repo.create(item)
    
    def delete_item(self, session, item):
        self.item_repo.set_session(session)
        return self.item_repo.delete(item)
    
class TicketService:
    def __init__(self, ticket_repo: TicketRepository, client_service: ClientService, item_sevice: ItemTicketService):
        self.ticket_repo = ticket_repo
        self.client_service = client_service
        self.item_service = item_sevice

    def create_ticket_by_client_id(self, session, client_id, discount):
        self.ticket_repo.set_session(session)
        client = self.client_service.get_client(session, client_id)
        if not client:
            raise ValueError("Cliente no encontrado")

        ticket = Ticket(client=client)
        ticket.date = datetime.now()
        self.ticket_repo.save(ticket)
        

        return ticket
    
    def update_ticket(self, session, ticket_id, ticketdto, itemsTicket):
        self.ticket_repo.set_session(session)
        ticket :Ticket = self.ticket_repo.get_by_id(ticket_id)

        for item in ticket.items:
            self.item_service.delete_item(session, item)

        ticket.discount = ticketdto.discount
        ticket.total = ticketdto.total
        ticket.subtotal = ticketdto.subtotal
        ticket.items = []

        for item in itemsTicket:
            newItem = self.item_service.create_item(session, item, ticket)
            ticket.items.append(newItem)

        return self.ticket_repo.update(ticket)
        

    def get_ticket_by_id(self, session, id):
        self.ticket_repo.set_session(session)
        return self.ticket_repo.get_by_id(id)
    
    def get_ticket_by_client_id(self, session, id):
        self.ticket_repo.set_session(session)
        return self.ticket_repo.get_by_client_id(id)


        
