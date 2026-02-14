"""
Deep Echelon Holdings - VIP Client Seeding Script
==================================================
This script creates a simulated High-Net-Worth Individual (HNWI) account
with a comprehensive 15-year investment history, demonstrating:
- Historical transaction backdating
- Multi-asset class allocation (gemstones, real estate)
- Market appreciation simulation
- Complete audit trail integrity
"""

import datetime
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, User, Portfolio, PortfolioPosition, Transaction
from app.auth import get_password_hash

def calculate_backdated_timestamp(years_ago: float) -> datetime.datetime:
    """
    Calculate a backdated timestamp from the current moment.
    
    Args:
        years_ago: Number of years to subtract (supports decimals for precision)
    
    Returns:
        datetime object set to the specified point in the past
    """
    days = int(years_ago * 365.25)  # Account for leap years
    return datetime.datetime.utcnow() - datetime.timedelta(days=days)


def cleanup_legacy_account(db: Session, username: str):
    """
    Remove existing test account and all associated data.
    SQLAlchemy cascade rules handle automatic cleanup of:
    - Portfolio
    - Transactions
    - Holdings
    - Portfolio Positions
    """
    legacy_user = db.query(User).filter(User.username == username).first()
    if legacy_user:
        print(f"🗑️  Located legacy account: {username} (ID: {legacy_user.id})")
        db.delete(legacy_user)
        db.commit()
        print(f"✅ Cascade deletion completed for {username}")
    else:
        print(f"ℹ️  No existing account found for {username}")


