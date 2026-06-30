from fastapi import FastAPI
from dotenv import load_dotenv
from supabase import create_client
import os
import requests as http_requests

POLYGON_BASE = "https://api.polygon.io"
FRED_BASE    = "https://api.stlouisfed.org/fred"

load_dotenv()

app = FastAPI(title="AI Portfolio Analyst API")

supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

@app.get("/portfolio/summary")
def get_summary():
    result = supabase.table("portfolio_summary").select("*").execute()
    return result.data[0] if result.data else {}

@app.get("/portfolio/positions")
def get_positions():
    result = supabase.table("portfolio_positions").select("*").execute()
    return result.data

@app.get("/portfolio/sector")
def get_sector():
    result = supabase.table("portfolio_sector_exposure").select("*").execute()
    return result.data

@app.get("/portfolio/spy")
def get_spy():
    result = supabase.table("portfolio_vs_spy").select("*").execute()
    return result.data

@app.get("/market/movers")
def get_movers(limit: int = 10):
    """Top gainers and top losers from the 560-ticker universe."""
    gainers = (
        supabase.table("market_movers")
        .select("*")
        .order("change_pct", desc=True)
        .limit(limit)
        .execute()
    )
    losers = (
        supabase.table("market_movers")
        .select("*")
        .order("change_pct", desc=False)
        .limit(limit)
        .execute()
    )
    return {"gainers": gainers.data, "losers": losers.data}


@app.get("/market/news")
def get_news(ticker: str = None, limit: int = 20):
    """
    Latest news from Polygon /v2/reference/news.
    Optionally filter to a single ticker with ?ticker=AAPL.
    """
    params = {
        "apiKey": os.environ["POLYGON_API_KEY"],
        "limit":  limit,
        "order":  "desc",
        "sort":   "published_utc",
    }
    if ticker:
        params["ticker.any_of"] = ticker
    resp = http_requests.get(f"{POLYGON_BASE}/v2/reference/news", params=params, timeout=10)
    resp.raise_for_status()
    return resp.json().get("results", [])


@app.get("/market/indicators")
def get_indicators():
    """
    Last 24 observations for 4 FRED macro series.
    FEDFUNDS (monthly), CPIAUCSL (monthly), GDP (quarterly), UNRATE (monthly).
    """
    fred_key = os.environ["FRED_API_KEY"]
    series_map = {
        "fed_funds_rate": "FEDFUNDS",
        "cpi":            "CPIAUCSL",
        "gdp":            "GDP",
        "unemployment":   "UNRATE",
    }
    result = {}
    for name, series_id in series_map.items():
        resp = http_requests.get(
            f"{FRED_BASE}/series/observations",
            params={
                "series_id":  series_id,
                "api_key":    fred_key,
                "file_type":  "json",
                "limit":      24,
                "sort_order": "desc",
            },
            timeout=10,
        )
        resp.raise_for_status()
        obs = resp.json().get("observations", [])
        # FRED marks missing observations with a literal "." — filter them out
        result[name] = [o for o in obs if o["value"] != "."]
    return result