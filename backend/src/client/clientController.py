from flask import Blueprint, request, jsonify
from src.utils.container import clientService
from src.utils.unitOfWork import UnitOfWork
from src.client.client import Client, ClientDTO
from database import SessionLocal
client_bp = Blueprint('client_bp', __name__)

@client_bp.route('/clients', methods=['GET'])
def list_clients():
    uow = UnitOfWork(SessionLocal)
    with uow as u:
        clients = clientService.list_clients(u.session)
        return jsonify([p.to_dict() for p in clients])

@client_bp.route('/clients/<int:id>', methods=['GET'])
def get_client(id):
    uow = UnitOfWork(SessionLocal)
    with uow as u:
        client : Client = clientService.get_client(u.session, id)
        return client.to_dict()

@client_bp.route('/clients', methods=['POST'])
def create_client():
    uow = UnitOfWork(SessionLocal)
    with uow as u:
        data = request.json
        if not data.get('pricelist_id'):
            return jsonify({'error': 'no Pricelist selected'}), 404
        client = clientService.create_client(data['name'], data.get('address', ''), data.get('phone', ''), data.get('pricelist_id'), u.session)
        return jsonify({"id": client.id, "name": client.name}), 201

@client_bp.route('/clients/<int:id>/prices', methods=['GET'])
def get_client_prices(id):
    uow = UnitOfWork(SessionLocal)
    with uow as u:
        items = clientService.get_client_prices(u.session, id)
        return jsonify([i.to_dict() for i in items])
    
@client_bp.route('/clients/<int:id>', methods=['PATCH'])
def edit_client_info(id):
    uow = UnitOfWork(SessionLocal)
    with uow as u:
        data = request.get_json()
        dto = ClientDTO(
            adress=data.get('adress'),
            phone=data.get('phone'),
            name= data.get('name'),
            pricelist_id=data.get('pricelist_id'))
        client = clientService.update_client(u.session, client_id= id, dto=dto)
        return client.to_dict()


    
