from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="user") # 'admin' or 'user'
    
    portfolio = relationship("Portfolio", back_populates="owner", uselist=False)
    positions = relationship("PortfolioPosition", back_populates="owner")

class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_asset_value = Column(Float, default=0.0)
    
    owner = relationship("User", back_populates="portfolio")
    holdings = relationship("Holding", back_populates="portfolio")
    transactions = relationship("Transaction", back_populates="portfolio")

class Holding(Base):
    __tablename__ = "holdings"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"))
    asset_name = Column(String)
    entry_price = Column(Float)
    current_value = Column(Float)
    roi = Column(Float) # Calculated field (current - entry) / entry * 100

    portfolio = relationship("Portfolio", back_populates="holdings")

class PortfolioHistory(Base):
    __tablename__ = "portfolio_history"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    value = Column(Float)

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"))
    transaction_type = Column(String, default="Asset Allocation") # e.g., Deposit, Yield Generation, Asset Allocation
    asset_name = Column(String)
    amount = Column(Float) # Positive for investment/gain, negative for withdrawal/loss
    transaction_date = Column(DateTime, default=datetime.datetime.utcnow)

    portfolio = relationship("Portfolio", back_populates="transactions")

class PortfolioPosition(Base):
    __tablename__ = "portfolio_positions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    asset_name = Column(String)
    entry_price = Column(Float)
    current_price = Column(Float)
    quantity = Column(Float)

    owner = relationship("User", back_populates="positions")
