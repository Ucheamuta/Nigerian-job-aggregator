from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
from scraper import scrape_jobs

app = FastAPI(title="Nigerian Job Aggregator")
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home():
    return {"message": "Job Aggregator API running"}

@app.get("/scrape")
def run_scrape():
    df = scrape_jobs()
    return {"records": len(df), "message": "Scraped & exported successfully"}

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    df = pd.read_csv("data/jobs.csv") if pd.io.common.file_exists("data/jobs.csv") else pd.DataFrame()
    stats = {
        "total_jobs": len(df),
        "companies": df["company"].nunique() if not df.empty else 0
    }
    return templates.TemplateResponse("dashboard.html", {"request": request, "stats": stats, "data": df.to_dict(orient="records")})
