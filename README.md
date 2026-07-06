# Portfolio Analyzer

A Portfolio Analyzer built on a modern data stack.

Pulls daily stock prices, transforms the data with dbt, and renders a live
portfolio dashboard directly from Supabase/Polygon/FRED. A Claude API analyzer
answers natural-language questions against the same live data using tool use.

---

## What It Does

- Fetches daily prices for 560+ stocks from Polygon.io and loads them into Supabase
- dbt staging and mart models clean and transform the raw data into portfolio metrics
- Streamlit dashboard calls Supabase/Polygon/FRED directly to render live portfolio
  positions, KPIs, sector exposure, market movers, news, and economic indicators
- Claude API portfolio analyzer uses tool use to answer questions against live data,
  with multi-turn conversation history
- Add/Sell Position forms write directly to Supabase — new tickers are
  auto-registered and backfilled with price history via Polygon
- Realized P&L mart tracks per-sale gains using weighted average cost basis
- GitHub Actions runs the price fetch and `dbt run` automatically every weekday
  at 4:30 PM ET
- A FastAPI layer exists with equivalent endpoints but is not currently used by
  the dashboard

---

## Stack

| Layer | Tool |
|-------|------|
| Data source | Polygon.io, FRED |
| Database | Supabase (PostgreSQL) |
| Transformation | dbt |
| Dashboard | Streamlit |
| AI layer | Claude API with tool use |
| API (unused by dashboard) | FastAPI |
| Automation | GitHub Actions |
| Language | Python |

---

## Project Structure

| Folder | What it does |
|--------|-------------|
| `ingestion/` | Daily price fetcher and backfill script |
| `dbt/` | Staging models and portfolio marts |
| `dashboard/` | Streamlit portfolio dashboard (calls Supabase/Polygon/FRED directly) |
| `analysis/` | Claude API portfolio analyzer |
| `api/` | FastAPI service (exists, not wired to the dashboard) |
| `schema/` | Database schema |
| `.github/workflows/` | Automated daily pipeline (price fetch + dbt run) |

---

## Database Schema

Source tables in Supabase: `stocks`, `price_history`, `fundamentals`, `portfolio`
(buy lots), `sales` (sell transactions).

dbt marts: `portfolio_positions`, `portfolio_summary`, `portfolio_sector_exposure`,
`portfolio_vs_spy`, `market_movers`, `realized_pnl`.

---

## Status

Active build. Phases 1–9 complete: ingestion, dbt layer, dashboard (with Market
Movers, News, and Economic Indicators tabs), Claude API analyzer with multi-turn
history, and Add/Sell Position forms with realized P&L tracking.

Next up: Realized P&L KPI card and total return (unrealized + realized) in the Portfolio Summary tab.
