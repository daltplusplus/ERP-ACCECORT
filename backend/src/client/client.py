from sqlalchemy import Column, Integer, String, DateTime
from base import Base

class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer,primary_key=True)
    name = Column(String)
    adress = Column(String)
    phone = Column(String)

    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'adress': self.adress,
            'phone': self.phone
        }


