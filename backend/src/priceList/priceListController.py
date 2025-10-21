from flask import Blueprint, jsonify, request
from src.priceList.priceList import PriceList, ItemPriceList, PriceListDTO
from src.product.product import Product
from src.client.client import Client
from src.utils.container import itemPriceListService, priceListService
from src.utils.unitOfWork import UnitOfWork
from database import SessionLocal

price_list_bp = Blueprint('price_list', __name__)
item_price_list_bp = Blueprint('item_price_list', __name__)


@price_list_bp.route('/price-lists', methods=['GET'])
def get_price_lists():
    uow = UnitOfWork(SessionLocal)
    with uow as u:
        lists = priceListService.list_price_lists(u.session)
        return jsonify([l.to_dict() for l in lists])
    



@price_list_bp.route('/price-lists/<int:list_id>', methods=['GET'])
def get_price_list(list_id):
    uow = UnitOfWork(SessionLocal)
    with uow as u:
        price_list = priceListService.get_price_list(u.session, list_id)
        if not price_list:
            return jsonify({'error': 'Price list not found'}), 404
        return jsonify(price_list.to_dict())
    
@price_list_bp.route('/price-lists/<int:list_id>/items', methods=['GET'])
def get_price_list_items(list_id):
    uow = UnitOfWork(SessionLocal)
    with uow as u:
        items = itemPriceListService.list_items_by_list(u.session, list_id)
        if not items:
            return jsonify({'error': 'Price list not found'}), 404
        return jsonify([i.to_dict() for i in items])


@price_list_bp.route('/price-lists', methods=['POST'])
def create_price_list():
    uow = UnitOfWork(SessionLocal)
    with uow as u:
        data = request.get_json()
                
        price_list = priceListService.create_price_list(u.session, data.get('name'))
        return jsonify(price_list.to_dict()), 201


@price_list_bp.route('/price-lists/<int:list_id>', methods=['DELETE'])
def delete_price_list(list_id):
    deleted = priceListService.delete_price_list(list_id)
    if not deleted:
        return jsonify({'error': 'Price list not found'}), 404
    return jsonify({'message': 'Deleted'})


@item_price_list_bp.route('/items', methods=['GET'])
def get_items():
    items = itemPriceListService.list_items()
    return jsonify([i.to_dict() for i in items])


@item_price_list_bp.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = itemPriceListService.get_item(item_id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    return jsonify(item.to_dict())


@item_price_list_bp.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    price_list_id = data.get('price_list_id')
    product_id = data.get('product_id')
    price = data.get('price')

    if None in [price_list_id, product_id, price]:
        return jsonify({'error': 'Missing data'}), 400

    price_list = PriceList(id=price_list_id)
    product = Product(id=product_id)
    item = itemPriceListService.create_item(price_list, product, price)
    return jsonify(item.to_dict()), 201


@item_price_list_bp.route('/items/<int:item_id>', methods=['PATCH'])
def update_item(item_id):
    uow = UnitOfWork(SessionLocal)
    with uow as u:
        data = request.get_json()
        new_price = data.get('price')
        if new_price is None:
            return jsonify({'error': 'price is required'}), 400

        updated = itemPriceListService.update_item_price(u.session, item_id, new_price)
        if not updated:
            return jsonify({'error': 'Item not found'}), 404
        return jsonify(updated.to_dict())


@item_price_list_bp.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    deleted = itemPriceListService.delete_item(item_id)
    if not deleted:
        return jsonify({'error': 'Item not found'}), 404
    return jsonify({'message': 'Deleted'})

@item_price_list_bp.route('/items', methods=['PATCH'])
def globa_item_increase():
    uow = UnitOfWork(SessionLocal)
    with uow as u:
        data = request.get_json()
        percentage = data.get('percentage')
        if percentage is None or percentage < 0:
            return jsonify({'error': 'invalid percentage'}), 400

        itemPriceListService.global_increase_by_percentage(u.session, percentage)
        return "aumento en " + str(percentage)

