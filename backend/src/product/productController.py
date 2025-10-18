from flask import Blueprint, jsonify, request
from src.product.product import Product
from src.utils.container import productService, priceListService, itemPriceListService
from src.utils.unitOfWork import UnitOfWork
from database import SessionLocal

product_bp = Blueprint('product', __name__)

@product_bp.route('/products', methods=['GET'])
def get_products():
    uow = UnitOfWork(SessionLocal)
    with uow as u:
        products = productService.list_products(u.session)
        return jsonify([p.to_dict() for p in products])


@product_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = productService.get_product(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify(product.to_dict())


@product_bp.route('/products', methods=['POST'])
def create_product():
    uow = UnitOfWork(SessionLocal)
    with uow as u:
        data = request.get_json()
        name = data.get('name')
        if not name:
            return jsonify({'error': 'Product name is required'}), 400

        product = productService.create_product(u.session, name)
        priceListService.add_product_to_all(u.session, product)
        return jsonify(product.to_dict()), 201


@product_bp.route('/products/<int:product_id>', methods=['PATCH'])
def update_product(product_id):
    data = request.get_json()
    name = data.get('name')

    uow = UnitOfWork(SessionLocal)
    with uow as u:
        if not name:
            return jsonify({'error': 'Product name is required'}), 400

        updated = productService.update_product(u.session, product_id, name)
        if not updated:
            return jsonify({'error': 'Product not found'}), 404
        return jsonify(updated.to_dict())


@product_bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    uow = UnitOfWork(SessionLocal)
    with uow as u:
        deleted = productService.delete_product(u.session, product_id)
        if not deleted:
            return jsonify({'error': 'Product not found'}), 404
        return jsonify({'message': 'Deleted'})
