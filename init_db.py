from app.database import engine, Base, SessionLocal
from app import models
from app.models import User, Portfolio, Holding, Transaction
from app.auth import get_password_hash
import datetime

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Check if admin exists
    admin = db.query(User).filter(User.username == "echelon_admin").first()
    if not admin:
        admin_user = User(
            username="echelon_admin",
            hashed_password=get_password_hash("Holdings2026!"),
            role="admin"
        )
        db.add(admin_user)
        db.commit()
        print("Administrative account provisioned: echelon_admin")
    
    # Create a test user
    test_user = db.query(User).filter(User.username == "client_alpha").first()
    if not test_user:
        user = User(
            username="client_alpha",
            hashed_password=get_password_hash("client123"),
            role="user"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Initialize portfolio
        portfolio = Portfolio(user_id=user.id, total_asset_value=1250000.0)
        db.add(portfolio)
        db.commit()
        db.refresh(portfolio)
        
        # Add dynamic portfolio positions
        p1 = models.PortfolioPosition(user_id=user.id, asset_name="High-Yield Corp Bonds", entry_price=100.0, current_price=105.2, quantity=1.0)
        p2 = models.PortfolioPosition(user_id=user.id, asset_name="Tech ETF", entry_price=450.0, current_price=512.0, quantity=1.0)
        p3 = models.PortfolioPosition(user_id=user.id, asset_name="Crypto Index", entry_price=12000.0, current_price=14500.0, quantity=1.0)
        db.add_all([p1, p2, p3])
        
        # Seed historical transactions for the new chart logic
        now = datetime.datetime.utcnow()
        t1 = Transaction(portfolio_id=portfolio.id, transaction_type="Deposit", asset_name="Initial Deposit", amount=1000000.0, transaction_date=now - datetime.timedelta(days=30))
        t2 = Transaction(portfolio_id=portfolio.id, transaction_type="Asset Allocation", asset_name="Quantum Fund A", amount=500000.0, transaction_date=now - datetime.timedelta(days=15))
        t3 = Transaction(portfolio_id=portfolio.id, transaction_type="Yield Generation", asset_name="Gain: Tech ETF", amount=250000.0, transaction_date=now - datetime.timedelta(days=5))
        db.add_all([t1, t2, t3])
        
        db.commit()
        print("Test client account provisioned: client_alpha with historical ledger")
        
    db.close()

if __name__ == "__main__":
    init_db()
