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
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    
    print(f"Fetching contribution data for @{username}...")
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching data: HTTP {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    raw_days = []
    
    # Get current year
    current_year = str(datetime.now().year)

    for td in soup.find_all("td", class_="ContributionCalendar-day"):
        date_str = td.get("data-date")
        level_str = td.get("data-level", "0")
        
        if not date_str:
            continue
            
        # Filter: keep only entries for the current year
        if not date_str.startswith(current_year):
            continue

        level = int(level_str)
        count = 0
        
        tool_tip_id = td.get("aria-describedby")
        if tool_tip_id:
            tooltip = soup.find(id=tool_tip_id)
            if tooltip:
                text = tooltip.text.strip()
                match = re.search(r'(\d+)\s+contribution', text)
                if match:
                    count = int(match.group(1))
        
        raw_days.append({
            "date": date_str,
            "count": count,
            "level": level
        })

    raw_days.sort(key=lambda x: x["date"])

    total_contributions = sum(d["count"] for d in raw_days)
    best_day = max(raw_days, key=lambda x: x["count"]) if raw_days else {"date": "N/A", "count": 0}

    # Calculate streaks for current year
    current_streak = 0
    longest_streak = 0
    temp_streak = 0

    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    for day in raw_days:
        if day["count"] > 0:
            temp_streak += 1
            if temp_streak > longest_streak:
                longest_streak = temp_streak
        else:
            temp_streak = 0

    active_streak = 0
    for day in reversed(raw_days):
        if day["count"] > 0:
            active_streak += 1
        else:
            if day["date"] not in [today, yesterday]:
                break
    current_streak = active_streak

    data = {
        "username": username,
        "year": current_year,
        "updated_at": today,
        "total": total_contributions,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day": best_day,
        "days": raw_days
    }

    os.makedirs("data", exist_ok=True)
    with open("data/contributions.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Success! Saved {total_contributions} contributions for {current_year} to data/contributions.json")

if __name__ == "__main__":
    fetch_contributions()
