from sqlalchemy import Column, Integer, BigInteger, String, Numeric, DateTime, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Transaction(Base, AsyncAttrs):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, nullable=False)
    type = Column(String, nullable=False)  # 'income' or 'expense'
    amount = Column(Numeric(10, 2), nullable=False)
    category = Column(String, nullable=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
