import os
import json
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

USERNAME = "code-with-hashimm"

def fetch_contributions(username=USERNAME):
    url = f"https://github.com/users/{username}/contributions"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    
    print(f"Fetching contribution data for @{username}...")
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching data: HTTP {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    parsed_days = {}

    calendar_cells = soup.find_all(attrs={"data-date": True})

    for cell in calendar_cells:
        date_str = cell.get("data-date")
        if not date_str:
            continue

        level_str = cell.get("data-level", "0")
        level = int(level_str) if level_str.isdigit() else 0

        count = 0
        text_to_search = cell.get_text() or ""
        tool_tip_id = cell.get("aria-describedby") or cell.get("id")
        
        if tool_tip_id:
            tooltip = soup.find(id=tool_tip_id) or soup.find(attrs={"for": tool_tip_id})
            if tooltip:
                text_to_search += " " + tooltip.text.strip()
        
        parent = cell.parent
        if parent:
            text_to_search += " " + parent.get_text()

        match = re.search(r'(\d+)\s+contribution', text_to_search, re.IGNORECASE)
        if match:
            count = int(match.group(1))

        parsed_days[date_str] = {"date": date_str, "count": count, "level": level}

    # Generate full 365-day continuous timeline up to today
    today_dt = datetime.now()
    all_dates = [(today_dt - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(365)]
    all_dates.reverse()

    days = []
    max_count = max([parsed_days.get(d, {}).get("count", 0) for d in all_dates] or [1])

    for d_str in all_dates:
        item = parsed_days.get(d_str, {"date": d_str, "count": 0, "level": 0})
        cnt = item["count"]
        lvl = item["level"]

        # Calculate dynamic color intensity if level was not provided by GitHub
        if lvl == 0 and cnt > 0:
            if cnt <= 2:
                lvl = 1
            elif cnt <= 5:
                lvl = 2
            elif cnt <= 9:
                lvl = 3
            else:
                lvl = 4

        days.append({"date": d_str, "count": cnt, "level": lvl})

    total_contributions = sum(d["count"] for d in days)

    data = {
        "username": username,
        "updated_at": today_dt.strftime("%Y-%m-%d"),
        "total": total_contributions,
        "days": days
    }

    os.makedirs("data", exist_ok=True)
    with open("data/contributions.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Success! Fetched {total_contributions} contributions across 365 days.")

if __name__ == "__main__":
    fetch_contributions()
