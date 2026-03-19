import requests
import pandas as pd
import os
os.makedirs("data", exist_ok=True)

def scrape_jobs(limit=50):
    r = requests.get("https://remoteok.com/api")
    jobs = r.json()[1:]  # real remote jobs data
    data = []
    for job in jobs[:limit]:
        data.append({
            "title": job.get("position", "N/A"),
            "company": job.get("company", "N/A"),
            "location": "Remote (Nigeria-eligible)",
            "salary": job.get("salary", "Negotiable")
        })
    df = pd.DataFrame(data)
    df.to_csv("data/jobs.csv", index=False)
    print(f"Scraped {len(df)} jobs")
    return df
