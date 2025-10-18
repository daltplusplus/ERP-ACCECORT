from src.priceList.priceListService import PriceListService, ItemPriceListService
from src.priceList.priceListRepository import PriceListRepository, ItemPriceListRepository
from src.product.productService import ProductService
from src.product.productRepository import ProductRepository
from src.client.clientRepository import ClientRepository
from src.client.clientService import ClientService
from src.ticket.ticketRepository import TicketRepository, ItemTicketRepository
from src.ticket.ticketService import TicketService, ItemTicketService

priceListRepository = PriceListRepository()
itemPriceListRepository = ItemPriceListRepository()
productRepository = ProductRepository()
clientRepository = ClientRepository()
ticketRepository = TicketRepository()
itemTicketRepository = ItemTicketRepository()

itemTicketService = ItemTicketService(itemTicketRepository)
itemPriceListService = ItemPriceListService(itemPriceListRepository)
productService = ProductService(productRepository)
priceListService = PriceListService(priceListRepository, itemPriceListService, productService)
clientService = ClientService(clientRepository, priceListService)
ticketService = TicketService(ticketRepository, clientService, itemTicketService)
