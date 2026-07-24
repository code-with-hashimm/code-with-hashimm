import os
import json
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

USERNAME = "code-with-hashimm"

def fetch_contributions(username=USERNAME):
    url = f"https://github.com/users/{username}/contributions"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return

    soup = BeautifulSoup(response.text, "html.parser")
    days = []
    
    for td in soup.find_all("td", class_="ContributionCalendar-day"):
        date_str = td.get("data-date")
        level_str = td.get("data-level", "0")
        if not date_str:
            continue

        level = int(level_str)
        count = 0
        tool_tip_id = td.get("aria-describedby")
        if tool_tip_id:
            tooltip = soup.find(id=tool_tip_id)
            if tooltip:
                match = re.search(r'(\d+)\s+contribution', tooltip.text.strip())
                if match:
                    count = int(match.group(1))
        
        days.append({"date": date_str, "count": count, "level": level})

    days.sort(key=lambda x: x["date"])
    total_contributions = sum(d["count"] for d in days)

    data = {
        "username": username,
        "updated_at": datetime.now().strftime("%Y-%m-%d"),
        "total": total_contributions,
        "current_streak": 0,
        "longest_streak": 0,
        "days": days
    }

    os.makedirs("data", exist_ok=True)
    with open("data/contributions.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    fetch_contributions()
