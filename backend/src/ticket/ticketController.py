# src/controller/ticket_controller.py

from flask import Blueprint, jsonify, request, send_file
from src.utils.container import ticketService, clientService
from src.ticket.ticket import Ticket, TicketDTO, ItemTicketDTO, ItemTicket
from src.utils.unitOfWork import UnitOfWork
from database import SessionLocal
from src.ticket.ticketPDFExporter import TicketPDFExporter
from dateutil.relativedelta import relativedelta
from datetime import datetime

ticket_bp = Blueprint("tickets", __name__)

@ticket_bp.route("/tickets", methods=["GET"])
def get_all_tickets():
    uow = UnitOfWork(SessionLocal)
    with uow as u:
        tickets = ticketService.get_tickets(u.session)
        return jsonify([i.to_dict() for i in tickets])

@ticket_bp.route("/tickets/<string:date>", methods=["GET"])
def get_tickets_by_month(date):
    uow = UnitOfWork(SessionLocal)
    with uow as u:
        dt = datetime.strptime(date, "%Y-%m")
        first_day = dt.replace(day=1)
        last_day = first_day + relativedelta(months=1) - relativedelta(seconds=1)
        tickets = ticketService.get_tickets(u.session, first_day, last_day, None)
        return jsonify([i.to_dict(include_client = True) for i in tickets])

@ticket_bp.route("/tickets/<string:date>/<int:client_id>", methods=["GET"])
def get_tickets(date, client_id):
    uow = UnitOfWork(SessionLocal)
    with uow as u:
        dt = datetime.strptime(date, "%Y-%m")
        first_day = dt.replace(day=1)
        last_day = first_day + relativedelta(months=1) - relativedelta(seconds=1)
        tickets = ticketService.get_tickets(u.session, first_day, last_day, client_id)
        return jsonify([i.to_dict(include_client = True) for i in tickets])
        

@ticket_bp.route("/tickets/<int:ticket_id>", methods=["GET"])
def get_ticket(ticket_id):
    uow = UnitOfWork(SessionLocal)
    with uow as u:
        ticket = ticketService.get_ticket_by_id(u.session, ticket_id)
        if ticket is None:
            return jsonify({"error": "Ticket not found"}), 404
        return jsonify(
            ticket.to_dict(include_items =True)
        )

@ticket_bp.route("/tickets", methods=["POST"])
def create_ticket():
    uow = UnitOfWork(SessionLocal)
    with uow as u:
        data = request.get_json()
        client_id = data.get("client_id")
        discount = data.get("discount", 0.0)

        ticket = ticketService.create_ticket_by_client_id(u.session, client_id, discount)
        if ticket is None:
            return jsonify({"error": "Client not found"}), 404

        return jsonify(
            ticket.to_dict(False, False)
        ), 201

@ticket_bp.route("/tickets/<int:ticket_id>", methods=["DELETE"])
def delete_ticket(ticket_id):
    success = ticketService.delete_ticket(ticket_id)
    if not success:
        return jsonify({"error": "Ticket not found"}), 404
    return jsonify({"message": "Ticket deleted successfully"})

@ticket_bp.route("/tickets/<int:ticket_id>", methods=["PATCH"])
def update_ticket(ticket_id):
    uow = UnitOfWork(SessionLocal)
    with uow as u:
        data = request.get_json()
        ticketdto = TicketDTO(discount=data.get("discount"), total=data.get("total"), subtotal=data.get("subtotal"), state=data.get("state"))
        itemsTicket = []

        items = data.get("items")
        if items:
            for item in items:
                newItem = ItemTicketDTO(unitPrice=item.get("unitPrice"), amount=item.get("amount"), itemPriceListId=item.get("itemPriceListId", 0), subtotal=item.get("subtotal"), name=item.get("name"))
                itemsTicket.append(newItem)

        updated_ticket = ticketService.update_ticket(u.session, ticket_id, ticketdto, itemsTicket)

        return jsonify(updated_ticket.to_dict()), 200

@ticket_bp.route('/tickets/client/<int:id>', methods=['GET'])
def get_client_prices(id):
    uow = UnitOfWork(SessionLocal)
    with uow as u:
        tickets = ticketService.get_ticket_by_client_id(u.session, id)
        return jsonify([i.to_dict() for i in tickets])

@ticket_bp.route("/tickets/<int:ticket_id>/pdf")
def generate_pdf(ticket_id):
    uow = UnitOfWork(SessionLocal)
    with uow as u:
        ticket = ticketService.get_ticket_by_id(u.session, ticket_id)
        client = clientService.get_client(u.session, ticket.client_id)
        exporter = TicketPDFExporter(ticket.to_dict(), client.to_dict())
        pdf_buffer = exporter.generar_pdf()
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=f"boleta_{ticket_id}.pdf",
            mimetype="application/pdf"
        )
        