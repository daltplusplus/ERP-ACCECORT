from dataclasses import dataclass

@dataclass
class TopClientDTO:
    client_id: int
    name: str
    total: float

@dataclass
class DashboardDTO:
    average: float
    ticketsAmount: float
    total: float
    grow: float
    top_clients: list[TopClientDTO]
    
