from database import init_db, SessionLocal
from flask import Flask
from src.client.clientController import client_bp
from src.priceList.priceListController import price_list_bp, item_price_list_bp
from src.product.productController import product_bp
from src.ticket.ticketController import ticket_bp

app = Flask(__name__)
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  
app.register_blueprint(client_bp)
app.register_blueprint(price_list_bp)
app.register_blueprint(item_price_list_bp)
app.register_blueprint(product_bp)
app.register_blueprint(ticket_bp)

def main():
    init_db()
    
if __name__ == "__main__":
    main()
    app.run(debug=True)