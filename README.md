# Deep Echelon Holdings - Client Wealth Portal (v2.0)

## Executive Summary

The Deep Echelon Holdings Client Wealth Portal is a high-performance, secure web interface designed for ultra-high-net-worth individuals to monitor their asset portfolios, view historical performance analytics, and manage liquidity requests. This proprietary platform combines institutional-grade security with an intuitive user experience, providing real-time portfolio valuation and comprehensive wealth management capabilities.

**Version 2.0** introduces significant enhancements including real-time asset allocation, backdated transaction capabilities for historical modeling, enhanced portfolio visualization, and streamlined user interface terminology.

---

## Tech Stack & Architecture

### Backend
- **Framework:** Python 3.x with **FastAPI** - Selected for high concurrency, async performance, and robust API design
- **Database:** **SQLite** - Production-ready file-based storage with ACID compliance
- **Authentication:** Hashed credentials using `bcrypt` with **Role-Based Access Control (RBAC)**
- **Session Management:** JWT-based secure session tokens

### Frontend
- **Templating:** Jinja2 for server-side rendering
- **Styling:** TailwindCSS with custom gold-and-black professional theme
- **Interactivity:** Vanilla JavaScript with Chart.js for data visualization
- **Standards:** HTML5, responsive design principles

### Security
- **Password Hashing:** bcrypt with cryptographic salting
- **Access Control:** Role-based permissions (Client vs. Admin)
- **Session Security:** HTTP-only cookies with CSRF protection
- **Data Validation:** Pydantic schemas for input sanitization

---

## Key Features

### Client Dashboard

#### Real-Time Portfolio Valuation
- **Dynamic Calculation:** Total portfolio value computed as `Net Cash Flow + Current Asset Value`
- **Live Updates:** Asset valuations reflect real-time market pricing set by administrators
- **Multi-Asset Support:** Unified view of cash positions and physical asset holdings

#### Asset Performance Tracking
- **"My Portfolio" View:** Comprehensive display of all allocated assets
- **ROI Analysis:** Side-by-side comparison of Buy Price vs. Current Market Value
- **Performance Indicators:** Color-coded profit/loss visualization (green for gains, red for losses)
- **Asset Details:** Quantity, entry price, current price, and total position value

#### Interactive Growth Chart
- **Historical Visualization:** Time-series graph showing net worth evolution
- **Transaction-Based:** Chart generated from complete transaction ledger
- **Transparency:** Full audit trail from initial deposit to current valuation

#### Transaction History
- **Immutable Ledger:** Complete chronological record of all account activity
- **Categorization:** Automatic tagging (Deposit, Yield Generation, Asset Allocation, etc.)
- **Audit Trail:** Unique reference IDs for compliance and verification
- **Real-Time Updates:** Live synchronization with portfolio changes

### Administrative Controls

#### Client Onboarding
- **Secure Account Creation:** Encrypted credential generation for new clients
- **Profile Management:** Username and password provisioning with bcrypt hashing
- **Access Control:** Automatic role assignment (Client tier)

#### Asset Management ("Market Maker Console")
- **Asset Allocation:** Ability to provision specific assets to client portfolios
- **Price Discovery:** Manual market price setting for illiquid assets (real estate, gemstones)
- **Position Tracking:** Real-time monitoring of all client holdings
- **Flexible Assets:** Support for real estate, precious stones, rare commodities, and traditional securities

#### Fund Operations
- **Direct Deposits:** Instant liquidity injection to client accounts
- **Balance Updates:** Real-time propagation across all interfaces
- **Transaction Recording:** Automatic ledger entries for audit compliance

#### Historical Ledger Injection
- **Backdating Capability:** Create transactions with historical effective dates
- **Data Modeling:** Accurate representation of long-term performance
- **Compliance Tool:** Retroactive reconciliation for legacy accounts
- **Chart Integration:** Backdated transactions correctly populate historical growth curves

### Security Protocols

#### Liquidity Circuit Breaker
- **Automated Withdrawal Suspension:** Service unavailable modal prevents unauthorized fund transfers
- **User Messaging:** Clear, professional communication directing clients to contact support
- **Administrative Override:** Only admin-level users can process withdrawal requests
- **Audit Logging:** All withdrawal attempts recorded for compliance

---

## Installation & Setup Guide

### Prerequisites
- Python 3.9 or higher
- pip package manager
- 500MB available disk space

### Step 1: Clone Repository
```bash
git clone <repository-url>
cd echelon-holdings
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

**Key Dependencies:**
- FastAPI - Web framework
- Uvicorn - ASGI server
- SQLAlchemy - Database ORM
- Pydantic - Data validation
- bcrypt - Password hashing
- python-jose - JWT implementation

### Step 3: Initialize Database
```bash
python init_db.py
```

This script creates:
- SQLite database (`echelon_holdings.db`)
- Core tables (Users, Portfolios, Transactions, Assets, PortfolioPositions)
- Default admin account:
  - Username: `echelon_admin`
  - Password: `Holdings2026!`

### Step 4: Seed VIP Client Data (Optional)
```bash
python seed_vip_client.py
```

This creates the **"Obsidian"** VIP client profile with:
- 15 years of historical transaction data (2011-2026)
- Diversified asset portfolio (real estate, gemstones, securities)
- Realistic growth curve demonstrating platform capabilities
- Login credentials:
  - Username: `client_obsidian`
  - Password: `secure_entry_123`

### Step 5: Run Development Server
```bash
uvicorn app.main:app --reload
```

The application will be available at: `http://localhost:8000`

