from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, database, auth, schemas
import datetime

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: schemas.UserCreate,
    db: Session = Depends(database.get_db),
    admin: models.User = Depends(auth.get_current_admin)
):
    existing_user = db.query(models.User).filter(models.User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Institutional ID already exists")
    
    new_user = models.User(
        username=user_data.username,
        hashed_password=auth.get_password_hash(user_data.password),
        role="user"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Initialize empty portfolio
    portfolio = models.Portfolio(user_id=new_user.id, total_asset_value=0.0)
    db.add(portfolio)
    db.commit()
    
    return {"message": f"Client account {new_user.username} provisioned"}

@router.post("/inject-liquidity")
async def inject_liquidity(
    data: schemas.LiquidityInjection,
    db: Session = Depends(database.get_db),
    admin: models.User = Depends(auth.get_current_admin)
):
    user = db.query(models.User).filter(models.User.username == data.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Client not found")
    
    portfolio = db.query(models.Portfolio).filter(models.Portfolio.user_id == user.id).first()
    portfolio.total_asset_value += data.amount
    
    # Track history for chart
    transaction = models.Transaction(
        portfolio_id=portfolio.id,
        transaction_type="Liquidity Injection",
        asset_name="Standard Liquidity Injection",
        amount=data.amount,
        transaction_date=datetime.datetime.utcnow()
    )
    db.add(transaction)
    
    db.commit()
    return {"message": f"Liquidity injection successful. New balance: {portfolio.total_asset_value}"}

@router.post("/retroactive-ledger-reconciliation")
async def retroactive_ledger_reconciliation(
    data: schemas.TemporalInjection,
    db: Session = Depends(database.get_db),
    admin: models.User = Depends(auth.get_current_admin)
):
    user = db.query(models.User).filter(models.User.username == data.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Client not found")
    
    portfolio = db.query(models.Portfolio).filter(models.Portfolio.user_id == user.id).first()
    
    # Create the transaction entry
    transaction = models.Transaction(
        portfolio_id=portfolio.id,
        transaction_type="Retroactive Reconciliation",
        asset_name=data.asset_name,
        amount=data.amount,
        transaction_date=data.effective_date
    )
    db.add(transaction)
    
    # Update current portfolio value
    portfolio.total_asset_value += data.amount
    
    db.commit()
    return {"message": "Retroactive ledger reconciliation successful."}

@router.post("/allocate-position")
async def allocate_position(
    data: schemas.PositionAllocate,
    db: Session = Depends(database.get_db),
    admin: models.User = Depends(auth.get_current_admin)
):
    user = db.query(models.User).filter(models.User.username == data.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # Get user's portfolio for transaction logging
    portfolio = db.query(models.Portfolio).filter(models.Portfolio.user_id == user.id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    # Check if position already exists for this user and asset
    position = db.query(models.PortfolioPosition).filter(
        models.PortfolioPosition.user_id == user.id,
        models.PortfolioPosition.asset_name == data.asset_name
    ).first()
    
    is_new_position = position is None
    old_quantity = position.quantity if position else 0
    
    if position:
        # Update existing position
        position.entry_price = data.entry_price
        position.current_price = data.current_price
        position.quantity = data.quantity
    else:
        # Create new position
        position = models.PortfolioPosition(
            user_id=user.id,
            asset_name=data.asset_name,
            entry_price=data.entry_price,
            current_price=data.current_price,
            quantity=data.quantity
        )
        db.add(position)
    
    # Create corresponding Transaction record for audit trail
    if is_new_position or data.quantity != old_quantity:
        quantity_delta = data.quantity - old_quantity
        
        if quantity_delta > 0:
            # Asset purchase/allocation - negative amount (cost)
            transaction = models.Transaction(
                portfolio_id=portfolio.id,
                transaction_type="Asset Allocation",
                asset_name=data.asset_name,
                amount=-(data.entry_price * quantity_delta),  # Negative = money out
                transaction_date=datetime.datetime.utcnow()
            )
            db.add(transaction)
        elif quantity_delta < 0:
            # Asset liquidation/sale - positive amount (cash return)
            transaction = models.Transaction(
                portfolio_id=portfolio.id,
                transaction_type="Asset Liquidation",
                asset_name=data.asset_name,
                amount=data.current_price * abs(quantity_delta),  # Positive = money in
                transaction_date=datetime.datetime.utcnow()
            )
            db.add(transaction)
    
    db.commit()
    return {"message": f"Asset allocation for {data.asset_name} synchronized."}

@router.get("/users")
async def list_users(
    db: Session = Depends(database.get_db),
    admin: models.User = Depends(auth.get_current_admin)
):
    users = db.query(models.User).filter(models.User.role == "user").all()
    return [{"username": u.username, "balance": u.portfolio.total_asset_value if u.portfolio else 0} for u in users]
