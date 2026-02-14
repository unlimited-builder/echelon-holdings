from pydantic import BaseModel
from typing import List, Optional
import datetime

class UserCreate(BaseModel):
    username: str
    password: str

class LiquidityInjection(BaseModel):
    username: str
    amount: float

class TemporalInjection(BaseModel):
    username: str
    asset_name: str
    amount: float
    effective_date: datetime.datetime

class HoldingBase(BaseModel):
    asset_name: str
    entry_price: float
    current_value: float
    roi: float

class PortfolioBase(BaseModel):
    total_asset_value: float
    holdings: List[HoldingBase]

class UserResponse(BaseModel):
    username: str
    role: str
    portfolio: Optional[PortfolioBase]

    class Config:
        from_attributes = True

class PositionAllocate(BaseModel):
    username: str
    asset_name: str
    entry_price: float
    current_price: float
    quantity: float
