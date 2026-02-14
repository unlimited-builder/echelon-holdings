from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from .routers import auth as auth_router, admin, client
from . import auth, models
import os

app = FastAPI(title="Deep Echelon Holdings - Proprietary Terminal")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(auth_router.router)
app.include_router(admin.router)
app.include_router(client.router)

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/dashboard")
async def dashboard_page(
    request: Request, 
    db: Session = Depends(get_db),
    user: models.User = Depends(auth.get_current_user_from_cookie)
):
    positions = []
    if user:
        positions = db.query(models.PortfolioPosition).filter(models.PortfolioPosition.user_id == user.id).all()
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "positions": positions
    })

@app.get("/admin-portal")
async def admin_portal_page(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

@app.get("/withdraw")
async def withdraw_page(request: Request):
    return templates.TemplateResponse("withdraw.html", {"request": request})

@app.get("/ledger")
async def ledger_page(request: Request):
    return templates.TemplateResponse("ledger.html", {"request": request})