def seed_vip_client():
    """
    Main seeding function to create "The Obsidian Client" with a 15-year history.
    """
    db = SessionLocal()
    
    try:
        print("\n" + "="*70)
        print("DEEP ECHELON HOLDINGS - VIP CLIENT PROVISIONING PROTOCOL")
        print("="*70 + "\n")
        
        # ========================================
        # STEP 1: Cleanup Legacy Accounts
        # ========================================
        print("PHASE 1: Legacy Account Cleanup")
        print("-" * 70)
        cleanup_legacy_account(db, "client_alpha")
        
        # ========================================
        # STEP 2: Create VIP Profile
        # ========================================
        print("\nPHASE 2: VIP Profile Creation")
        print("-" * 70)
        
        join_date = calculate_backdated_timestamp(15.0)
        print(f"📅 Join Date (Backdated): {join_date.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        
        vip_user = User(
            username="lawrence_flanagan",
            hashed_password=get_password_hash("Pieces&G423"),
            role="user"
        )
        db.add(vip_user)
        db.commit()
        db.refresh(vip_user)
        print(f"✅ VIP Account Created: {vip_user.username} (ID: {vip_user.id})")
        print(f"   Note: Account backdating requires manual database timestamp adjustment")
        
        # ========================================
        # STEP 3: Initialize Portfolio
        # ========================================
        portfolio = Portfolio(
            user_id=vip_user.id,
            total_asset_value=0.0  # Will be dynamically calculated
        )
        db.add(portfolio)
        db.commit()
        db.refresh(portfolio)
        print(f"✅ Portfolio Initialized (ID: {portfolio.id})")
        
        # ========================================
        # STEP 4: Historical Timeline Injection
        # ========================================
        print("\nPHASE 3: 15-Year Historical Timeline Construction")
        print("-" * 70)
        
        # T-minus 15 Years: Initial Liquidity Injection
        print("\n💰 T-15.0Y: Initial Capital Deployment")
        t1 = Transaction(
            portfolio_id=portfolio.id,
            transaction_type="Liquidity Injection",
            asset_name="Primary Account Funding",
            amount=50000000.00,  # $50M inflow (POSITIVE)
            transaction_date=calculate_backdated_timestamp(15.0)
        )
        db.add(t1)
        print(f"   ├─ Deposited: $50,000,000.00")
        
        # T-minus 14.8 Years: Gemstone Acquisitions
        print("\n💎 T-14.8Y: Precious Gemstone Allocation")
        gemstones = [
            ("Fancy Vivid Blue Diamond (IF, 10.12ct)", 3900000.00, 18500000.00),
            ("Pink Diamond 'The Graff Pink' (8.76ct)", 1200000.00, 5100000.00),
            ("Burmese Ruby 'Pigeon Blood' (15.08ct)", 850000.00, 3400000.00),
            ("Colombian Emerald 'Muzo' (12.44ct)", 600000.00, 2200000.00),
        ]
        
        acquisition_date_gems = calculate_backdated_timestamp(14.8)
        for gem_name, cost, current_value in gemstones:
            # Ledger entry: Cost outflow (NEGATIVE)
            t = Transaction(
                portfolio_id=portfolio.id,
                transaction_type="Asset Allocation",
                asset_name=gem_name,
                amount=-cost,  # Negative = money out for purchase
                transaction_date=acquisition_date_gems
            )
            db.add(t)
            
            # Holdings entry: Track asset at cost basis, show current market value
            holding = PortfolioPosition(
                user_id=vip_user.id,
                asset_name=gem_name,
                entry_price=cost,
                current_price=current_value,
                quantity=1.0
            )
            db.add(holding)
            
            roi = ((current_value - cost) / cost) * 100
            print(f"   ├─ {gem_name}")
            print(f"   │  ├─ Cost Basis: ${cost:,.2f}")
            print(f"   │  ├─ Current Value: ${current_value:,.2f}")
            print(f"   │  └─ ROI: +{roi:.1f}%")
        
        # T-minus 14.5 Years: Real Estate Acquisitions
        print("\n🏛️  T-14.5Y: Global Real Estate Positioning")
        properties = [
            ("Penthouse Suite - Le Mirabeau, Monaco", 12500000.00, 28900000.00),
            ("Traditional Villa - Kyoto, Arashiyama District", 4200000.00, 9800000.00),
        ]
        
        acquisition_date_re = calculate_backdated_timestamp(14.5)
        for property_name, cost, current_value in properties:
            # Ledger entry
            t = Transaction(
                portfolio_id=portfolio.id,
                transaction_type="Asset Allocation",
                asset_name=property_name,
                amount=-cost,
                transaction_date=acquisition_date_re
            )
            db.add(t)
            
            # Holdings entry
            holding = PortfolioPosition(
                user_id=vip_user.id,
                asset_name=property_name,
                entry_price=cost,
                current_price=current_value,
                quantity=1.0
            )
            db.add(holding)
            
            roi = ((current_value - cost) / cost) * 100
            print(f"   ├─ {property_name}")
            print(f"   │  ├─ Cost Basis: ${cost:,.2f}")
            print(f"   │  ├─ Current Value: ${current_value:,.2f}")
            print(f"   │  └─ ROI: +{roi:.1f}%")
        
        # T-minus 12 Years: Lifestyle Withdrawal
        print("\n💸 T-12.0Y: Liquidity Withdrawal Event")
        t_withdrawal = Transaction(
            portfolio_id=portfolio.id,
            transaction_type="Withdrawal",
            asset_name="Lifestyle Disbursement",
            amount=-2500000.00,  # $2.5M outflow (NEGATIVE)
            transaction_date=calculate_backdated_timestamp(12.0)
        )
        db.add(t_withdrawal)
        print(f"   └─ Withdrawn: $2,500,000.00")
        
        db.commit()
        
        # ========================================
        # STEP 5: Balance Verification
        # ========================================
        print("\nPHASE 4: Financial Position Summary")
        print("-" * 70)
        
        # Calculate cash on hand (net cash flow)
        all_transactions = db.query(Transaction).filter(
            Transaction.portfolio_id == portfolio.id
        ).all()
        net_cash_flow = sum(t.amount for t in all_transactions)
        
        # Calculate total holdings value
        all_holdings = db.query(PortfolioPosition).filter(
            PortfolioPosition.user_id == vip_user.id
        ).all()
        total_holdings_value = sum(h.current_price * h.quantity for h in all_holdings)
        
        # Total net worth
        total_net_worth = net_cash_flow + total_holdings_value
        
        print(f"\n📊 Cash Position Analysis:")
        print(f"   ├─ Initial Funding:      +$50,000,000.00")
        print(f"   ├─ Asset Acquisitions:   -${sum(cost for _, cost, _ in gemstones + properties):,.2f}")
        print(f"   ├─ Lifestyle Withdrawal: -$2,500,000.00")
        print(f"   └─ Cash on Hand:         ${net_cash_flow:,.2f}")
        
        print(f"\n💼 Holdings Valuation:")
        print(f"   ├─ Number of Assets:     {len(all_holdings)}")
        print(f"   ├─ Total Cost Basis:     ${sum(cost for _, cost, _ in gemstones + properties):,.2f}")
        print(f"   └─ Current Market Value: ${total_holdings_value:,.2f}")
        
        print(f"\n🏆 Total Net Worth:         ${total_net_worth:,.2f}")
        
        # Update portfolio total
        portfolio.total_asset_value = total_net_worth
        db.commit()
        
        print("\n" + "="*70)
        print("✅ VIP CLIENT PROVISIONING COMPLETE")
        print("="*70)
        print(f"\n🔐 Login Credentials:")
        print(f"   Username: lawrence_flanagan")
        print(f"   Password: Pieces&G423")
        print(f"\n📅 Account Age: 15 Years")
        print(f"💎 Portfolio Span: 6 Premium Assets")
        print(f"📈 Average ROI: ~{((total_holdings_value - sum(cost for _, cost, _ in gemstones + properties)) / sum(cost for _, cost, _ in gemstones + properties)) * 100:.1f}%")
        print("\n")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ ERROR: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_vip_client()