### Step 6: Access the Platform

**Landing Page:** `http://localhost:8000/`

**Client Login:** `http://localhost:8000/login`
- Use seeded credentials or create new accounts via admin portal

**Admin Portal:** `http://localhost:8000/admin-portal`
- Login with admin credentials to access management controls

---

## Project Structure

```
echelon-holdings/
├── app/
│   ├── routers/
│   │   ├── admin.py          # Admin-only endpoints (asset allocation, backdating)
│   │   ├── auth.py           # Authentication routes (login, logout)
│   │   └── client.py         # Client dashboard and transaction history
│   ├── templates/
│   │   ├── index.html        # Public landing page
│   │   ├── login.html        # Authentication interface
│   │   ├── dashboard.html    # Client portfolio view
│   │   ├── ledger.html       # Transaction history
│   │   ├── withdraw.html     # Withdrawal request (circuit breaker)
│   │   ├── admin.html        # Administrative controls
│   │   └── base.html         # Base template with navigation
│   ├── static/
│   │   └── (static assets)
│   ├── auth.py               # JWT utilities and password hashing
│   ├── database.py           # Database connection and session management
│   ├── main.py               # FastAPI application entry point
│   ├── models.py             # SQLAlchemy ORM models
│   └── schemas.py            # Pydantic validation schemas
├── init_db.py                # Database initialization script
├── seed_vip_client.py        # VIP client data seeding script
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

---

## API Endpoints

### Authentication
- `POST /auth/login` - User authentication
- `GET /auth/logout` - Session termination

### Client Routes (JWT Protected)
- `GET /dashboard` - Portfolio dashboard with assets and chart
- `GET /ledger` - Transaction history
- `GET /withdraw` - Withdrawal request interface
- `GET /api/portfolio-history` - Historical balance data (JSON)

### Admin Routes (Admin Role Required)
- `GET /admin-portal` - Administrative control panel
- `POST /admin/create-user` - Client account provisioning
- `POST /admin/deposit` - Direct fund injection
- `POST /admin/backdate-transaction` - Historical ledger entry
- `POST /admin/allocate-position` - Asset allocation to client
- `POST /admin/update-asset-price` - Market price updates

---

## User Roles & Permissions

### Client Role
- View personal portfolio and transaction history
- Access historical performance charts
- View allocated assets and current valuations
- Request withdrawals (subject to circuit breaker)

### Admin Role
- All client permissions
- Create new user accounts
- Deposit funds to any client account
- Allocate assets to client portfolios
- Set and update asset market prices
- Create backdated transactions
- Access admin control panel

---

## Data Models

### User
- Username, hashed password, role (client/admin)

### Portfolio
- One-to-one relationship with User
- Current balance calculated dynamically

### Transaction
- Transaction type (Deposit, Yield, Asset Allocation, etc.)
- Amount, timestamp, effective date
- Reference ID for audit trail

### Asset
- Asset name, current market price
- Managed globally by administrators

### PortfolioPosition
- Links User to Asset with quantity and entry price
- Track cost basis and current valuation

---

## Version History

### v2.0 (February 2026)
- **UI Terminology Simplification:** Replaced technical jargon with standard fintech language
- **Landing Page Redesign:** Professional, welcoming copy for public-facing interface
- **Enhanced Asset Management:** Real-time portfolio position tracking
- **Backdating Capability:** Historical transaction injection for legacy accounts
- **Portfolio Visualization:** Interactive Chart.js integration
- **Transactional Integrity:** Complete ledger synchronization with asset allocations
- **Circuit Breaker Enhancement:** User-friendly withdrawal suspension messaging

### v1.0 (Initial Release)
- Core authentication and RBAC
- Basic portfolio tracking
- Admin controls for user and fund management
- SQLite database implementation

---

## Security Considerations

### Production Deployment Recommendations
1. **Database Migration:** Replace SQLite with PostgreSQL or MySQL for multi-user concurrency
2. **Secret Management:** Store JWT secret keys in environment variables, not source code
3. **HTTPS Enforcement:** Deploy behind reverse proxy with SSL/TLS termination
4. **Rate Limiting:** Implement request throttling to prevent brute-force attacks
5. **Audit Logging:** Enhanced logging for all administrative actions
6. **Backup Strategy:** Automated database backups with encryption at rest
7. **Session Timeout:** Implement automatic session expiration after inactivity
8. **Two-Factor Authentication:** Add MFA for enhanced admin account security

---

## Disclaimer

**PROPRIETARY SOFTWARE NOTICE**

This software and its documentation are the exclusive property of **Deep Echelon Holdings**. Unauthorized access, use, reproduction, or distribution is strictly prohibited and may be subject to legal action.

**AUTHORIZED PERSONNEL ONLY**

Access to this system is restricted to authorized employees, contractors, and clients of Deep Echelon Holdings. All activities are monitored and logged for security and compliance purposes.

**FINANCIAL SOFTWARE DISCLAIMER**

This platform is designed for wealth management and portfolio tracking. It does not constitute financial advice, investment recommendations, or a solicitation to buy or sell securities. Past performance is not indicative of future results. Users should consult with qualified financial advisors before making investment decisions.

**NO WARRANTY**

This software is provided "as is" without warranty of any kind, express or implied, including but not limited to warranties of merchantability, fitness for a particular purpose, or non-infringement.

---

**© 2026 Deep Echelon Holdings. All rights reserved.**
