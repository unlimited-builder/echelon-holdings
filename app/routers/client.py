from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from .. import models, database, auth, schemas
import datetime

router = APIRouter(prefix="/client", tags=["client"])

@router.get("/portfolio")
async def get_portfolio(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    portfolio = db.query(models.Portfolio).filter(models.Portfolio.user_id == current_user.id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    # Calculate current value of all positions
    positions = db.query(models.PortfolioPosition).filter(models.PortfolioPosition.user_id == current_user.id).all()
    positions_value = sum(pos.current_price * pos.quantity for pos in positions)
    
    # Calculate net cash flow from ledger (deposits - withdrawals - asset purchases + asset sales)
    transactions = db.query(models.Transaction).filter(models.Transaction.portfolio_id == portfolio.id).all()
    net_cash_flow = sum(t.amount for t in transactions)
    
    # Total portfolio value = Net cash + Current value of positions
    total_value = net_cash_flow + positions_value
    
    # Update portfolio total for display
    portfolio.total_asset_value = total_value
    db.commit()
    
    # Return as dict for proper serialization
    return {
        "id": portfolio.id,
        "user_id": portfolio.user_id,
        "total_asset_value": portfolio.total_asset_value
    }

@router.get("/ledger-entries")
async def get_ledger_entries(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    portfolio = db.query(models.Portfolio).filter(models.Portfolio.user_id == current_user.id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
        
    transactions = db.query(models.Transaction).filter(
        models.Transaction.portfolio_id == portfolio.id
    ).order_by(models.Transaction.transaction_date.desc()).all()
    
    return transactions

@router.get("/history")
async def get_portfolio_history(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    portfolio = db.query(models.Portfolio).filter(models.Portfolio.user_id == current_user.id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio history not found")
    
    transactions = db.query(models.Transaction).filter(
        models.Transaction.portfolio_id == portfolio.id
    ).order_by(models.Transaction.transaction_date.asc()).all()
    
    cumulative_history = []
    running_balance = 0.0
    for t in transactions:
        running_balance += t.amount
        cumulative_history.append({
            "timestamp": t.transaction_date.isoformat(),
            "value": running_balance
        })
    
    # If no transactions yet, return current snapshot or empty
    if not cumulative_history:
        # Fallback to current value if no transaction history available for the new system
        cumulative_history.append({
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "value": portfolio.total_asset_value
        })

    return cumulative_history
