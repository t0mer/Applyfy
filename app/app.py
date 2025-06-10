import io
import csv
import uvicorn
import pandas as pd
from typing import List
from jobspy import scrape_jobs
from fastapi import FastAPI, Query
from fastapi.responses import Response

app = FastAPI()

@app.get("/scrape_jobs")
def scrape_jobs_endpoint(
    search_term: str = Query(...),
    location: str = Query(...),
    results_wanted: int = Query(...),
    hours_old: int = Query(...),
    country_indeed: str = Query(...),
):
    jobs = scrape_jobs(
        site_name=["linkedin"],
        search_term=search_term,
        location=location,
        results_wanted=results_wanted,
        hours_old=hours_old,
        country_indeed=country_indeed
    )

    csv_buffer = io.StringIO()
    jobs.to_csv(csv_buffer, quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)
    csv_data = csv_buffer.getvalue()

    return Response(content=csv_data, media_type="text/plain")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
