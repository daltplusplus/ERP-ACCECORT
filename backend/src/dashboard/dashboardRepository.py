from sqlalchemy.orm import Session
from sqlalchemy import select, func, desc
from datetime import datetime
from dateutil.relativedelta import relativedelta
from src.ticket.ticket import Ticket, ItemTicket, TicketState
from src.client.client import Client
from src.dashboard.dashboard import TopClientDTO

class DashboardRepository:
    def set_session(self, session):
        self.session = session

    # Tickets promedio
    def average_ticket(self, since: datetime, until: datetime):
        subq = (
            select(Ticket.total)
            .join(ItemTicket)
            .where(
                Ticket.date.between(since, until),
                Ticket.state != TicketState.CANCELED
            )
            .group_by(Ticket.id)
            .having(func.count(ItemTicket.id) > 0)
            .subquery()
        )

        stmt = select(func.avg(subq.c.total))
        return self.session.execute(stmt).scalar() or 0

    # Cantidad total de Tickets
    def valid_tickets_subquery(self, since, until):
        return (
            select(Ticket.id, Ticket.total, Ticket.client_id)
            .join(ItemTicket)
            .where(
                Ticket.date.between(since, until),
                Ticket.state != TicketState.CANCELED
            )
            .group_by(Ticket.id)
            .having(func.count(ItemTicket.id) > 0)
            .subquery()
        )

    # Top Clients
    def top_clients(self, since: datetime, until: datetime, limit: int = 5):
        tickets_subq = (
            select(
                Ticket.id.label("ticket_id"),
                Ticket.client_id,
                Ticket.total
            )
            .join(ItemTicket, ItemTicket.ticket_id == Ticket.id)
            .where(
                Ticket.date.between(since, until),
                Ticket.state != TicketState.CANCELED
            )
            .group_by(Ticket.id)
            .having(func.count(ItemTicket.id) > 0)
            .subquery()
        )

        stmt = (
            select(
                Client.id,
                Client.name,
                func.sum(tickets_subq.c.total).label("total")
            )
            .join(tickets_subq, tickets_subq.c.client_id == Client.id)
            .group_by(Client.id, Client.name)
            .order_by(desc("total"))
            .limit(limit)
        )

        rows = self.session.execute(stmt).all()

        return [
            TopClientDTO(
                client_id=row.id,
                name=row.name,
                total=row.total
            )
            for row in rows
        ]


    def tickets_amount(self, since: datetime, until: datetime):
        subq = (
            select(Ticket.id)
            .join(ItemTicket, ItemTicket.ticket_id == Ticket.id)
            .where(
                Ticket.date.between(since, until),
                Ticket.state != TicketState.CANCELED
            )
            .group_by(Ticket.id)
            .having(func.count(ItemTicket.id) > 0)
            .subquery()
        )

        stmt = select(func.count(subq.c.id))
        return self.session.execute(stmt).scalar() or 0
    
    def total_sales(self, since: datetime, until: datetime) -> float:
        subq = (
            select(
                Ticket.id,
                Ticket.total
            )
            .join(ItemTicket, ItemTicket.ticket_id == Ticket.id)
            .where(
                Ticket.date.between(since, until),
                Ticket.state != TicketState.CANCELED
            )
            .group_by(Ticket.id)
            .having(func.count(ItemTicket.id) > 0)
            .subquery()
        )

        stmt = select(func.coalesce(func.sum(subq.c.total), 0.0))
        return self.session.execute(stmt).scalar()


    # Crecimiento vs mes anterior (mismo período)
    def grow_vs_last_month(self, since: datetime, until: datetime):
        period = until - since
        since_prev = since - relativedelta(months=1)
        until_prev = since_prev + period

        actual = self.total_sales(since, until)
        last = self.total_sales(since_prev, until_prev)

        if last == 0:
            return 0.0

        return round(((actual - last) / last) * 100, 2)
