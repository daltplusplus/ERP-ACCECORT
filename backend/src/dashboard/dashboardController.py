from flask import Blueprint, jsonify, request
from src.utils.container import dashboardService
from src.utils.unitOfWork import UnitOfWork
from database import SessionLocal
from dataclasses import asdict

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard', methods=['GET'])
def get_products():
    uow = UnitOfWork(SessionLocal)
    with uow as u:
        data  = dashboardService.summary(u.session)
        return jsonify(asdict(data))


