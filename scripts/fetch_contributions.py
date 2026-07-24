import os
import json
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

USERNAME = "code-with-hashimm"

def fetch_contributions(username=USERNAME):
    # Fetch full year profile contribution page
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
    days = []

    # Modern GitHub calendar uses <td class="ContributionCalendar-day"> or <rect class="ContributionCalendar-day">
    calendar_cells = soup.find_all(attrs={"data-date": True})

    for cell in calendar_cells:
        date_str = cell.get("data-date")
        if not date_str:
            continue

        level_str = cell.get("data-level", "0")
        level = int(level_str) if level_str.isdigit() else 0

        # Extract contribution count from cell attributes, tooltips, or text content
        count = 0
        
        # Check tooltips or aria-label/text
        text_to_search = cell.get_text() or ""
        tool_tip_id = cell.get("aria-describedby") or cell.get("id")
        
        if tool_tip_id:
            tooltip = soup.find(id=tool_tip_id) or soup.find(attrs={"for": tool_tip_id})
            if tooltip:
                text_to_search += " " + tooltip.text.strip()
        
        # Fallback to searching nearby <tool-tip> custom elements
        parent = cell.parent
        if parent:
            text_to_search += " " + parent.get_text()

        match = re.search(r'(\d+)\s+contribution', text_to_search, re.IGNORECASE)
        if match:
            count = int(match.group(1))
        elif level > 0:
            # Fallback estimation if level exists but count text wasn't extracted
            count = level * 2

        days.append({
            "date": date_str,
            "count": count,
            "level": level
        })

    # Deduplicate by date
    unique_days = {}
    for d in days:
        unique_days[d["date"]] = d
    
    sorted_days = [unique_days[k] for k in sorted(unique_days.keys())]

    # Calculate totals and streaks
    total_contributions = sum(d["count"] for d in sorted_days)
    
    current_streak = 0
    longest_streak = 0
    temp_streak = 0

    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    for day in sorted_days:
        if day["count"] > 0:
            temp_streak += 1
            if temp_streak > longest_streak:
                longest_streak = temp_streak
        else:
            temp_streak = 0

    active_streak = 0
    for day in reversed(sorted_days):
        if day["count"] > 0:
            active_streak += 1
        else:
            if day["date"] not in [today, yesterday]:
                break
    current_streak = active_streak

    data = {
        "username": username,
        "updated_at": today,
        "total": total_contributions,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "days": sorted_days
    }

    os.makedirs("data", exist_ok=True)
    with open("data/contributions.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Success! Parsed {total_contributions} contributions across {len(sorted_days)} days.")

if __name__ == "__main__":
    fetch_contributions()
