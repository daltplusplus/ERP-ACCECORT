from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from base import Base
from src.client import client
#from project.shared.database import Base


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer,primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }