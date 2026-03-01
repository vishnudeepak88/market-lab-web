import io
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
import matplotlib
matplotlib.use('Agg') # head-less rendering
import matplotlib.pyplot as plt

from app.db import get_db
from app.services.market_service import get_leaderboard_data, get_ticker_detail, get_ticker_history
from app.config import settings

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def index_page(request: Request, db = Depends(get_db)):
    context = {
        "request": request,
        "app_name": settings.app_name,
        "mode": "Postgres (Connected)" if settings.database_url else "Demo (In-Memory)",
    }
    return templates.TemplateResponse("index.html", context)

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request, db = Depends(get_db)):
    # Render page without logic initially
    leaderboard = get_leaderboard_data(20, None, None, db)
    context = {
        "request": request,
        "app_name": settings.app_name,
        "leaderboard": leaderboard
    }
    return templates.TemplateResponse("dashboard.html", context)

@router.get("/ticker/{symbol}", response_class=HTMLResponse)
async def ticker_detail_page(request: Request, symbol: str, db = Depends(get_db)):
    detail = get_ticker_detail(symbol, db)
    if not detail or not detail.get('date'):
        raise HTTPException(status_code=404, detail="Ticker not found")
        
    context = {
        "request": request,
        "app_name": settings.app_name,
        "detail": detail
    }
    return templates.TemplateResponse("ticker.html", context)

@router.get("/chart/{symbol}.png")
async def ticker_chart_png(symbol: str, db = Depends(get_db)):
    hist = get_ticker_history(symbol, 180, db)
    if not hist:
        raise HTTPException(status_code=404, detail="No history found for chart")
        
    # Reverse so oldest is first
    hist.reverse()
    dates = [h['date'] for h in hist]
    closes = [h['close'] for h in hist]
    
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(dates, closes, color='#2563eb', linewidth=2)
    ax.set_title(f"{symbol.upper()} - 180 Days")
    ax.set_xticklabels([])
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100)
    plt.close(fig)
    buf.seek(0)
    
    return Response(content=buf.getvalue(), media_type="image/png")
